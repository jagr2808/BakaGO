from tkinter import *

import sys
from PIL import Image

WHITE = 1
BLACK = -1
DRAW = 0

def create_board_image(n):
	tl = Image.open('img/top_left.png')
	ue = Image.open('img/up_edge.png')
	tr = Image.open('img/top_right.png')
	le = Image.open('img/left_edge.png')
	c = Image.open('img/center.png')
	re = Image.open('img/right_edge.png')
	bl = Image.open('img/bottom_left.png')
	de = Image.open('img/down_edge.png')
	br = Image.open('img/bottom_right.png')
	
	images = ([tl] + (n-2)*[ue] + [tr]) +\
		(n-2)*([le] + (n-2)*[c] + [re]) +\
		([bl] + (n-2)*[de] + [br])
	widths, heights = zip(*(i.size for i in images))

	total_width = n*images[0].size[0]
	total_height = n*images[0].size[0]

	new_im = Image.new('RGB', (total_width, total_height))

	for x in range(n):
		for y in range(n):
			im = images[y*n+x]
			new_im.paste(im, (x*im.size[0], y*im.size[1]))
	s ='img/board.png'
	new_im.save(s)
	return s

def fill_board_image(board):
	size = board.shape[0]
	new_im = Image.open('img/board.png')
	black_stone = Image.open('img/black_stone.png')
	white_stone = Image.open('img/white_stone.png')
	for x in range(size):
		for y in range(size):
			if board[x, y] == BLACK:
				new_im.paste(black_stone, (x*black_stone.size[0], y*black_stone.size[1]), black_stone)
			elif board[x, y] == WHITE:
				new_im.paste(white_stone, (x*white_stone.size[0], y*white_stone.size[1]), white_stone)
	s ='img/game.png'
	new_im.save(s)
	return s

class GUI:
	def click(self, event):
		print('clcik')
		size = self.size
		self.move = ((event.x*size // self.img.width()), (event.y*size // self.img.height()))
		self.clicked.set(1)
		return
		if set_move((event.x*board.size // self.img.width()) + 1, (event.y*board.size // self.img.height()) + 1):
			turn = (turn+1)%2
			board.remove_dead(turn)
			board.prev_move[(turn+1)%2] = board.copy()
			
			self.img = PhotoImage(file=fill_board_image())
			self.canvas.itemconfig(self.image_on_canvas, image = self.img)
			self.canvas.update()
			
			make_move()
			turn = (turn+1)%2
			board.remove_dead(turn)
			board.prev_move[(turn+1)%2] = board.copy()
		self.img = PhotoImage(file=fill_board_image())
		self.canvas.itemconfig(self.image_on_canvas, image = self.img)
		#self.canvas.update()
	
	def make_move(self, board):
		print('waiting')
		self.clicked = IntVar()
		self.canvas.wait_variable(self.clicked)
		return self.move
		
		
	def draw(self, board):
		self.img = PhotoImage(file=fill_board_image(board))
		self.canvas.itemconfig(self.image_on_canvas, image = self.img)
		
	
	def wait(self, time):
		var = IntVar()
		self.root.after(time, var.set, 1)
		self.root.wait_variable(var)
	
	def __init__(self, size):
		self.size = size
		self.root = Tk()

		#setting up a tkinter canvas with scrollbars
		self.frame = Frame(self.root, bd=2, relief=SUNKEN, width=500, height=500)
		self.frame.pack_propagate(0)
		self.frame.grid_propagate(0)
		
		self.frame.grid_rowconfigure(0, weight=1)
		self.frame.grid_columnconfigure(0, weight=1)
		xscroll = Scrollbar(self.frame, orient=HORIZONTAL)
		xscroll.grid(row=1, column=0, sticky=E+W)
		yscroll = Scrollbar(self.frame)
		yscroll.grid(row=0, column=1, sticky=N+S)
		self.canvas = Canvas(self.frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
		self.canvas.grid(row=0, column=0, sticky=N+S+E+W)
		xscroll.config(command=self.canvas.xview)
		yscroll.config(command=self.canvas.yview)
		self.frame.pack(fill=BOTH,expand=1)

		#adding the image
		self.img = PhotoImage(file=create_board_image(self.size))
		self.image_on_canvas = self.canvas.create_image(0,0,image=self.img,anchor="nw")
		self.canvas.config(scrollregion=self.canvas.bbox(ALL))
		
		#mouseclick event
		self.canvas.bind("<Button 1>",self.click)

		self.wait(100)
		#root.mainloop()
