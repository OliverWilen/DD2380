#!/usr/bin/env python3
import fileinput
import sys

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

def deltaAlgorithm(A, B, pi, O):
    delta = []
    deltaidx = []
    temp = []
    for i in range(0, len(A)):
        temp.append(pi[0][i]*B[i][O[0]])

    delta.append(temp)

    for o in range(1, len(O)):
        delta.append([])
        deltaidx.append([])
        for i in range(0, len(A)):
            step = []
            for j in range(0, len(A)):
                step.append(A[j][i]*delta[o-1][j]*B[i][o])

            maxvalue = max(step)    
            delta[o].append(maxvalue)
            deltaidx[o-1].append(step.index(maxvalue))

    sequence = []
    sequence.append(delta[len(O)-1].index(max(delta[len(O)-1])))
    print(delta)
    print(deltaidx)

    for t in range(1, len(O)):
        sequence.append(deltaidx.pop()[sequence[t-1]])

    return sequence
        

A,B,pi,O = parseIn(sys.stdin)

print(deltaAlgorithm(A, B, pi, O))

