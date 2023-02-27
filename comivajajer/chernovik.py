from operator import attrgetter
import random, sys, time, copy
import chernovik3 as ch

class Graph:

    def __init__(self, amount_vertices):
        self.edges = {}  # словарь крайних значений
        self.vertices = set()  # вершины
        self.amount_vertices = amount_vertices  # количество вершин aus1

    #метод добавления вершин aus2
    def addEdge(self, src, dest, cost=0):
        #если есть - то не надо
        if not self.existsEdge(src, dest):
            self.edges[(src, dest)] = cost
            self.vertices.add(src)
            self.vertices.add(dest)

    def existsEdge(self, src, dest):
        return (True if (src, dest) in self.edges else False)

    # все вершины графа
    def showGraph(self):
        print('Всего в графе:\n')
        for edge in self.edges:
            print('%d создано на %d с суммарной стоимостью %d' % (edge[0], edge[1], self.edges[edge]))

    # полная стоимость пути
    def getCostPath(self, path):

        total_cost = 0
        for i in range(self.amount_vertices - 1):
            total_cost += self.edges[(path[i], path[i + 1])]

        # плюсуем стоимость пути графа к вершине
        total_cost += self.edges[(path[self.amount_vertices - 1], path[0])]
        return total_cost

    # рандомный путь - список рандомных путей aus4
    def getRandomPaths(self, max_size):

        random_paths, list_vertices = [], list(self.vertices)

        initial_vertice = random.choice(list_vertices)
        if initial_vertice not in list_vertices:
            print('Error: нет такой %d not вершины!' % initial_vertice)
            sys.exit(1)

        list_vertices.remove(initial_vertice)
        list_vertices.insert(0, initial_vertice)

        for i in range(max_size):
            list_temp = list_vertices[1:]
            random.shuffle(list_temp)
            list_temp.insert(0, initial_vertice)

            if list_temp not in random_paths:
                random_paths.append(list_temp)

        return random_paths

#Закончили с графом - переходим к обработке aus5
#готовый граф
class CompleteGraph(Graph):

    # создаём готовый граф
    def generates(self):
        for i in range(self.amount_vertices):
            for j in range(self.amount_vertices):
                if i != j:
                    weight = random.randint(1, 10)
                    self.addEdge(i, j, weight)


# сами вычисления aus6
class Particle:

    def __init__(self, solution, cost):
        # решение на текущую итерацию
        self.solution = solution

        # лучшее решение на данный момент
        self.pbest = solution

        # меняем стоимость
        self.cost_current_solution = cost
        self.cost_pbest_solution = cost

        # наши вершины это последовательность из 4 кортежей
        # (1, 2, 1, 'beta') means SO(1,2), вероятность 1 сравниваем с "beta"
        self.velocity = []

    # меняем лучшее
    def setPBest(self, new_pbest):
        self.pbest = new_pbest

    # возвращаем лучшее
    def getPBest(self):
        return self.pbest

    # добавляем новую вершину в наш путь (ну закидываем вершину в кортже, не забыть рассказать о муравьях)
    def setVelocity(self, new_velocity):
        self.velocity = new_velocity

    # то же самое, что выше, но возвращаем aus
    def getVelocity(self):
        return self.velocity

    def setCurrentSolution(self, solution):
        self.solution = solution

    def getCurrentSolution(self):
        return self.solution

    def setCostPBest(self, cost):
        self.cost_pbest_solution = cost

    def getCostPBest(self):
        return self.cost_pbest_solution

    def setCostCurrentSolution(self, cost):
        self.cost_current_solution = cost

    def getCostCurrentSolution(self):
        return self.cost_current_solution

    # очищаем список вершин
    def clearVelocity(self):
        del self.velocity[:]


