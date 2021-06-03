import numpy as np

def find_coeff(x_data,y_data,n):
    A = np.zeros([n+1,n+1])
    sx = np.zeros(2*n + 1)
    b = np.zeros(n+1)
    tmp = np.ones(len(x_data))
    for i in range(2*n):
        tmp = tmp*x_data
        sx[i+1] =sum(tmp)
    sx[0] = len(x_data)
    tmp = y_data
    for i in range(1,n+2):
        b[-i] = sum(tmp)
        tmp = tmp*x_data
    for i in range(n+1):
        for j in range(1,n+2):
            A[i][j-1] = sx[-i-j]
    return np.linalg.inv(A).dot(b)

def eval_poly(c,x):
    tmp = np.zeros(len(x))
    for i in c:
        tmp = tmp*x + i
    return tmp

