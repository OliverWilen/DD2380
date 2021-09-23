#!/usr/bin/env python3
import random
import math
from time import time

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR

class Minimax:
    def __init__(self):
        self.time_overhead = 0.03
        self.time_threshold = 75*1e-3 - self.time_overhead
        self.time_start = None
    
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
    def invSquareDist(self, tupleA, tupleB):
        if(tupleA == tupleB):
            return 0
        x1,y1 = tupleA
        x2,y2 = tupleB
        return 1/(math.sqrt(math.pow(x2-x1,2) + math.pow(y2-y1,2)))

    def minimaxAB(self, node, depth, alpha, beta, player):
        a = alpha
        b = beta
        v = 0.0

        if (self.checktimeout()):
            return v

        children = node.compute_and_get_children()
        if (depth==0 or len(children)==0):
            return self.heuristic(player,node.state)

        if player==0:           #player A
            v = -(math.inf)
            for child in children:
                v = max(v, self.minimaxAB(child,depth-1,a,b,1))
                a = max(a,v)
                if b<=a:
                    break       #beta prune
                if (self.checktimeout()):
                    return v

        else:                   #player B
            v = math.inf
            for child in children:
                v = min(v, self.minimaxAB(child,depth-1,a,b,0))
                b = min(b,v)
                if b<=a:
                    break       #alpha prune
                if (self.checktimeout()):
                    return v

        return v

    def IDDFS(self, children_nodes, time_start):
        self.time_start = time_start
        best_node = children_nodes[0]
        for depth in range(2, 100):
            if (self.checktimeout()):
                return best_node

            best_value = -math.inf

            for child in children_nodes:
                if(depth%2 == 1):
                    value = -self.minimaxAB(child, depth, -math.inf, math.inf, 0)
                else:
                    value = self.minimaxAB(child, depth, -math.inf, math.inf, 0)

                if (self.checktimeout()):
                    return best_node

                if (value > best_value):  
                    best_value = value
                    temp_node = child

            best_node = temp_node 

        return best_node

    def checktimeout(self):
        if(time() - self.time_start <= self.time_threshold):
            return False
        else:
            return True
