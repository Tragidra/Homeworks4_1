import random
import numpy as np
import math
import time
n=9
NFT0=0.4
lam=0.001
cnt=10000
t=60
cij=np.array([[0,34,16,38,21,8,11,26,14],
[34,0,33,25,22,30,24,31,20],
[16,33,0,25,31,8,13,39,20],
[38,25,25,0,39,30,27,49,30],
[21,22,31,39,0,24,18,10,11],
[8,30,8,30,24,0,6,31,13],
[11,24,13,27,18,6,0,27,7],
[26,31,39,49,10,31,27,0,21],
[14,20,20,30,11,13,7,21,0]])
ei=np.array([0,41,88,132,24,0,0,3,0,112,194,0,69,0,146,105,117,0,130,0,174])
li=np.array([345,183,247,275,137,101,76,155,140,255,308,93,202,106,289,263,264,104,233,122,308])
li0=np.array([345,183,247,275,137,101,76,155,140,255,308,93,202,106,289,263,264,104,233,122,308])
li0.sort()
Sx=[]
for j in range(n):
    for k in range(n):
        if(li[k]==li0[j] and k not in Sx):
            Sx.append(k)
Sx.remove(0)
A=[]
c=0
A.append(cij[0,Sx[0]])
for q in range(n-2 ):
    A.append(max(A[q],ei[Sx[q]])+cij[Sx[q],Sx[q+1]])
    if(A[q+1]<=li[Sx[q+1]]):
        c=c+1
if(c<19):
    print('initial infeasible solution: {}'.format(Sx))
# swapping elements to see for feasibility
B=list(Sx)


for u in range(n-1):
    for v in range(n-1):
        B[u],B[v]=B[v],B[u]
        M=[]
        M.append(cij[0,B[0]])
        d=0
        for q in range(n-2):
            M.append(max(M[q],ei[B[q]])+cij[B[q],B[q+1]])
            if(M[q+1]<=li[B[q+1]]):
                d=d+1
        if(d<19):
            funct=0
            funct=M[-1]+cij[B[-1],0]+((19-d)*(1+(lam*t))/(NFT0))
            if(funct<cnt):
                cnt=funct
                O=list(B)
                pi0=list(O)
        if(d==19):
            Sl=list(B)
            pi0=list(Sl)
        B=list(Sx)

#initial random solution
#initial random infeasible solutions
print('Initial random feasible solution: {}'.format(pi0))