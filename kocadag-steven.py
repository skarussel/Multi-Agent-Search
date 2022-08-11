import sys 
import re

import numpy as np
from node import Node
from copy import deepcopy


actions = ["left", "right", "down", "up", "stop", "suck"]
max_cleaner = 0
calls = 0
n_actions = 0

def find_cleaners(state):
    """
    input: state
    output: x,y, coordinates of cleaner
    """

    cleaners = [None]*(max_cleaner+1)

    for i in range(len(state)):
        for j in range(len(state[i])):
            field = state[i][j]
            for char in field:
                if (char.isdigit()):
                    cleaners[int(char)]=[i,j]

    return cleaners

def init_cleaners(state):
    agents = []

    for i in range(len(state)):
        for j in range(len(state[i])):
            field = state[i][j]
            if (field.isdigit()):
                agents.append(int(field))
    agents.sort() 
    return agents

def append_to_field(field, agent):
    if (field==" "):
            return str(agent)
    else:
        return field + str(agent)

def remove_from_field(field, char):
    if (field==str(char)):
        return " "
    else:
        return field.replace(str(char), "")

def suckcess(field):
    if ("." in field):
        return True




def count_enemies(state):

    max = 0
    for row in state:
        for field in row:
            if field.isdigit():
                if max<int(field):
                    max=int(field)
    return max

def count_dirts(state):
    res = 0
    for row in state:
        for field in row:
            if "." in field:
                res+=1
    return res



def is_terminal(state, action_counter):
    if (action_counter==n_actions):
        return True 
    for l in state:
        if ([x for x in l if "0" in x and sum(c.isdigit() for c in x)>1]):
            return True  
    for l in state:
    # check for dirt 
        if any(re.findall(r'\.+',s) for s in l):
            return False
    return True
     
def utility(state, prev_action, sucked_dirt):
    global calls
    calls +=1
    sucked_dirt_enemies = num_dirts-sucked_dirt-count_dirts(state)
    res = Node(sucked_dirt-sucked_dirt_enemies, prev_action)

 
    # -100 if vacuum cleaner is on same field as enemy
    for l in state:
        if ([x for x in l if "0" in x and sum(c.isdigit() for c in x)>1]):
            return Node(-100, prev_action)
    
    
    return res
    

def split(string):
    """
    input: string 
    output: split word into char
    """
    return [char for char in string]

def is_dirt(element):
    """
    input: one field in nxm grid
    output: number of dirt if dirt is on field, None else
    """
    
    dirt = re.findall(r'\.+',element)
    if (dirt):
        return True
    else: 
        return False

def printstate(state):
    final = ''
    for row in state:
        final+=(' '.join(map(str, row))+"\n")
    print(final)

def perform_action(s, agent, action, sucked_dirt):
    """
    input: state,agent,action
    output: node that contains state after performing action
    """
    state = deepcopy(s)
    cleaners = find_cleaners(state)
    x,y = cleaners[agent]
    
    x_old, y_old = x,y
    if (action=="up"):
        x-=1
    elif (action=="down"):
        x+=1
    elif (action=="left"):
        y-=1
    elif (action=="right"):
        y+=1
    
    if (x>X_SHAPE or x<0 or y>Y_SHAPE or y<0 or state[x][y]=='x'):
        x,y=x_old,y_old

    old_field = state[x_old][y_old]
    if (x_old!=x or y_old!=y):
        new_field = state[x][y]
        state[x_old][y_old] = remove_from_field(old_field, agent)
        state[x][y] = append_to_field(new_field, agent)
    elif (action=="suck"):
        if (agent==0 and suckcess(old_field)):
            sucked_dirt+=1
        state[x][y] = remove_from_field(old_field, ".")
    
    return state, sucked_dirt 


def abMax(state,action_counter, prev_action, alpha ,beta, sucked_dirt):
    if(is_terminal(state, action_counter)):
        return utility(state, prev_action, sucked_dirt)
    
    best_node = None 
    val = -np.Infinity
    states = []
    next_agent = agents[1]
    

    for a in actions:
        s, s_dirt = perform_action(state,0 ,a, sucked_dirt)
        if (s not in states or a in ["suck"]):
            states.append(s)
            if (next_agent%2==0):
                # if agents is even it plays random
                result = randValue(s, 1, action_counter+1, prev_action+[a], s_dirt)
            else:
                # if agents is odd it plays optimal
                result = abMin(s, 1, action_counter+1, prev_action+[a], alpha, beta, s_dirt)
            if (result.value>val):
                best_node = result
                val = result.value
            if (val>alpha):
                alpha = val
            if beta <= alpha:
                break
    return best_node

def abMin(state, agent_idx, action_counter, prev_action, alpha, beta, sucked_dirt):
    if(is_terminal(state, action_counter)):
        return utility(state, prev_action, sucked_dirt)
    agent = agents[agent_idx]
    best_node = None
    val = np.Infinity
    states = []
    for a in actions:
        s, s_dirt = perform_action(state, agent, a, sucked_dirt)
        if (s not in states or a in ["suck"]):
            states.append(s)
            if (agent_idx < len(agents)-1):
                next_agent = agents[agent_idx+1]
                if (next_agent%2==0):
                # if agents is even it plays random
                    result = randValue(s, agent_idx+1, action_counter+1, prev_action+[a], s_dirt)
                else:
                # if agents is odd it plays optimal
                    result = abMin(s, agent_idx+1, action_counter+1, prev_action+[a], alpha, beta, s_dirt)
            else:
                result = maxValue(s, action_counter+1, prev_action+[a], s_dirt)

            if (result.value<val):
                best_node = result
                val = result.value
            if (val<beta):
                beta= val 
            if beta <= alpha:
                break
    return best_node