#реализация самого алгоритма
class PSO:

    def __init__(self, graph, iterations, size_population, beta=1, alfa=0.9):
        self.graph = graph  #граф
        self.iterations = iterations
        self.size_population = size_population
        self.particles = []
        self.beta = beta
        self.alfa = alfa

        # случайные 100 путей aus
        solutions = self.graph.getRandomPaths(self.size_population)

        if not solutions:
            print('Не ввёл популяцию...')
            sys.exit(1)

        # создаём решения и начинаем меняь их местами и меняем пути
        for solution in solutions:
            #создаём новое решение
            particle = Particle(solution=solution, cost=graph.getCostPath(solution))
            # закидываем наше решение в список решений
            self.particles.append(particle)

        # обновить размер роя
        self.size_population = len(self.particles)

    # лучшее решение роя aus
    def setGBest(self, new_gbest):
        self.gbest = new_gbest

    # в ответ выводим его
    def getGBest(self):
        return self.gbest

    def showsParticles(self):

        print('Все реешния...\n')
        for particle in self.particles:
            print('Лучший путь: %s\t|\tЛучшая стоимость: %d\t|\tтекущий путь: %s\t|\tтекущая стоимость: %d' \
                  % (str(particle.getPBest()), particle.getCostPBest(), str(particle.getCurrentSolution()),
                     particle.getCostCurrentSolution()))
        print('')

    def run(self):

        # для каждой итерации
        for t in range(self.iterations):

            # обновим лучший путь
            self.gbest = min(self.particles, key=attrgetter('cost_pbest_solution'))

            # для каждого пути (итерации лучшего путя) в рое aus
            for particle in self.particles:

                particle.clearVelocity()  # чистим путь
                temp_velocity = []
                solution_gbest = copy.copy(self.gbest.getPBest())  # лучшее решение
                solution_pbest = particle.getPBest()[:]  # делаем копию лучшего решения
                solution_particle = particle.getCurrentSolution()[
                                    :]  #закидываем копию текущего решения в список всех решений

                # пробуем всевозможные комбинации (pbest - x(t-1)) aus
                for i in range(self.graph.amount_vertices):
                    if solution_particle[i] != solution_pbest[i]:
                        # выбираем вершину для смены её на другую
                        swap_operator = (i, solution_pbest.index(solution_particle[i]), self.alfa)

                        # добавляем нашу вершину, которую будем менять в список вершин
                        temp_velocity.append(swap_operator)

                        # меняем
                        aux = solution_pbest[swap_operator[0]]
                        solution_pbest[swap_operator[0]] = solution_pbest[swap_operator[1]]
                        solution_pbest[swap_operator[1]] = aux

                # создаём все вершины для смены их позиций to calculate (gbest - x(t-1))
                for i in range(self.graph.amount_vertices):
                    if solution_particle[i] != solution_gbest[i]:
                        #создаём вершину
                        swap_operator = (i, solution_gbest.index(solution_particle[i]), self.beta)

                        temp_velocity.append(swap_operator)

                        aux = solution_gbest[swap_operator[0]]
                        solution_gbest[swap_operator[0]] = solution_gbest[swap_operator[1]]
                        solution_gbest[swap_operator[1]] = aux

                # обновляем вершину
                particle.setVelocity(temp_velocity)

                # генерируем новое решение на основе тех вершин, которые мы поменяли местами
                for swap_operator in temp_velocity:
                    if random.random() <= swap_operator[2]:
                        aux = solution_particle[swap_operator[0]]
                        solution_particle[swap_operator[0]] = solution_particle[swap_operator[1]]
                        solution_particle[swap_operator[1]] = aux

                # переписываем путь
                particle.setCurrentSolution(solution_particle)
                # считаем стоимость текущего пути
                cost_current_solution = self.graph.getCostPath(solution_particle)
                # обновляем стоимость текущего пути
                particle.setCostCurrentSolution(cost_current_solution)

                # проверяем лучшее и текущее решение
                if cost_current_solution < particle.getCostPBest():
                    particle.setPBest(solution_particle)
                    particle.setCostPBest(cost_current_solution)


if __name__ == "__main__": #ausконец
    graph = Graph(amount_vertices=9)
    graph.addEdge(0, 1, 13)
    graph.addEdge(0, 2, 11)
    graph.addEdge(0, 3, 11)
    graph.addEdge(0, 4, 11)
    graph.addEdge(0, 5, 14)
    graph.addEdge(0, 6, 19)
    graph.addEdge(0, 7, 13)
    graph.addEdge(0, 8, 8)
    graph.addEdge(1, 0, 13)
    graph.addEdge(1, 2, 8)
    graph.addEdge(1, 3, 8)
    graph.addEdge(1, 4, 8)
    graph.addEdge(1, 5, 11)
    graph.addEdge(1, 6, 16)
    graph.addEdge(1, 7, 16)
    graph.addEdge(1, 8, 10)
    graph.addEdge(2, 0, 11)
    graph.addEdge(2, 1, 8)
    graph.addEdge(2, 3, 10)
    graph.addEdge(2, 4, 10)
    graph.addEdge(2, 5, 3)
    graph.addEdge(2, 6, 8)
    graph.addEdge(2, 7, 13)
    graph.addEdge(2, 8, 8)
    graph.addEdge(3, 0, 11)
    graph.addEdge(3, 1, 8)
    graph.addEdge(3, 2, 10)
    graph.addEdge(3, 4, 10)
    graph.addEdge(3, 5, 3)
    graph.addEdge(3, 6, 8)
    graph.addEdge(3, 7, 13)
    graph.addEdge(3, 8, 8)
    graph.addEdge(4, 0, 11)
    graph.addEdge(4, 1, 8)
    graph.addEdge(4, 2, 10)
    graph.addEdge(4, 3, 10)
    graph.addEdge(4, 5, 3)
    graph.addEdge(4, 6, 8)
    graph.addEdge(4, 7, 13)
    graph.addEdge(4, 8, 8)
    graph.addEdge(5, 0, 14)
    graph.addEdge(5, 1, 11)
    graph.addEdge(5, 2, 3)
    graph.addEdge(5, 3, 3)
    graph.addEdge(5, 4, 3)
    graph.addEdge(5, 6, 5)
    graph.addEdge(5, 7, 14)
    graph.addEdge(5, 8, 11)
    graph.addEdge(6, 0, 19)
    graph.addEdge(6, 1, 16)
    graph.addEdge(6, 2, 8)
    graph.addEdge(6, 3, 8)
    graph.addEdge(6, 4, 8)
    graph.addEdge(6, 5, 5)
    graph.addEdge(6, 7, 9)
    graph.addEdge(6, 8, 14)
    graph.addEdge(7, 0, 13)
    graph.addEdge(7, 1, 16)
    graph.addEdge(7, 2, 13)
    graph.addEdge(7, 3, 13)
    graph.addEdge(7, 4, 13)
    graph.addEdge(7, 5, 14)
    graph.addEdge(7, 6, 9)
    graph.addEdge(7, 8, 6)
    graph.addEdge(8, 0, 8)
    graph.addEdge(8, 1, 10)
    graph.addEdge(8, 2, 8)
    graph.addEdge(8, 3, 8)
    graph.addEdge(8, 4, 8)
    graph.addEdge(8, 5, 11)
    graph.addEdge(8, 6, 14)
    graph.addEdge(8, 7, 6)

    pso = PSO(graph, iterations=1000, size_population=100, betaF=1, alfa=0.9)
    pso.run()
    pso.showsParticles()

    print('Лучший путь: %s | стоимость: %d\n' % (pso.getGBest().getPBest(), pso.getGBest().getCostPBest()))