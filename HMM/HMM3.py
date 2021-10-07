#!/usr/bin/env python3
import fileinput
import sys
import math

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

#alpha-pass algorithm, runs over observations 0 -> t_end
def forwardAlgorithm(A, B, pi, O, t_end):
    templist = []
    for i in range(0, len(A)):
        templist.append(pi[0][i]*B[i][O[0]])
    alpha = templist
    
    for t in range(1, t_end):
        templist = []
        for i in range(0, len(A)):
            s = 0
            for j in range(0, len(A)):
                s += alpha[j]*A[j][i]
            
            templist.append(s*B[i][O[t]])
            
        alpha = templist
    return alpha
 
#beta-pass algorithm, runs over observations T -> t_start        
def backwardAlgorithm(A, B, O, t_start):
    templist = []
    for i in range(0, len(A)):
        templist.append(1.0)

    beta = templist

    for t in range(1, t_start):
        templist = []
        for i in range(0, len(A)):
            s = 0
            for j in range(0, len(A)):
                s += beta[j] * B[j][O[len(O)-t]] * A[i][j]
            
            templist.append(s)
            
        beta = templist
    return beta

#gamma function, marginalizes di-gamma over states so that parameter j can be omitted.
def gamma(t, i, A, B, pi, O:
    g = 0
    for j in range(0, len(A)):
        g += di_gamma(t, i, j, A, B, pi, O)
    return g

#di-gamma function, returns di-gamma evaluation for a specific state (i,j,t)
def di_gamma(t, i, j, A, B, pi, O):
    dg = forwardAlgorithm(A, B, pi, O, t) * A[i][j] * B[j][O[t+1]] * backwardAlgorithm(A, B, O, t+1)
    return dg

#Runs the overall structure of the Baum-Welch algorithm.
def Baum_Welch(A, B, pi, O):
    maxIters = 100
    iters = 0
    oldlogProb = -math.inf
    N = len(A)
    T = len(O)

    while(True):
        #re-estimate pi
        for i in range(0, N):
            pi[0][i] = gamma(0, i, A, B, pi)

        #re-estimate A
        for i in range(0, N):
            denom = 0
            for t in range(0, T-1):
                denom += gamma(t, i, A, B, pi)
            
            for j in range(j, N):
                numer = 0
                for t in range(0, T-1):
                    numer += di_gamma(t, i, j, A, B, pi)
            
                A[i][j] = numer/demon

        #re-estimate B
        for i in range(0, N):
            denom = 0
            for t in range(0, T-1):
                denom += gamma(t, i, A, B, pi)
            
            for j in range(j, N):
                numer = 0
                for t in range(0, T-1):
                    if(O[t] == j):
                        numer += gamma(t, i, A, B, pi)
            
                B[i][j] = numer/demon

        logprob = 0
        for t in range(0, T):
            logprob -= sum(forwardAlgorithm(A, B, pi, O, t))

        if (iters < maxIters and logprob > oldlogProb):
                oldlogProb = logprob
        else:
            return[A, B]

    return ""

A,B,pi,O = parseIn(sys.stdin)
x = backwardAlgorithm(A, B, pi, O)
print(x)