def abMinMax(state):
    action_counter = 0
    best_node = None
    best_action = None
    max_value = - np.Infinity
    alpha = -np.Infinity
    beta = np.Infinity 
    states = []
    sucked_dirt = 0
    for a in actions:
        s, s_dirt = perform_action(state,0, a,sucked_dirt)
        if (s not in states or a in ["suck"]):
            states.append(s)
            next_agent = agents[1]
            if (next_agent%2==0):
                # if agents is even it plays random
                result = randValue(s, 1, action_counter+1, [a], s_dirt)
            else:
            # if agents is odd it plays optimal
                result = abMin(s, 1, action_counter+1, [a], alpha, beta, s_dirt)
            if (result.value>max_value):
                max_value = result.value 
                best_node = result
                best_action = a
            if (max_value>alpha):
                alpha = max_value
            if beta <= alpha:
                break
    return best_action, max_value, calls 


def MinMax(state):
    action_counter = 0
    best_action = None
    max_value = - np.Infinity
    next_agent = agents[1]
    states = []
    sucked_dirt = 0 
    for a in actions:
        s, s_dirt = perform_action(state,0, a, sucked_dirt)
        if (s not in states or a in ["suck"]):
            states.append(s)
            if (next_agent%2==0):
                # if agents is even it plays random
                result = randValue(s, 1, action_counter+1, [a], s_dirt)
            else:
                # if agents is odd it plays optimal
                result = minValue(s, 1, action_counter+1, [a], s_dirt)
            if (result.value>max_value):
                max_value = result.value 
                best_node = result
                best_action = a
    return best_action, max_value, calls 

def minValue(state, agent_idx, action_counter, prev_action, sucked_dirt):

    if(is_terminal(state, action_counter)):
        return utility(state, prev_action, sucked_dirt)
    agent = agents[agent_idx]
    best_node = None
    best_val = np.Infinity
    states = []
    for a in actions:
        s, s_dirt = perform_action(state, agent, a, sucked_dirt)
        if (s not in states or a in ["suck"]):
            states.append(s)
            if (agent_idx < len(agents)-1):
                next_agent = agents[agent_idx+1]
                if (next_agent%2==0):
                    result = randValue(s, agent_idx+1, action_counter+1, prev_action+[a], s_dirt)
                else:
                    result = minValue(s, agent_idx+1, action_counter+1, prev_action+[a], s_dirt)
            else:
                result = maxValue(s, action_counter+1, prev_action+[a], s_dirt)
            if (result.value<best_val):
                best_node = result
                best_val = result.value
    
    return best_node

def randValue(state, agent_idx, action_counter, prev_action, sucked_dirt):

    if(is_terminal(state, action_counter)):
        return utility(state, prev_action, sucked_dirt)
    agent = agents[agent_idx]
    used_actions = []
    values = []
    states = []
    for a in actions:
        s, s_dirt = perform_action(state, agent, a, sucked_dirt)
        if (s not in states or a in ["suck"]):
            states.append(s)  
            if (agent_idx < len(agents)-1):
                next_agent = agents[agent_idx+1]
                if (next_agent%2==0):
                    result = randValue(s, agent_idx+1, action_counter+1, prev_action+[a], s_dirt)
                else:
                    result = minValue(s, agent_idx+1, action_counter+1, prev_action+[a], s_dirt)
            else:
                result = maxValue(s, action_counter+1, prev_action+[a], s_dirt)
            used_actions.append(a)
            values.append(result.value)
    
    path = result.paths
    #path[action_counter] = used_actions
    node = Node(np.mean(values), path)
    
    return node



def maxValue(state,action_counter, prev_action, sucked_dirt):

    if(is_terminal(state, action_counter)):
        return utility(state, prev_action, sucked_dirt)
    
    best_node = None 
    val = -np.Infinity
    states = []
    for a in actions:
        s,s_dirt = perform_action(state,0 ,a, sucked_dirt)
        if (s not in states or a in ["suck"]):
            states.append(s)
            next_agent = agents[1]
            if (next_agent%2==0):
                # if agents is even it plays random
                result = randValue(s, 1, action_counter+1, [a], s_dirt)
            else:
                # if agents is odd it plays optimal
                result = minValue(s, 1, action_counter+1, [a], s_dirt)
            if (result.value>val):
                best_node = result
                val = result.value
    
    return best_node


def write(agent="", action="", action_counter=""):
    string = str(agent) + " "+ action + " " + str(action_counter)
    with open("output.txt", 'a+') as f:
        f.write(string + "\n")
        if (agent==0 and action=="suck" and action_counter==4):
            f.write("\n")


  
if __name__=="__main__":


    # read search_type, n_actions and init file path from command line arguments
    search_type = sys.argv[1]
    init_file = sys.argv[2]
    n_actions = int(sys.argv[3])


    # convert init file to initial state 
    with open(init_file) as file:
        state = list(map(split,[line.replace('\n','').replace("c", "0") for line in file]))
    
    X_SHAPE = len(state)-1
    Y_SHAPE = len(state[0])-1

    max_cleaner = count_enemies(state)
    num_dirts = count_dirts(state)

    agents = init_cleaners(state)
    cleaners = find_cleaners(state)
    
    if (search_type=="min-max"):
        action, value, calls = MinMax(state)
    elif(search_type=="alpha-beta"):
        action, value, calls = abMinMax(state)
    
    print(f"Action: {action}")
    print(f"Value: {value}")
    print(f"Util calls: {calls}")
    
    
  
