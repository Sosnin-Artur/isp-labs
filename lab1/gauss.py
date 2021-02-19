#!/usr/bin/env python3.8
import numpy as np
import sys

def gauss(A):
    n = len(A)	
    for i in range(1, n): 
        k = 0      
        while ((A[i][i] == 0 or A[k][k] == 0) and k != i):
            A[i], A[k] = np.copy(A[k]), np.copy(A[i])            
            k += 1
            if (k == n):
                return None            

    for i in range(0, n):       
        for k in range(i + 1, n):
            c = A[k][i] / A[i][i]
            A[k] -= c * A[i]

    x = [0 for i in range(n)]
    for i in range(n - 1, -1, -1):
        x[i] = A[i][n] / A[i][i]
        for k in range(i - 1, -1, -1):
            A[k][n] -= A[k][i] * x[i]
    return x

file = open(sys.argv[1])
data = file.read().split();
data = [int(i) for i in data]
shape = data[:2]
A = np.zeros((shape[0], shape[1]))
for i in range(0, shape[0]):
    for j in range(0, shape[1]):
        A[i][j] = (data[i * shape[0] + j + 2])
b = np.zeros(shape[1])
for i in range(0, shape[0]):
    b[i] = (data[i + shape[0] * shape[1] + 2])
print(gauss(np.column_stack((A, b))))
