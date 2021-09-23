#!/usr/bin/env python3
import random
import math
import time

from statehash import StateHash
from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR

class Minimax:

    def __init__(self):
        self.tt = StateHash()

    #Heuristic evaluation function v2.0, sums player score and sums up weighted distance to fish. 
    #Takes into account both overall score and how good the hooks are positioned for each player.
    #When comparing different states, if the score favors opponent identically, this heuristic will give a better heuristic score to the state with better hook position (i.e. less negative).
    #Should uphold zero-sum game requirement.
    #TODO: Account for caught fish. currently heuristic includes hooked fish into positional calculation for opponent!
    def heuristic(self, player, state):
        hookA = state.get_hook_positions()[0]
        hookB = state.get_hook_positions()[1]
        scoreA = state.get_player_scores()[0]
        scoreB = state.get_player_scores()[1]
        fish_positions = state.get_fish_positions() 
        hA,hB = 0.0,0.0     #contains positional value for player A and B.

        #For every fish in the sea, multiply fish value by the inverse square distance to player hooks.
        #More valuable fish can give much higher values if you are close.
        for x in fish_positions:
            hA += self.invSquareDist(hookA,fish_positions[x])*state.get_fish_scores()[x]
            hB += self.invSquareDist(hookB,fish_positions[x])*state.get_fish_scores()[x]
        #Calculates the overall heuristic evaluation of the state for each player. Score plus positional value.
        stateVal = scoreA-scoreB+hA-hB

        #Should uphold zero-sum requirement that h(A,s)+h(B,s) = 0.
        return ((1-player)*stateVal - player*stateVal)
        

    #Helper function to calculate inverse square distance between sets of coordinates.
    def invSquareDist(this, tupleA, tupleB):
        #check equality
        if(tupleA == tupleB):
            return 0
        x1,y1 = tupleA
        x2,y2 = tupleB
        #adjust coordinates to account for "horizontal roll". I.e. if x1 = 0 and x2 = 19, the distance is 1, not 19.
        #if there's a distance greater or equal to 10 between the two points, they are closer to each other by going through the world border than trough the open field.
        if x1+10<x2:
            x2 = x2-20
        else:
            if x2+10<x1:
                x1 = x1-20

        return 1/(math.sqrt(math.pow(x2-x1,2) + math.pow(y2-y1,2)))

    def minimaxAB(self, node, depth, alpha, beta, player):
        a = alpha
        b = beta
        v = 0.0

        children = node.compute_and_get_children()
        if (depth==0 or len(children)==0):
            #check transposition table if state has been visited
            h = self.tt.get(node.state)
            if h=="empty":
                h = self.heuristic(player,node.state)
                self.tt.add(node.state,h)
            return h

        if player==0:           #player A
            v = -(math.inf)
            for child in children:
                v = max(v, self.minimaxAB(child,depth-1,a,b,1))
                a = max(a,v)
                if b<=a:
                    break       #beta prune

        else:                   #player B
            v = math.inf
            for child in children:
                v = min(v, self.minimaxAB(child,depth-1,a,b,0))
                b = min(b,v)
                if b<=a:
                    break       #alpha prune

        return v