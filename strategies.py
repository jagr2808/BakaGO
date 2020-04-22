from random import randint
import numpy as np

def mr_random(board):
	b = board.state()
	for i in range(10):
		x = randint(0, 8)
		y = randint(0, 8)
		if b[x, y] == 0:
			return (x, y)
	return (-1, -1)
	
def take_shared_liberty(board):
	b = board.state()
	g, groups = board.groups(b)
	if (groups == 1 and board.movenumber > 7) or (board.movenumber > 67 and groups < 3):
		return (-1,-1)
	l, _ = board.liberties(g, groups)
	l = np.sum(l, axis=2)
	nums = l.flatten()
	ms = np.argwhere(nums == np.amax(nums)).flatten()
	m = np.unravel_index(ms[randint(0, len(ms)-1)], l.shape)
	return m
	
def weakest_group(board):
	b = board.state()
	g, groups = board.groups(b)
	if groups == 0:
		return (3, 4)
	if (groups == 1 and board.movenumber > 7) or (board.movenumber > 67 and groups < 3):
		return (-1,-1)
	l, libs = board.liberties(g, groups)
	weak = np.argmin(libs)
	l = l[:,:,weak]
	m = np.argmax(l)
	m = np.unravel_index(m, l.shape)
	return m
	
