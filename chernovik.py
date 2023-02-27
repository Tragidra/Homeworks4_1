from chernovik2 import *
from chernovik3 import print_history_table


if __name__ == '__main__':
    objective_function = ('min', '1x_1 + 1x_2')
    constraints = ['4x_1 - 4x_2 <= 7', '4x_1 - 1x_2 <= 8', '-2x_1 + 4x_2 >= 7']
    num_vars = 2
    gomory_vals, gomory_solution, gomory_history, basic_vars_history = gomory_solve(
        num_vars,
        constraints,
        objective_function
    )
    print('Gomory method steps:')
    print_history_table(gomory_history, basic_vars_history, gomory_solution)