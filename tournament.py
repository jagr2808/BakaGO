import numpy as np
from GUI import *
import strategies as strat
from board import *


def match(playerblack, playerwhite, update=None, spectater=None):
	color = BLACK
	board = Board()
	passing = False
	while True:
		if spectater != None:
			spectater(20)
		if color == WHITE:
			m = playerwhite(board)
		else:
			m = playerblack(board)
		if m == (-1,-1):
			if color == WHITE:
				print('white passed')
			else:
				print('black passed')
			if passing == False:
				passing = True
			else:
				break
		else:
			passing = False
		x, y = m
		msg = board.move(x, y, color)
		if msg == DRAW:
			break
		if msg == ILLEGAL:
			print('Illegal move')
			break
		color *= -1
		if update != None:
			update(board, m)
	#calculate winner...
	s = board.score()
	if s > 0:
		print('W+%.1f' % s)
	else:
		print('B+%.1f' % -s)
	if spectater != None:
		spectater(10000)
	
if __name__ == '__main__':
	screen = GUI(9)
	
	match(strat.take_shared_liberty, strat.take_shared_liberty, lambda b, _: screen.draw(b.state()), screen.wait)
	#match(strat.weakest_group, strat.take_shared_liberty)
	
	
