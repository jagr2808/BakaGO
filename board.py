import numpy as np

WHITE = 1
BLACK = -1
DRAW = 0
ILLEGAL = -2

class Board:
	def __init__(self, size=9, komi=6.5):
		self.size = size
		self.komi = komi
		self.board = np.zeros((size, size, 2*size*size), int)
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
		Board.simplify(self.board[:, :, m], color)
		if m > 1 and self.board[x,y,m-2] == color and (self.board[:,:, m] == self.board[:,:, m-2]).all(): # (japaneese) ko
			return ILLEGAL
		return color
	
	def state(self):
		return self.board[:,:,self.movenumber]
	
	def simplify(board, color):
		size = board.shape[0]
		g, groups = Board.groups(board)
		l, libs = Board.liberties(g, groups)
		libs = np.abs(libs)
		for x in range(size):
			for y in range(size):
				i = -g[x,y]*color
				if i > 0 and libs[i-1] == 0:
					board[x, y] = 0
					g[x, y] = 0
		l, libs = Board.liberties(g, groups)
		for x in range(size):
			for y in range(size):
				i = g[x,y]*color
				if i > 0 and libs[i-1] == 0:
					board[x, y] = 0
		
	def groups(b):
		groups = 0
		size = b.shape[0]
		g = np.zeros((size, size), int)
		
		def recurse(x, y, color):
			if x - 1 >= 0 and g[x-1, y] == 0 and b[x-1, y] == color:
				g[x-1, y] = color*groups
				recurse(x-1, y, color)
			if x + 1 < size and g[x+1, y] == 0 and b[x+1, y] == color:
				g[x+1, y] = color*groups
				recurse(x+1, y, color)
			if y - 1 >= 0 and g[x, y-1] == 0 and b[x, y-1] == color:
				g[x, y-1] = color*groups
				recurse(x, y-1, color)
			if y + 1 < size and g[x, y+1] == 0 and b[x, y+1] == color:
				g[x, y+1] = color*groups
				recurse(x, y+1, color)
		
		for x in range(size):
			for y in range(size):
				if g[x,y] == 0 and b[x, y] != 0:
					color = b[x,y]
					groups += 1
					g[x, y] = color*groups
					recurse(x, y, color)
		#print(g)
		return g, groups
	
	def liberties(g, groups):
		size = g.shape[0]
		liberties = np.zeros((size, size, groups), int)
		group_color = np.zeros(groups)
		for x in range(size):
			for y in range(size):
				if g[x,y] == 0:
					if x - 1 >= 0 and g[x-1, y] != 0:
						liberties[x, y, abs(g[x-1, y])-1] = 1
					if x + 1 < size and g[x+1, y] != 0:
						liberties[x, y, abs(g[x+1, y])-1] = 1
					if y - 1 >= 0 and g[x, y-1] != 0:
						liberties[x, y, abs(g[x, y-1])-1] = 1
					if y + 1 < size and g[x, y+1] != 0:
						liberties[x, y, abs(g[x, y+1])-1] = 1
				else:
					group_color[abs(g[x, y])-1] = g[x,y]
		group_color = np.sign(group_color)
		print(np.sum(liberties, axis=(0,1)))
		return liberties, np.sum(liberties, axis=(0,1))*group_color
	
	def eyes(board):
		size = board.shape[0]
		g, groups = Board.groups(board)
		libs, _ = Board.liberties(g, groups)
		eyes = np.zeros(g.shape)
		for x in range(size):
			for y in range(size):
				neighbours = []
				if x - 1 >= 0:
					neighbours.append(g[x-1, y])
				if x + 1 < size:
					neighbours.append(g[x+1, y])
				if y - 1 >= 0 and g[x, y-1] != 0:
					neighbours.append(g[x, y-1])
				if y + 1 < size and g[x, y+1] != 0:
					neighbours.append(g[x, y+1])
				neighbours = np.array(neighbours)
				if g[x, y] == 0 and (neighbours == neighbours[0]).all():
					eyes[x, y] = neighbours[0]
		return eyes
		
	def areascore(board):
		size = board.shape[0]
		g, _ = Board.groups(board)
		g = np.sign(g)
		white_territory = np.zeros((size, size), int)
		black_territory = np.zeros((size, size), int)
		
		def recurse(x, y, color, territory):
				
			if x - 1 >= 0 and g[x-1, y] == 0 and territory[x-1, y] == 0:
				territory[x-1, y] = color
				recurse(x-1, y, color, territory)
			if x + 1 < size and g[x+1, y] == 0 and territory[x+1, y] == 0:
				territory[x+1, y] = color
				recurse(x+1, y, color, territory)
			if y - 1 >= 0 and g[x, y-1] == 0 and territory[x, y-1] == 0:
				territory[x, y-1] = color
				recurse(x, y-1, color, territory)
			if y + 1 < size and g[x, y+1] == 0 and territory[x, y+1] == 0:
				territory[x, y+1] = color
				recurse(x, y+1, color, territory)
				
		for x in range(size):
			for y in range(size):
				if g[x,y] == BLACK:
					recurse(x, y, BLACK, black_territory)
				elif g[x,y] == WHITE:
					recurse(x, y, WHITE, white_territory)
					print(x,y)
					print(white_territory)
		return np.sum(white_territory + black_territory + g)
	
	def score(self):
		return Board.areascore(self.board[:,:,self.movenumber]) + self.komi
		
