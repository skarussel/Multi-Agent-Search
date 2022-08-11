from copy import deepcopy


class Node:
    def __init__(self, val, paths=[]) -> None:
        
        """
        state: current state
        path: actions that lead from start state to current state
        cost: accumulated cost along path
        h: heuristic value
        insert_time: integer that specifies insert time 
        """

        self.value = val
        self.paths = paths 
        

    def copy(self):
        return deepcopy(self)

    def set_insert_time(self, time):
        self.insert_time=time

    






    