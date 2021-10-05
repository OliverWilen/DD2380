#!/usr/bin/env python3
import math
import fileinput
import sys


def parseIn(input):
    A = makeMatrix(input.readline())
    B = makeMatrix(input.readline())
    pi = makeMatrix(input.readline())
    return A,B,pi

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

def matrixMul(A, B):
    result = []
    for row in A:
        resultCol = []
        for col in list(zip(*B)):
            products = [a * b for a, b in zip(row, col)]
            resultCol.append(sum(products))
        result.append(resultCol)
    return result


def nextTransitionObservation(A,B,pi):
    return matrixMul(matrixMul(pi, A), B) 

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
