import numpy as np
from math import inf as infinity
import itertools
import random
import time

#copy Rohit Agrawal's work and modify for py_game version
game_state = [[0,0,0],[0,0,0],[0,0,0]]
players = [1,-1]

def play_move(state, player, block_num):
    if state[int((block_num-1)/3)][(block_num-1)%3] == 0:
        state[int((block_num-1)/3)][(block_num-1)%3] = player
    else:
        block_num = int(input("Block is not empty, ya blockhead! Choose again: "))
        play_move(state, player, block_num)
    
def copy_game_state(state):
    new_state = [[0,0,0],[0,0,0],[0,0,0]]
    for i in range(3):
        for j in range(3):
            new_state[i][j] = state[i][j]
    return new_state
    
def check_current_state(game_state):    
    # Check horizontals
    if (game_state[0][0] == game_state[0][1] and game_state[0][1] == game_state[0][2] and game_state[0][0] != 0):
        return game_state[0][0], "Done"
    if (game_state[1][0] == game_state[1][1] and game_state[1][1] == game_state[1][2] and game_state[1][0] != 0):
        return game_state[1][0], "Done"
    if (game_state[2][0] == game_state[2][1] and game_state[2][1] == game_state[2][2] and game_state[2][0] != 0):
        return game_state[2][0], "Done"
    
    # Check verticals
    if (game_state[0][0] == game_state[1][0] and game_state[1][0] == game_state[2][0] and game_state[0][0] != 0):
        return game_state[0][0], "Done"
    if (game_state[0][1] == game_state[1][1] and game_state[1][1] == game_state[2][1] and game_state[0][1] != 0):
        return game_state[0][1], "Done"
    if (game_state[0][2] == game_state[1][2] and game_state[1][2] == game_state[2][2] and game_state[0][2] != 0):
        return game_state[0][2], "Done"
    
    # Check diagonals
    if (game_state[0][0] == game_state[1][1] and game_state[1][1] == game_state[2][2] and game_state[0][0] != 0):
        return game_state[1][1], "Done"
    if (game_state[2][0] == game_state[1][1] and game_state[1][1] == game_state[0][2] and game_state[2][0] != 0):
        return game_state[1][1], "Done"
    
    # Check if draw
    draw_flag = 0
    for i in range(3):
        for j in range(3):
            if game_state[i][j] ==0:
                draw_flag = 1
    if draw_flag is 0:
        return None, "Draw"
    
    return None, "Not Done"

def print_board(game_state):
    print('----------------')
    print('| ' + str(game_state[0][0]) + ' || ' + str(game_state[0][1]) + ' || ' + str(game_state[0][2]) + ' |')
    print('----------------')
    print('| ' + str(game_state[1][0]) + ' || ' + str(game_state[1][1]) + ' || ' + str(game_state[1][2]) + ' |')
    print('----------------')
    print('| ' + str(game_state[2][0]) + ' || ' + str(game_state[2][1]) + ' || ' + str(game_state[2][2]) + ' |')
    print('----------------')
    
  
# Initialize state values into 2 arrays (all possible state values for X and O). 
# Each has a state index and a state value (initialized with 0.0). These will be updated during learning
player = [1,-1,0]
states_dict = {}
all_possible_states = [[list(i[0:3]),list(i[3:6]),list(i[6:10])] for i in itertools.product(player, repeat = 9)]
n_states = len(all_possible_states) # 2 players, 9 space values
n_actions = 9   # 9 spaces
state_values_for_AI_O = np.full((n_states),0.0)
state_values_for_AI_X = np.full((n_states),0.0)
print("n_states = %i \nn_actions = %i"%(n_states, n_actions))

# State values for AI: 1 if for a win. -1 for a lost. 
# No need to update state value if not done at this point
# However, these intermediate states will have subsequent value from the 2 below update_state_value functions (apply learning rate = 0.2), 
# which means state before win will have value of 0.8. state before lost will have value of -0.8

for i in range(n_states):
    states_dict[i] = all_possible_states[i]
    winner, _ = check_current_state(states_dict[i])
    if winner == -1:   # AI won
        state_values_for_AI_O[i] = 1
    elif winner == 1:   # AI lost
        state_values_for_AI_O[i] = -1
        
# State values for AI 'X'       
for i in range(n_states):
    winner, _ = check_current_state(states_dict[i])
    if winner == -1:   # AI lost
        state_values_for_AI_X[i] = -1
    elif winner == 1:   # AI won
        state_values_for_AI_X[i] = 1

