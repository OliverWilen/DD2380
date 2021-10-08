#!/usr/bin/env python3
import fileinput
import sys
import math

from HMM3 import gamma

"""
Takes the input string and converst the first three lines to matrices.
"""
def parseIn(input):
    A = makeMatrix(input.readline())
    B = makeMatrix(input.readline())
    pi = makeMatrix(input.readline())
    O = list(map(int, input.readline().split()[1:]))
    return A,B,pi,O
"""
Takes a string of numbers and coverts it into a two dimentional array.
The first and second numbers of the string describe the size of the matrix
"""
def makeMatrix(line):
    line = list(map(float, line.split()))
    height = int(line.pop(0))
    width = int(line.pop(0))
    matrix = []
    for i in range(0,height):
        row = []
        for j in range(0,width):
            row.append(line.pop(0))
        matrix.append(row)
    return matrix

"""
Matrix multiplication usign two dimentional arrays
"""
def matrixMul(A, B):
    result = []
    for row in A:
        resultCol = []
        for col in list(zip(*B)):
            products = [a * b for a, b in zip(row, col)]
            resultCol.append(sum(products))
        result.append(resultCol)
    return result

"""
Calculates the next transition observation vector based on a previous state probability
vector (pi), transition matrix (A) and emission matrix(B)
"""
def nextTransitionObservation(A,B,pi):
    return matrixMul(matrixMul(pi, A), B) 

"""
Converts a matrix represented as a two dimentional array into a string.
The two first numbers define the size of the matrix
"""
def matrixToString(matrix):
    string = ""
    string += str(len(matrix)) + " "
    string += str(len(matrix[0]))
    for row in matrix: 
        for value in row:
            string += " " + str(value)
    return string

#Runs the overall structure of the Baum-Welch algorithm.
def Baum_Welch(A, B, pi, O):
    maxIters = 1000000
    iters = 0
    oldlogProb = -math.inf
    N = len(A)
    M = len(B[0])
    T = len(O)

    while(True):
#-----------------------#initializations#-----------------------#        
        #alpha matrix
        alpha = [[0 for i in range(N)] for t in range(T)]
        #beta matrix
        beta = [[0 for i in range(N)] for t in range(T)]
        #alpha scaling values
        c = [0] * T
        #gamma matrix
        gamma = [[0 for i in range(N)] for t in range(T)]
        #di gamma matrix
        di_gamma = [[[0 for j in range(M)] for i in range(N)] for t in range(T)]
#--------------------------#alpha pass#--------------------------#
        #initial time step
        c.append(0)
        alpha.append([])
        for i in range (0, N):
            alpha[0].append(pi[i]*B[i][O[0]])
            c[0] += alpha[0][i]
        #scale alpha
        c[0] = 1/c[0]
        for value in alpha[0]:
            value *= c[0]

        #general case
        for t in range(1, T):
            c[t] = 0
            alpha.append([])
            for i in range(0, N):
                alpha[t].append([])
                alpha_val = 0
                for j in range(0, N):
                    alpha_val += alpha[t-1][j]*A[j][i]
                alpha[t][i] = alpha_val*B[i][O[t]]
                c[t] += alpha[t][i]
            #scale alpha
            c[t] = 1/c[t]
            for value in alpha[t]:
                value *= c[t]
#---------------------------#beta pass#--------------------------#
        #scale initial value
        for i in range(0, N):
            beta[0][i] = c[0]

        #general case
        for t in range(T-1, -1):
            for i in range(0, N):
                bt = 0
                for j in range(0, N):
                    bt += A[i][j] * B[j][O[t]] * beta[t+1][j]
                bt *= c[t]
                beta[t][i] = bt
        
#-----------------------#di-gamma and gamma#---------------------#       
        #Compude gamma and di gamma
        for t in range(0, T-1):
            for i in range(0, N):
                for j in range(0, N):
                    di_gamma[t][i][j] = alpha[t][i]*A[i][j]*B[j][O[t+1]]*beta[t+1][j]
                    gamma[t][i] += di_gamma

        #Special case for gamma[t-1]
        for i in range(0, N):
            gamma[-1][i] = alpha[-1][i]
#--------------------#estimate new parameters#-------------------#
        #re-estimate pi
        for i in range(0, N):
            pi[0][i] = gamma[0][i]

        #re-estimate A
        for i in range(0, N):
            denom = 0
            for t in range(0, T-1):
                denom += gamma[t][i]
            
            for j in range(0, N):
                numer = 0
                for t in range(0, T-1):
                    numer += di_gamma[t][i][j]
            
                A[i][j] = numer/denom

        #re-estimate B
        for i in range(0, N):
            denom = 0
            for t in range(0, T):
                denom += gamma[t][i]
            
            for j in range(j, N):
                numer = 0
                for t in range(0, T):
                    if(O[t] == j):
                        numer += gamma[t][i]
            
                B[i][j] = numer/denom


        #Calculate the log of the observations with the new estimations
        logprob = -sum([math.log(1/ct, 10) for ct in c])
        iters += 1
        
        #Stop looping if the probabilities coverge or maximum iterations is reached
        if (iters < maxIters and logprob > oldlogProb):
                oldlogProb = logprob
        else:
            return A, B

A,B,pi,O = parseIn(sys.stdin)
resultA, resultB = Baum_Welch(A, B, pi, O)

print(matrixToString(resultA))
print(matrixToString(resultB))