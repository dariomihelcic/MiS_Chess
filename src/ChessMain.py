from ChessBoard import ChessBoard
from ChessRules import ChessRules
from ChessAI import ChessAI
import time

class ChessMain:
	command_list = ("reset", "undo", )
	
	def __init__(self):
		#self.GUI = ChessGUI()
		self.Board = ChessBoard()
		self.Rules = ChessRules()
		self.AI = ChessAI()
		self.players = ["White", "Black"]

	#to be moved to GUI class?
	def draw(self,board):
		'''Draw the board in textual forme.'''
		print("    a    b    c    d    e    f    g    h ")
		print("  ----------------------------------------")
		for r in range(8):
			print(str(abs(r-8))+"|", end='',)
			for c in range(8):
				if board[r][c] != 'e':
					print( "",str(board[r][c]), "|", end='',)
				else:
					print("    |", end='',)
				if c == 7:
					print() #to get a new line
			print ("  ----------------------------------------")

	def reset(self):
		'''Reset the game.'''
		self.Board.reset_board()
		self.current_player = 0

	def undo(self):
		#Undo move.
		if self.Board.undo_move():
			self.current_player = (self.current_player+1)%2

	def execute_command(self, command):
		'''
		Execute passed command.
		Check if command is ChessMain method or chess move.
		If move is valid, move the piece and change player.
		'''
		if command in self.command_list:
			function = getattr(self, command)
			function()

		elif self.is_valid_move(command):
			self.Board.move_piece(self.get_move(command))
			self.current_player = (self.current_player+1)%2

		else :
			print("Invalid command! Try again.")

	def is_valid_move(self, command):
		'''Calls Rules.set_up, checks if command is a valid move.'''
		self.Rules.set_up(self.Board.state,
		                  self.Board.get_castle_variables(),
		                  self.players[self.current_player])
		#Check if command is inside board parameters (1-7, a-h) 
		try:
			if int(command[1])-1 in range(8) and \
			   int(command[3])-1 in range(8) and \
			   command[0] in 'abcdefgh' and \
			   command[2] in 'abcdefgh':
			   #Check if command is a vaid move.
				if self.Rules.is_legal_move(
					self.get_from_position(command),
				    self.get_to_position(command)):
					return True
			else:
				print("Incorrect move!")
				return False
		#If move is written in incorrect form, return False.
		#Caused by int() function. 
		except ValueError:
			return False

	def get_from_position(self,command):
		'''Return tuple of from_row and from_col of command.'''
		#Convert letter index to number index. letter->ASCII->index.
		from_col = ord(command[0]) - 97
		#Board index converted from 8-1 to 0-7. 
		from_row = abs(int(command[1])-8) 	
		return (from_row, from_col)

	def get_to_position(self, command):
		'''Return tuple of to_row and to_col of command.'''
		#Convert letter index to number index. letter->ASCII->index.
		to_col = ord(command[2])- 97
		#Board index converted from 8-1 to 0-7. 
		to_row = abs(int(command[3])-8)
		return (to_row, to_col)

	def get_move(self, command):
		'''Return move tuple in from (from_tuple, to_tuple).'''
		return (self.get_from_position(command),
		        self.get_to_position(command))

	def change_player(self):
		self.current_player = (self.current_player+1)%2

	def read_FEN(self, FEN_state):
		#could return state, player, castle_variables, last_move, stale_moves, full_moves. 
		state = [[1] * 8 for i in range(8)]
		rank = 0
		fild = 0
		for idx,char in enumerate(FEN_state):
			if char == '/':
				rank +=1
				fild=0
				continue

			if char == ' ':
				player=FEN_state[idx+1]
				castle_variables = FEN_state[idx+3:idx+7]
				idx +=8
				char = FEN_state[idx]
				last_move=char
				idx+=1
				char=FEN_state[idx]
				while char != ' ':
					last_move +=char
					idx+=1
					char = FEN_state[idx]
				idx+=1
				stale_moves = int(FEN_state[idx])
				idx+=2
				full_moves = int(FEN_state[idx])
				break


			if char.isdigit():
				for num in range(int(char)):
					state[rank][fild] = 'e'
					fild +=1
			else:		 
				state[rank][fild] = self.translate_FEN_name(char)
				fild+=1
		print(state)
		print(player, castle_variables, last_move, stale_moves, full_moves)
		

	def translate_FEN_name(self, name):
		#From 'b' to 'r' in ASCII.
		if name.islower():
			return 'b'+name.upper()
		#From 'B' to 'R' in ASCII.	
		if name.isupper():
			return 'w'+ name

	def is_checkmate(self):
		print(self.players[(self.current_player+1)%2], " won!!!")
		command = []
		while command != 'y':
			command = input(" Restart game? y / n")
		self.reset()
		
	def main_loop(self):
		'''Main loop, playable chess.'''
		self.current_player = 0
		player_option = -1
		MINMAX_DEPTH = 3

		print("\t\tSimple Chess\n\t\t  Welcome!\nTo move piecese, type the command in a 4 letter format: \n   row from, column from, row to, column to.")
		while player_option not in (1, 2, 3): 
			player_option = int(input(" Choose the players: \n 1: Player vs Player \n 2: Player vs AI \n 3: AI vs AI \n Choose option 1, 2 or 3:"))
			print(player_option)

		while (1):
			print(self.players[self.current_player]+"'s turn.")
			board = self.Board.get_state()
			castle_variables = self.Board.get_castle_variables()
			self.draw(board)
			#AI vs AI
			if player_option == 3:
				AI_move = self.AI.minmax(MINMAX_DEPTH,
										board,
										castle_variables,
										self.current_player)
				if AI_move[1] == None:
					self.is_checkmate()
				self.Board.move_piece(AI_move[1])
				self.change_player()
				self.Rules.set_up(board,
								castle_variables,
								self.players[self.current_player])	
			#Human vs AI
			elif player_option == 2:
				if self.current_player:
					command = input(" Next move? ")
					self.execute_command(command)
				elif not self.current_player:
					self.Board.move_piece(self.AI.minmax(MINMAX_DEPTH,
														board,
														castle_variables,
														self.current_player)[1])
					self.change_player()
				self.Rules.set_up(board,
								castle_variables,
								self.players[self.current_player])
			#Human vs Human
			elif player_option == 1:
				command = input(" Next move? ")
				self.execute_command(command)
				self.current_player = (self.current_player+1)%2
				self.Rules.set_up(board,
								castle_variables,
								self.players[self.current_player])

			if self.Rules.is_in_check():
				if self.Rules.is_checkmate():
					self.is_checkmate()
				print(self.players[self.current_player]+" king is in check!")
			
			if self.Rules.is_stalemate():
				print("Stalemate, tie!")
				command = []
				while command != 'y':
					command = input(" Restart game? y / n")
				self.reset()

			
game = ChessMain()
game.main_loop()		