#update current state value after a new move is made. New state is determined by getBestMove function below
def update_state_value_O(curr_state_idx, next_state_idx, learning_rate):
    new_value = state_values_for_AI_O[curr_state_idx] + learning_rate*(state_values_for_AI_O[next_state_idx]  - state_values_for_AI_O[curr_state_idx])
    state_values_for_AI_O[curr_state_idx] = new_value
    
def update_state_value_X(curr_state_idx, next_state_idx, learning_rate):
    new_value = state_values_for_AI_X[curr_state_idx] + learning_rate*(state_values_for_AI_X[next_state_idx]  - state_values_for_AI_X[curr_state_idx])
    state_values_for_AI_X[curr_state_idx] = new_value

def getBestMove(state, player, epsilon):
    '''
    Reinforcement Learning Algorithm
    '''    
    moves = []
    curr_state_values = []
    empty_cells = []

    #find all empty cells
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                empty_cells.append(i*3 + (j+1))
    
    #for each empty cells, find the next state value if AI make a move to that empty cell and put all of them into a list.
    #if AI chooses exploration, then best move is just an random empty cell. Decrease the epsilon value so AI would explore less and exploit more in later interatios.
    #if AI chooses exploitation, then best move is the highest state value from list
    for empty_cell in empty_cells:
        moves.append(empty_cell)
        new_state = copy_game_state(state)
        play_move(new_state, player, empty_cell)
        next_state_idx = list(states_dict.keys())[list(states_dict.values()).index(new_state)]
        if player == 1:
            curr_state_values.append(state_values_for_AI_X[next_state_idx])
        else:
            curr_state_values.append(state_values_for_AI_O[next_state_idx])
        
    print('Possible moves = ' + str(moves))
    print('Move values = ' + str(curr_state_values))    
    best_move_idx = np.argmax(curr_state_values)
    
    if np.random.uniform(0,1) <= epsilon:       # Exploration
        best_move = random.choice(empty_cells)
        print('Agent decides to explore! Takes action = ' + str(best_move))
        epsilon *= 0.99
    else:   #Exploitation
        best_move = moves[best_move_idx]
        print('Agent decides to exploit! Takes action = ' + str(best_move))
    return best_move

# PLaying

# #LOAD TRAINED STATE VALUES
state_values_for_AI_X = np.loadtxt('trained_state_values_X.txt', dtype=np.float64)
state_values_for_AI_O = np.loadtxt('trained_state_values_O.txt', dtype=np.float64)

learning_rate = 0.2
epsilon = 0.2
num_iterations = 20000

for iteration in range(num_iterations):
    game_state = [[0,0,0],[0,0,0],[0,0,0]]
    current_state = "Not Done"
    print("\nIteration " + str(iteration) + "!")
    print_board(game_state)
    winner = None
    current_player_idx = random.choice([0,1])
        
    while current_state == "Not Done":
        curr_state_idx = list(states_dict.keys())[list(states_dict.values()).index(game_state)]
        if current_player_idx == 0:     # AI_X's turn
            print("\nAI X's turn!")         
            block_choice = getBestMove(game_state, players[current_player_idx], epsilon)
            play_move(game_state ,players[current_player_idx], block_choice)
            new_state_idx = list(states_dict.keys())[list(states_dict.values()).index(game_state)]
            
        else:       # AI_O's turn
            print("\nAI O's turn!")   
            block_choice = getBestMove(game_state, players[current_player_idx], epsilon)
            play_move(game_state ,players[current_player_idx], block_choice)
            new_state_idx = list(states_dict.keys())[list(states_dict.values()).index(game_state)]
        
        print_board(game_state)
        #print('State value = ' + str(state_values_for_AI[new_state_idx]))
        update_state_value_O(curr_state_idx, new_state_idx, learning_rate)
        update_state_value_X(curr_state_idx, new_state_idx, learning_rate)
        winner, current_state = check_current_state(game_state)
        if winner is not None:
            print(str(winner) + " won!")
        else:
            current_player_idx = (current_player_idx + 1)%2
        
        if current_state is "Draw":
            print("Draw!")
            
        #time.sleep(1)
print('Training Complete!')    

# Save state values for future use
np.savetxt('trained_state_values_X.txt', state_values_for_AI_X, fmt = '%.6f')
np.savetxt('trained_state_values_O.txt', state_values_for_AI_O, fmt = '%.6f')