#!/usr/bin/env python3
import random
import math

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR


class PlayerControllerHuman(PlayerController):
    def player_loop(self):
        """
        Function that generates the loop of the game. In each iteration
        the human plays through the keyboard and send
        this to the game through the sender. Then it receives an
        update of the game through receiver, with this it computes the
        next movement.
        :return:
        """

        while True:
            # send message to game that you are ready
            msg = self.receiver()
            if msg["game_over"]:
                return


class PlayerControllerMinimax(PlayerController):

    def __init__(self):
        super(PlayerControllerMinimax, self).__init__()

    def player_loop(self):
        """
        Main loop for the minimax next move search.
        :return:
        """

        # Generate game tree object
        first_msg = self.receiver()
        # Initialize your minimax model
        model = self.initialize_model(initial_data=first_msg)

        while True:
            msg = self.receiver()

            # Create the root node of the game tree
            node = Node(message=msg, player=0)

            # Possible next moves: "stay", "left", "right", "up", "down"
            best_move = self.search_best_next_move(
                model=model, initial_tree_node=node)

            # Execute next action
            self.sender({"action": best_move, "search_time": None})

    def initialize_model(self, initial_data):
        """
        Initialize your minimax model 
        :param initial_data: Game data for initializing minimax model
        :type initial_data: dict
        :return: Minimax model
        :rtype: object

        Sample initial data:
        { 'fish0': {'score': 11, 'type': 3}, 
          'fish1': {'score': 2, 'type': 1}, 
          ...
          'fish5': {'score': -10, 'type': 4},
          'game_over': False }

        Please note that the number of fishes and their types is not fixed between test cases.
        """
        # EDIT THIS METHOD TO RETURN A MINIMAX MODEL ###
        return None

    #basic heuristic model. sums up score at given state.
    #def heuristic(self, player, state):
    #    a,b = state.get_player_scores
    #    if player==0:
    #        return a-b
    #    else:
    #        return b-a


    #Heuristic evaluation function v2.0, sums player score and sums up weighted distance to fish. 
    #Takes into account both overall score and how good the hooks are positioned for each player.
    #When comparing different states, if the score favors opponent identically, this heuristic will give a better heuristic score to the state with better hook position (i.e. less negative).
    #Should uphold zero-sum game requirement.
    #TODO: Account for caught fish. currently heuristic includes hooked fish into positional calculation for opponent!
    def heuristic(self, player, state):
        hookA = state.get_hook_positions()[0]
        hookB = state.get_hook_positions()[1]
        scoreA = float(state.get_player_scores()[0])
        scoreB = float(state.get_player_scores()[1])
        fish_positions = state.get_fish_positions() 
        hA,hB = 0.0,0.0     #contains positional value for player A and B.

        #For every fish in the sea, multiply fish value by the inverse square distance to player hooks.
        #More valuable fish can give much higher values if you are close.
        for x in fish_positions:
            hA += self.invSquareDist(hookA,fish_positions[x])*state.get_fish_scores()[x]
            hB += self.invSquareDist(hookB,fish_positions[x])*state.get_fish_scores()[x]

        #Calculates the overall heuristic evaluation of the state for each player. Score plus positional value.
        stateValA = scoreA-scoreB+hA-hB
        stateValB = scoreB-scoreA+hB-hA

        #Returns highest value between A and B, but negates it if the highest value was for the other player.
        #Should uphold zero-sum requirement that h(A,s)+h(B,s) = 0.
        return max(stateValA,stateValB)*(float(1-player)*self.fltComp(stateValA,stateValB) + float(player)*self.fltComp(stateValB,stateValA))
        

    #Helper function to calculate inverse square distance between sets of coordinates.
    def invSquareDist(this, tupleA, tupleB):
        if(tupleA == tupleB):
            return 0
        x1,y1 = tupleA
        x2,y2 = tupleB
        return 1/(math.sqrt(math.pow(x2-x1,2) + math.pow(y2-y1,2)))

    #Comparator for floats.
    def fltComp(this,A,B):
        if A==B:
            return 0
        if A>B:
            return 1
        else:
            return -1

    def minimaxAB(self, node, depth, alpha, beta, player):
        a = alpha
        b = beta
        v = 0.0

        children = node.compute_and_get_children()
        if (depth==0 or len(children)==0):
            return self.heuristic(player,node.state)

        if player==0:           #player A
            v = -float(math.inf)
            for child in children:
                v = float(max(v, self.minimaxAB(child,depth-1,a,b,1)))
                a = float(max(a,v))
                if float(b)<=a:
                    break       #beta prune

        else:                   #player B
            v = float(math.inf)
            for child in children:
                v = float(min(v, self.minimaxAB(child,depth-1,a,b,0)))
                b = float(min(b,v))
                if b<=float(a):
                    break       #alpha prune

        return v

    def search_best_next_move(self, model, initial_tree_node):
        """
        Use your minimax model to find best possible next move for player 0 (green boat)
        :param model: Minimax model
        :type model: object
        :param initial_tree_node: Initial game tree node 
        :type initial_tree_node: game_tree.Node 
            (see the Node class in game_tree.py for more information!)
        :return: either "stay", "left", "right", "up" or "down"
        :rtype: str
        """

        # EDIT THIS METHOD TO RETURN BEST NEXT POSSIBLE MODE FROM MINIMAX MODEL ###
        pl = 0
        state = initial_tree_node.state
        h = self.heuristic(pl,state)

        children_nodes = initial_tree_node.compute_and_get_children()
        best_v = -float(math.inf)
        best_node = children_nodes[0]
        for child in children_nodes:
            v = self.minimaxAB(child,2,0,0,0)
            #print("child minimax value: " + str(v))
            if v>best_v:
                best_v = v
                best_node = child

        #print("best node minimax value: " + str(v))

        next_move = ACTION_TO_STR[best_node.move]
        #print("recommended next move: " + next_move)
        return next_move
        
        #random_move = random.randrange(5)
        #return ACTION_TO_STR[random_move]