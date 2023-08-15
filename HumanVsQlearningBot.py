import random
import pygame
from pygame.locals import *
import logging
import numpy as np
import itertools

# logging.basicConfig(filename = 'Result.log', level=logging.INFO)
# copy Rohit Agrawal's work and modify for py_game version. It doesn't work really well but the concept has been applied. 

pygame.init()

BLUE = (0, 0, 255)
GREEN = (0 ,255, 0)
RED = (255, 0 , 0)

width = 300
height = 300
line_width = 6
font = pygame.font.SysFont(None,20)

screen = pygame.display.set_mode((width, height))

markers = [[0,0,0],[0,0,0],[0,0,0]]
clicked = False
pos = []
player = 1
winner = 0
game_over = False
again_rect = Rect(width//2 - 80,height//2,160,50)
win = [0,0]
totalgame = 0
win_text = ''
winrateCalculated = False
states_dict = {}


def copy_game_state(state):
    new_state = [[0,0,0],[0,0,0],[0,0,0]]
    for i in range(3):
        for j in range(3):
            new_state[i][j] = state[i][j]
    return new_state
    

def play_move(state, player, block_num):
    if state[int((block_num-1)/3)][(block_num-1)%3] == 0:
        state[int((block_num-1)/3)][(block_num-1)%3] = player

def draw_grid():
	gr = (50,50,50)
	bg = (255,255,200)
	screen.fill(bg)
	for x in range(1,3):
		pygame.draw.line(screen,gr,(0,x*(width/3)), (width,x * (width/3)), line_width)
		pygame.draw.line(screen,gr,(x*(height/3),0), (x * (height/3),height), line_width)

def draw_marker():
	x_pos = 0
	for x in markers:
		y_pos =0
		for y in x:
			if y == 1:
				pygame.draw.line(screen,GREEN,(y_pos*100+15,x_pos*100+15),(y_pos*100+85,x_pos*100+85))
				pygame.draw.line(screen,GREEN,(y_pos*100+15,x_pos*100+85),(y_pos*100+85,x_pos*100+15))
			if y == -1:
				pygame.draw.circle(screen,RED,(y_pos*100+50,x_pos*100+50),30,line_width)
			y_pos +=1
		x_pos +=1

def check_winner():
	global winner
	global game_over

	y_pos = 0

	for x in markers:
		if sum(x) == 3:
			winner = 1
			game_over =True
		if sum(x) == -3:
			winner = 2
			game_over =True
		if markers[0][y_pos] + markers[1][y_pos] + markers[2][y_pos] == 3:
			winner = 1
			game_over = True
		if markers[0][y_pos] + markers[1][y_pos] + markers[2][y_pos] == -3:
			winner = 2
			game_over= True
		y_pos +=1
	
	if markers[0][0] + markers[1][1] +markers[2][2] == 3 or markers[2][0] + markers[1][1] +markers[0][2] == 3:
		winner = 1
		game_over = True
	if markers[0][0] + markers[1][1] +markers[2][2] == -3 or markers[2][0] + markers[1][1] +markers[0][2] == -3:
		winner = 2
		game_over = True

def draw_winner(winner):
	global totalgame, win_text, winrateCalculated

	if winner == 0 and winrateCalculated == False:
		totalgame += 1
		win_text = 'Draw!'
	else:	
		if winner == 1 and winrateCalculated == False:
			totalgame += 1
			win[0] += 1
			winrate1 = str((win[0]/totalgame)*100)
			win_text = 'Player 1 wins!'
			logging.info(win_text)
		if winner == 2 and winrateCalculated == False:
			totalgame += 1
			win[1] += 1
			winrate2 = str((win[1]/totalgame)*100)
			win_text = 'Player 2 wins!'
			logging.info(win_text)

	win_img = font.render(win_text, True, BLUE)
	pygame.draw.rect(screen,GREEN,(width//2 -100,height//2 -60,200,50))
	screen.blit(win_img,(width//2 -100,height//2 -50))

	again_text = 'Play Again?'
	again_img = font.render(again_text, True, BLUE)
	pygame.draw.rect(screen,GREEN,again_rect)
	screen.blit(again_img,(width//2 -80,height//2 +10))
	winrateCalculated = True

        

def getBestMove(state, player):
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
    
    if not empty_cells:
    	return -1

    for empty_cell in empty_cells:
        moves.append(empty_cell)
        new_state = copy_game_state(state)
        play_move(new_state, player, empty_cell)
        next_state_idx = list(states_dict.keys())[list(states_dict.values()).index(new_state)]
        curr_state_values.append(state_values_for_AI[next_state_idx])
        print('next state value', state_values_for_AI[next_state_idx])
    print('Possible moves = ' + str(moves))
    print('Move values = ' + str(curr_state_values))    
    print('markers:',markers)
    best_move_idx = np.argmax(curr_state_values)
    # print('state:',states_dict[best_move_idx])

    best_move = moves[best_move_idx]
    return best_move

def print_board(game_state):
    print('----------------')
    print('| ' + str(game_state[0][0]) + ' || ' + str(game_state[0][1]) + ' || ' + str(game_state[0][2]) + ' |')
    print('----------------')
    print('| ' + str(game_state[1][0]) + ' || ' + str(game_state[1][1]) + ' || ' + str(game_state[1][2]) + ' |')
    print('----------------')
    print('| ' + str(game_state[2][0]) + ' || ' + str(game_state[2][1]) + ' || ' + str(game_state[2][2]) + ' |')
    print('----------------')
    

#LOAD TRAINED STATE VALUES
state_values_for_AI = np.loadtxt('trained_state_values_O.txt', dtype=np.float64)

players = [1,-1,0]
states_dict = {}
all_possible_states = [[list(i[0:3]),list(i[3:6]),list(i[6:10])] for i in itertools.product(players, repeat = 9)]
n_states = len(all_possible_states) # 2 players, 9 space values
n_actions = 9   # 9 spaces

for i in range(n_states):
    states_dict[i] = all_possible_states[i]


run = True



while run:

	draw_grid()
	draw_marker()

	draw = 0

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if game_over == 0:
			if event.type == pygame.MOUSEBUTTONDOWN:
				clicked = True
			if event.type == pygame.MOUSEBUTTONUP and clicked == True:
				clicked = False
				pos = pygame.mouse.get_pos()
				cell_x = pos[1]
				cell_y = pos[0 ]
				print(cell_x//100,cell_y//100)
				if markers[cell_x//100][cell_y//100] == 0:
					markers[cell_x//100][cell_y//100] = player			
					player *= -1
				check_winner()
				
	if player == -1 and game_over == False:
		smartMove = getBestMove(markers,-1)
		print(smartMove)
		if smartMove == -1:
			#draw
			player = 0
			game_over = True
		else:
			markers[(smartMove-1)%3][int((smartMove-1)/3)] = player
			print_board(markers)
			player *= -1
			check_winner()

	if game_over == True:
		draw_winner(winner)
		if event.type == pygame.MOUSEBUTTONDOWN:
			clicked = True
		if event.type == pygame.MOUSEBUTTONUP and clicked == True:
			pos = pygame.mouse.get_pos()
			if again_rect.collidepoint(pos):
				markers = []
				pos = []
				player = 1
				winner = 0
				game_over = False
				for x in range(3):
					row = [0]*3
					markers.append(row)

	pygame.display.update()


pygame.quit()