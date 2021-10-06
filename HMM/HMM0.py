#!/usr/bin/env python3
import fileinput
import sys

"""
#Parses the input from stdin and sends each line to be converted into two dimentional arrays
"""
def parseIn(input):
    A = makeMatrix(input.readline())
    B = makeMatrix(input.readline())
    pi = makeMatrix(input.readline())
    return A,B,pi
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



A,B,pi = parseIn(sys.stdin)
next = nextTransitionObservation(A,B,pi)
print(matrixToString(next))
