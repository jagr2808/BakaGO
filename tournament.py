import numpy as np
from GUI import *
import strategies as strat

WHITE = 1
BLACK = -1
DRAW = 0
ILLEGAL = -2

class Board:
	def __init__(self, size=9):
		self.size = size
		self.board = np.zeros((size, size, 2*size*size), int)
		self.ko = None
		self.movenumber = 0
	
	def move(self, x, y, color):
		self.movenumber += 1
		m = self.movenumber
		
		if (x, y) == (-1, -1):
			self.board[:, :, m] = self.board[:, :, m-1]
			return color
			
		if m >= self.board.shape[2]-1:
			return DRAW
		if self.board[x, y, m-1] != 0:
			self.board[:, :, m] = self.board[:, :, m-1]
			return ILLEGAL
		self.board[:, :, m] = self.board[:, :, m-1]
		self.board[x, y, m] = color
		self.simplify(color)
		return color
	
	def state(self):
		return self.board[:,:,self.movenumber]
	
	def simplify(self, color):
		g, groups = self.groups(self.board[:,:,self.movenumber])
		l, libs = self.liberties(g, groups)
		for x in range(self.size):
			for y in range(self.size):
				i = -g[x,y]*color
				if i > 0 and libs[i-1] == 0:
					self.board[x, y, self.movenumber] = 0
					g[x, y] = 0
		l, libs = self.liberties(g, groups)
		for x in range(self.size):
			for y in range(self.size):
				i = g[x,y]*color
				if i > 0 and libs[i-1] == 0:
					self.board[x, y, self.movenumber] = 0
		
	
	def groups(self, b):
		groups = 0
		g = np.zeros((self.size, self.size), int)
		#b = self.board[:,:,self.movenumber]
		
		def recurse(x, y, color):
			if x - 1 >= 0 and g[x-1, y] == 0 and b[x-1, y] == color:
				g[x-1, y] = color*groups
				recurse(x-1, y, color)
			if x + 1 < self.size and g[x+1, y] == 0 and b[x+1, y] == color:
				g[x+1, y] = color*groups
				recurse(x+1, y, color)
			if y - 1 >= 0 and g[x, y-1] == 0 and b[x, y-1] == color:
				g[x, y-1] = color*groups
				recurse(x, y-1, color)
			if y + 1 < self.size and g[x, y+1] == 0 and b[x, y+1] == color:
				g[x, y+1] = color*groups
				recurse(x, y+1, color)
		
		for x in range(self.size):
			for y in range(self.size):
				if g[x,y] == 0 and b[x, y] != 0:
					color = b[x,y]
					groups += 1
					g[x, y] = color*groups
					recurse(x, y, color)
		print(g)
		return g, groups
	
	def liberties(self, g, groups):
		liberties = np.zeros((self.size, self.size, groups), int)
		for x in range(self.size):
			for y in range(self.size):
				if g[x,y] == 0:
					if x - 1 >= 0 and g[x-1, y] != 0:
						liberties[x, y, abs(g[x-1, y])-1] = 1
					if x + 1 < self.size and g[x+1, y] != 0:
						liberties[x, y, abs(g[x+1, y])-1] = 1
					if y - 1 >= 0 and g[x, y-1] != 0:
						liberties[x, y, abs(g[x, y-1])-1] = 1
					if y + 1 < self.size and g[x, y+1] != 0:
						liberties[x, y, abs(g[x, y+1])-1] = 1
		print(np.sum(liberties, axis=(0,1)))
		return liberties, np.sum(liberties, axis=(0,1))
		
	def score(self):
		# !!!! liberties are never negative, bad scoring makes no sense then!!!!
		print('scoring')
		g, groups = self.groups(self.board[:,:,self.movenumber])
		l, libs = self.liberties(g, groups)
		score = np.sum(self.board[:,:,self.movenumber])
		l = np.sum(l, axis=2)
		score += np.sum(np.ones((self.size, self.size))[l > 0])
		return score
		
def match(playerblack, playerwhite, update=None, spectater=None):
	color = BLACK
	board = Board()
	passing = False
	while True:
		if spectater != None:
			spectater(200)
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
			break
		color *= -1
		if update != None:
			update(board, m)
	#calculate winner...
	s = board.score() + 6.5
	if s > 0:
		print('W+%.1f' % s)
	else:
		print('B+%.1f' % -s)
	if spectater != None:
		spectater(5000)
	
if __name__ == '__main__':
	screen = GUI(9)
	
	match(strat.weakest_group, strat.take_shared_liberty, lambda b, _: screen.draw(b.state()), screen.wait)
	
	