import pygame
from pygame.locals import *

pygame.init()

BLUE = (0, 0, 255)
GREEN = (0 ,255, 0)
RED = (255, 0 , 0)

width = 300
height = 300
line_width = 6
font = pygame.font.SysFont(None,40)

screen = pygame.display.set_mode((width, height))

markers = []
clicked = False
pos = []
player = 1
winner = 0
game_over = False
again_rect = Rect(width//2 - 80,height//2,160,50)

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
				pygame.draw.line(screen,GREEN,(x_pos*100+15,y_pos*100+15),(x_pos*100+85,y_pos*100+85))
				pygame.draw.line(screen,GREEN,(x_pos*100+15,y_pos*100+85),(x_pos*100+85,y_pos*100+15))
			if y == -1:
				pygame.draw.circle(screen,RED,(x_pos*100+50,y_pos*100+50),30,line_width)
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
	if winner == 0:
		win_text = 'Draw!'
	else:	
		win_text = 'Player ' + str(winner) + ' wins!'
	win_img = font.render(win_text, True, BLUE)
	pygame.draw.rect(screen,GREEN,(width//2 -100,height//2 -60,200,50))
	screen.blit(win_img,(width//2 -100,height//2 -50))

	again_text = 'Play Again?'
	again_img = font.render(again_text, True, BLUE)
	pygame.draw.rect(screen,GREEN,again_rect)
	screen.blit(again_img,(width//2 -80,height//2 +10))

run = True

for x in range(3):
	row = [0]*3
	markers.append(row)

print(markers)

while run:

	draw_grid()
	draw_marker()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if game_over == 0:
			if event.type == pygame.MOUSEBUTTONDOWN:
				clicked = True
			if event.type == pygame.MOUSEBUTTONUP and clicked == True:
				clicked = False
				pos = pygame.mouse.get_pos()
				cell_x = pos[0]
				cell_y = pos[1]
				if markers[cell_x//100][cell_y//100] == 0:
					markers[cell_x//100][cell_y//100] = player
					player *= -1
				legal_moves = []
				for x in (0,1,2):
					for y in (0,1,2):
						if markers[x][y] == 0:
							legal_moves.append([x,y])
				if not legal_moves:
					player = 0
					game_over = True
				else: 
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