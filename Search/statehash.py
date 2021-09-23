#!/usr/bin/env python3
import math

from fishing_game_core.game_tree import State

class StateHash:
    def __init__(self):
        #Internal dict (hash map). Keys are state properties converted to a long string. Value is the associated heuristic evaluation of the state.
        self.hashmap = {}

    #Method to convert state properties into hashable string and enter into hashmap.
    def add(self, state, heuristic):
        statekey = self.getStateKey(state)
        self.hashmap[statekey] = heuristic
        """
        #get list of transpositionally related keys
        t_keys = self.getTransposedKeys(state)
        for k in t_keys:
            #store heuristic using state keys in hashmap
            print(k)
            self.hashmap[k] = heuristic
        #do the same for opponent
        state.set_player(1-state.player)
        t_keys_opponent = self.getTransposedKeys(state)
        for k in t_keys_opponent:
            #store negated heuristic using state keys in hashmap
            print(k)
            self.hashmap[k] = -heuristic
        """
        

    #Method to retrieve heuristic value of previously added state.
    def get(self, state):
        #get state key
        statekey = self.getStateKey(state)
        #see if value exists and return, else return string "empty"
        if statekey in self.hashmap:
            return self.hashmap[statekey]
        else:
            return "empty"

    #utility function which creates a key
    def getStateKey(self, state):
        #convert state attributes into strings:
        #player
        player = str(state.player)
        #player_scores
        scores = str(state.player_scores[0]).zfill(4)+str(state.player_scores[1]).zfill(4)      #assumes no more than 9999 score achieveable by either player.
        #player_caught
        caught = str(state.player_caught[0]).zfill(2)+str(state.player_caught[1]).zfill(2)      #assumes no more than 100 fish, 0-99 index.
        #hook_positions
        hooks = str(state.hook_positions[0][0]).zfill(2)+str(state.hook_positions[0][1]).zfill(2)+str(state.hook_positions[1][0]).zfill(2)+str(state.hook_positions[1][1]).zfill(2)
        #fish_positions
        fish = ""
        positions = state.fish_positions
        for key in positions:
            fish= fish + str(positions[key][0]).zfill(2) + str(positions[key][1]).zfill(2)
        #fish_scores
        fish_values = ""
        for key in positions:
            fish_values=fish_values + str(state.fish_scores[key]).zfill(2)
        #compile strings into one key
        statekey = player+scores+caught+hooks+fish+fish_values
        return statekey

    """
    #Returns list of keys for transposed states.
    #only returns symmetrical keys, intention is to call same method for opposite player and create similar list for those states.
    #this method only cares for states which are identical except offset by the same amount along the x axis.
    #Mirrored states seem to be unlikely to occur, especially in close succession to previous states.
    def getTransposedKeys(self, input_state):
        state = input_state
        transposedKeys = []
        x1,y1 = state.hook_positions[0][0],state.hook_positions[0][1]
        x2,y2 = state.hook_positions[1][0],state.hook_positions[1][1]
        for i in range (0,20):
            #increase x-coordinate for player hooks
            state.set_hook_positions([(x1+i)%20,y1,(x2+i)%20,y2])
            #increase x-coordinate for all fish
            for fish in state.fish_positions:
                x,y = input_state.fish_positions[fish][0],input_state.fish_positions[fish][1] 
                state.set_fish_positions(fish,((x+i)%20,y))
            transposedKeys.append(self.getStateKey(state))
        return transposedKeys
    """