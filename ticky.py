

import random, sys, time, pygame
from pygame.locals import *


# Create the constants (go ahead and experiment with different values)
BOARDWIDTH = 3  # number of columns in the board
BOARDHEIGHT = 3 # number of rows in the board
TILESIZE = 100
WINDOWWIDTH = 480
WINDOWHEIGHT = 480
FPS = 30
BLANK = None

#                 R    G    B
BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)
BRIGHTBLUE =    (  0,  50, 255)
DARKTURQUOISE = (  3,  54,  73)
GREEN =         (  0, 204,   0)

BGCOLOR = DARKTURQUOISE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

BLANK = 10
PLAYER_O = 11
PLAYER_X = 21


PLAYER_O_WIN = PLAYER_O * 3
PLAYER_X_WIN = PLAYER_X * 3

CONT_GAME 		= 10
DRAW_GAME 		= 20
QUIT_GAME 		= 30

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

choice = 0

def check_draw_game(board):
	return True if sum(board)%10 == 9 else False

def check_win_game(board):
	if ((board[0]+board[1]+board[2]) == PLAYER_O_WIN):
		return PLAYER_O
	elif ((board[0]+board[1]+board[2]) == PLAYER_X_WIN):
		return PLAYER_X
	elif ((board[3]+board[4]+board[5]) == PLAYER_O_WIN):
		return PLAYER_O
	elif ((board[3]+board[4]+board[5]) == PLAYER_X_WIN):
		return PLAYER_X
	elif ((board[6]+board[7]+board[8]) == PLAYER_O_WIN):
		return PLAYER_O
	elif ((board[6]+board[7]+board[8]) == PLAYER_X_WIN):
		return PLAYER_X
	elif ((board[0]+board[3]+board[6]) == PLAYER_O_WIN):
		return PLAYER_O
	elif ((board[0]+board[3]+board[6]) == PLAYER_X_WIN):
		return PLAYER_X
	elif ((board[1]+board[4]+board[7]) == PLAYER_O_WIN):
		return PLAYER_O
	elif ((board[1]+board[4]+board[7]) == PLAYER_X_WIN):
		return PLAYER_X
	elif ((board[2]+board[5]+board[8]) == PLAYER_O_WIN):
		return PLAYER_O
	elif ((board[2]+board[5]+board[8]) == PLAYER_X_WIN):
		return PLAYER_X
	elif ((board[0]+board[4]+board[8]) == PLAYER_O_WIN):
		return PLAYER_O
	elif ((board[0]+board[4]+board[8]) == PLAYER_X_WIN):
		return PLAYER_X
	elif ((board[2]+board[4]+board[6]) == PLAYER_O_WIN):
		return PLAYER_O
	elif ((board[2]+board[4]+board[6]) == PLAYER_X_WIN):
		return PLAYER_X
	elif check_draw_game(board):
		return DRAW_GAME
	else:
		return CONT_GAME

def unit_score(winner,depth):
	if winner == DRAW_GAME:
		return 0
	else:
		return 10 - depth if winner == PLAYER_X else depth - 10

def get_available_step(board):
	ava_step = []
	for i in range(9):
		if board[i] == BLANK:
			ava_step.append(i)
	return ava_step



def minmax(board, depth):
	global choice
	result = check_win_game(board)
	if result != CONT_GAME:
		return unit_score(result, depth)

	depth += 1
	scores = []
	steps = []

	for step in get_available_step(board):
		score = minmax(update_state(board,step,depth),depth)
		scores.append(score)
		steps.append(step)

	if depth % 2 == 1:
		max_value_index = scores.index(max(scores))
		choice = steps[max_value_index]
		return max(scores)
	else:
		min_value_index = scores.index(min(scores))
		choice = steps[min_value_index]
		return min(scores)

def update_state(board, step, depth):
	board = list(board)
	if depth % 2 ==1:
		board[step] = PLAYER_X
	else:
		board[step] = PLAYER_O
	return board

def update_board(board, step, player):
	board[step] = player

def change_to_player(player):
	if player == PLAYER_O:
		return 'O'
	elif player == PLAYER_X:
		return 'X'
	elif player == BLANK:
		return '-'


#def draw_the_game(board):
#	for i in range(3):
#		for j in range(3):
#			print change_to_player(board[i*3+j]),
#		print ' '

def drawBoard(board, message):
    DISPLAYSURF.fill(BGCOLOR)
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)

    for tilex in range(3):
        for tiley in range(3):
        	if board[tilex*3+tiley] != BLANK:
                 drawTile(tilex, tiley, board[tilex*3+tiley])

    left, top = getLeftTopOfTile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)

    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)

def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)

def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

def drawTile(tilex, tiley, symbol, adjx=0, adjy=0):
    # draw a tile at board coordinates tilex and tiley, optionally a few
    # pixels over (determined by adjx and adjy)
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    textSurf = BASICFONT.render(symbol_to_str(symbol), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(textSurf, textRect)


def symbol_to_str(symbol):
	if symbol == PLAYER_O:
		return 'O'
	elif symbol ==PLAYER_X:
		return 'X'

def getSpotClicked(x, y):
    # from the x & y pixel coordinates, get the x & y board coordinates
    for tileX in range(3):
        for tileY in range(3):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)

def board_to_step(spotx, spoty):
	return spotx * 3 + spoty

def main():
	global FPSCLOCK, DISPLAYSURF, BASICFONT, NEW_SURF, NEW_RECT
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	pygame.display.set_caption('Ticky')
	BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
	NEW_SURF,   NEW_RECT   = makeText('New Game', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)
	board = [BLANK] * 9
	flag = 0
	msg = "Ticky - Unbeatable Tic Tac Toe AI"
	drawBoard(board,msg)
	pygame.display.update()
	computer_turn = 0
	while True:
		(spotx, spoty) = (None, None)
		for event in pygame.event.get():
			if event.type == MOUSEBUTTONUP:
				spotx, spoty = getSpotClicked(event.pos[0], event.pos[1])
				if (spotx, spoty) == (None, None):
					if NEW_RECT.collidepoint(event.pos):
						board = [BLANK] * 9
						flag = 0
						msg = "Ticky - Unbeatable Tic Tac Toe AI"
						drawBoard(board, msg)
						pygame.display.update()
		if (spotx, spoty) != (None, None):
			if not flag:
				player = PLAYER_O
				next_step = board_to_step(spotx, spoty)
				update_board(board,next_step, player)
				result = check_win_game(board)
				if result != CONT_GAME:
					flag = 1
					if result == PLAYER_X:
						msg = "Ticky win!"
					elif result == PLAYER_O:
						msg = "you win, awesome!"
					else:
						msg = "Draw game"
				drawBoard(board, msg)
				pygame.display.update()
				computer_turn = 1
			if not flag and computer_turn:
				score = minmax(board, 0)
				player = PLAYER_X
				update_board(board, choice, player)
				result = check_win_game(board)
				if result != CONT_GAME:
					flag = 1
					if result == PLAYER_X:
						msg = "Ticky win!"
					elif result == PLAYER_O:
						msg = "you win, awesome!"
					else:
						msg = "Draw game"
				drawBoard(board, msg)
				pygame.display.update()
				computer_turn = 0


if __name__ == '__main__':
	main()