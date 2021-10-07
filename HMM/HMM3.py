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

#alpha-pass algorithm
def forwardAlgorithm(A, B, pi, O):
    #calculate initial time step
    templist = []
    alpha = []
    c = [0]
    for i in range(0, len(A)):
        a = pi[0][i]*B[i][O[0]]
        c[0] += a
        templist.append(a)
    #scale values with norm. facor.
    c[0] = 1/c[0]
    for i in range(0, len(A)):
        templist[i] = templist[i]*c[0]
    alpha.append(templist)
    
    #calculate succeeding time steps until O
    for t in range(1, len(O)):
        templist = []
        c.append(0)
        for i in range(0, len(A)):
            s = 0
            for j in range(0, len(A)):
                s += alpha[t-1][j]*A[j][i]
            a = s*B[i][O[t]]
            c[t] += a
            templist.append(a)
        #scale values at current time step with norm. factor
        c[t] = 1/c[t]
        for i in range(0, len(A)):
            templist[i] = templist[i]*c[t]
        alpha.append(templist)
    return alpha, c
 
#beta-pass algorithm      
def backwardAlgorithm(A, B, O, c):
    templist = []
    beta = []

    for i in range(0, len(A)):
        templist.append(c[-1])

    beta.append(templist)

    for t in range(len(O)-2, -1, -1):  
        templist = []
        for i in range(0, len(A)):
            s = 0
            for j in range(0, len(A)):
                s += beta[-1][j] * B[j][O[t+1]] * A[i][j]
            
            templist.append(s * c[t])
            
        beta.append(templist)

    beta.reverse()
    return beta

#gamma function, marginalizes di-gamma over states so that parameter j can be omitted.
def gamma(t, i, A, B, pi, O, alpha, beta):
    g = 0
    if (t == len(O) - 1):
        return alpha[t][i]

    for j in range(0, len(A)):
        g += di_gamma(t, i, j, A, B, pi, O, alpha, beta)
    return g

#di-gamma function, returns di-gamma evaluation for a specific state (i,j,t)
def di_gamma(t, i, j, A, B, pi, O, alpha, beta):
    dg = alpha[t][i] * A[i][j] * B[j][O[t+1]] * beta[t+1][j]
    return dg

#Runs the overall structure of the Baum-Welch algorithm.
def Baum_Welch(A, B, pi, O):
    maxIters = 1000000
    iters = 0
    oldlogProb = -math.inf
    N = len(A)
    T = len(O)

    alpha, c = forwardAlgorithm(A, B, pi, O)
    beta = backwardAlgorithm(A, B, O, c)


    while(True):
        #re-estimate pi
        for i in range(0, N):
            pi[0][i] = gamma(0, i, A, B, pi, O, alpha, beta)

        #re-estimate A
        for i in range(0, N):
            denom = 0
            for t in range(0, T-1):
                denom += gamma(t, i, A, B, pi, O, alpha, beta)
            
            for j in range(0, N):
                numer = 0
                for t in range(0, T-1):
                    numer += di_gamma(t, i, j, A, B, pi, O, alpha, beta)
            
                A[i][j] = numer/denom

        #re-estimate B
        for i in range(0, N):
            denom = 0
            for t in range(0, T):
                denom += gamma(t, i, A, B, pi, O, alpha, beta)
            
            for j in range(j, N):
                numer = 0
                for t in range(0, T):
                    if(O[t] == j):
                        numer += gamma(t, i, A, B, pi, O, alpha, beta)
            
                B[i][j] = numer/denom


        #Calculate the log of the observations with the new estimations
        alpha, c = forwardAlgorithm(A, B, pi, O)
        beta = backwardAlgorithm(A, B, O, c)
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

