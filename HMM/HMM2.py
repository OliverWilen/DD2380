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

#TODO!! use log values to prevent underflow in floats! :)
def deltaAlgorithm(A, B, pi, O):
    N = len(A)
    K = len(B)
    T = len(O)
    delta = []      #delta matrix; each value represents probability that state was reached if optimal path was used. index 0 represents time depth, index 1 represents state.
    deltaidx = []   #delta index matrix; each value corresponds to a state in delta, and represents the parent state which most likely lead to this state.
    temp = []       
    #calculate first iteration of delta 
    for i in range(0, N):
        temp.append(pi[0][i]*B[i][O[0]])

    delta.append(temp)

    #calculate rest of delta matrix
    #for each observation in the sequence:
    for o in range(1, T):
        delta.append([])
        deltaidx.append([])
        #for each state in this delta matrix row:
        for i in range(0, N):
            possibleEntries = []
            #for each possible path to state i:
            for j in range(0, N):
                possibleDelta = A[j][i]*delta[o-1][j]*B[i][O[o]]
                possibleEntries.append(possibleDelta)
            #only add the greatest value to delta, also add the associated parent state in deltaidx.
            maxvalue = max(possibleEntries)    
            delta[o].append(maxvalue)
            deltaidx[o-1].append(possibleEntries.index(maxvalue))

    #calculating the optimal path
    #start the sequence with the most probable state in time step T, then traverse parent nodes backwards from that point.
    sequence = []
    sequence.append(delta[len(O)-1].index(max(delta[len(O)-1])))
    for t in range(1, T):
        sequence.append(deltaidx.pop()[sequence[t-1]])
    sequence.reverse()
    return vectorToString(sequence)
    
#formatting output       
def vectorToString(vector):
    string = ""
    for value in vector:
        string += " " + str(value)
    return string

A,B,pi,O = parseIn(sys.stdin)

print(deltaAlgorithm(A, B, pi, O))

