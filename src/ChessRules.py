
class ChessRules:
	def __init__(self):
		'''Set instance method for en passant moves.'''
		self.en_passant = (-1, None)

	def set_up(self, board, castle_variables, current_player):
		'''Called before using other methods.
		Sets instance methods for:
		The board setting rules are cheked on.
		The color of the current player.
		'''
		self.board = board
		self.kings_moved = castle_variables[:2]
		self.rooks_moved = castle_variables[-4:]
		if current_player == "Black":
			self.player_color = 'b'
			self.enemy_color = 'w'
		else:
			self.player_color = 'w'
			self.enemy_color = 'b'

	def get_list_moves(self):
		list_moves = []
		if self.player_color == 'b':
			for row in range(8):
				for col in range(8):
					#Only for black pieces
					if 'b' in self.board[row][col]:
						from_position = (row, col)
						list_to_position = self.get_valid_moves((row,col))

						for to_position in list_to_position:
							list_moves.append((from_position, to_position))
		if self.player_color == 'w':
			for row in range(8):
				for col in range(8):
					#Only for white pieces
					if 'w' in self.board[row][col]:
						from_position = (row, col)
						list_to_position = self.get_valid_moves((row,col))

						for to_position in list_to_position:
							list_moves.append((from_position, to_position))

		return list_moves	

	def is_checkmate(self):
		'''Check if current player is in checkmate.
		Call get_valid_moves for every piece of current player.
		Return True if there are no valid moves.
		'''
		player_valid_moves = []
		for row in range(8):
			for col in range(8):
				if self.player_color in self.board[row][col]:
					player_valid_moves.extend(self.get_valid_moves((row,col)))	
		
		if len(player_valid_moves) == 0:
			return True
		else:
			return False

	def get_valid_moves(self, from_position):
		'''Returns a list of valid moves'''
		legal_to_positions = []
		for row in range(8):
			for col in range(8):
				to_position = (row,col)
				if self.is_legal_move(from_position, to_position):
					if not self.results_in_check(from_position, to_position):
						legal_to_positions.append(to_position)
		return legal_to_positions

	def is_legal_move(self, from_position, to_position):
		'''Check if move from_position to to_position is valid.
		Implements rules for chess pieces.
		Returns True or False.
		'''
		from_row = from_position[0]
		from_col = from_position[1]
		to_row = to_position[0]
		to_col = to_position[1]
		from_piece = self.board[from_row][from_col]
		to_piece = self.board[to_row][to_col]

		#Remove possible en passant on players next move.
		if self.player_color == self.en_passant[1]:
		 	self.en_passant = (-1, "none")

		if from_position == to_position:
			return False

		if 'P' in from_piece:
			#Pawn
			if self.player_color == 'b':
				#moving forward one space
				if to_row == from_row+1 and \
				   to_col == from_col and \
				   to_piece == 'e':
					return True
				#moving forvard 2 spaces
				if from_row == 1 and \
				   to_row == from_row+2 and \
				   to_col == from_col and \
				   self.is_clear_path(from_position, to_position) and \
				   to_piece == 'e':
					self.en_passant = (to_col, self.player_color)
					return True
				#eating
				if to_row == from_row+1 and \
				   (to_col == from_col+1 or to_col == from_col-1) and \
				   (self.enemy_color in to_piece or \
				   (to_piece == 'e' and to_col == self.en_passant[0])):
					return True
			elif self.player_color == 'w':
				#moving forward one space
				if to_row == from_row-1 and \
				   to_col == from_col and \
				   to_piece == 'e':
					return True
				#moving forvard 2 spaces
				if from_row == 6 and \
				   to_row == from_row-2 and \
				   to_col == from_col and \
				   self.is_clear_path(from_position, to_position) and \
				   to_piece == 'e':
					self.en_passant = (to_col, self.player_color)
					return True
				#eating
				if to_row == from_row-1 and \
				   (to_col == from_col+1 or to_col == from_col-1) and \
				   (self.enemy_color in to_piece or \
				   (to_piece == 'e' and to_col == self.en_passant[0])):
					return True

		elif 'R' in from_piece:
			#Rook
			if (to_row == from_row or to_col == from_col) and \
			   (to_piece == 'e' or self.enemy_color in to_piece):
				if self.is_clear_path(from_position, to_position):
					return True

		elif 'N' in from_piece:
			#Knight
			col_diff = to_col - from_col
			row_diff = to_row - from_row
			if (to_piece == 'e' or self.enemy_color in to_piece) and \
			   (col_diff*col_diff + row_diff*row_diff == 5):
					return True

		elif 'B' in from_piece:
			#Bishop
			if (abs(to_row - from_row) == abs(to_col - from_col)) and \
			   (to_piece == 'e' or self.enemy_color in to_piece):
				if self.is_clear_path(from_position, to_position):
					return True

		elif 'Q' in from_piece:
			#Queen
			if (abs(to_row - from_row) == abs(to_col - from_col)) and \
			   (to_piece == 'e' or self.enemy_color in to_piece):
				if self.is_clear_path(from_position, to_position):
					return True
			if (to_row == from_row or to_col == from_col) and \
			   (to_piece == 'e' or self.enemy_color in to_piece):
				if self.is_clear_path(from_position, to_position):
					return True

		elif 'K' in from_piece:
			#King
			col_diff = to_col - from_col
			row_diff = to_row - from_row
			if abs(col_diff) + abs(row_diff) == 1 or (abs(col_diff)==1 and abs(row_diff)==1):
				return True
			#Castling
			if 'wK' in from_piece and self.player_color == 'w':
				#White Castle
				if to_col==2 and not self.rooks_moved[0] and not self.kings_moved[0]:
					if self.is_clear_path((7,4), (7,0)) and not self.would_be_check(7,4,2,-1) and not self.is_in_check():
						return True
				if to_col==6 and not self.rooks_moved[1] and not self.kings_moved[0]:
					if self.is_clear_path((7,4), (7,7)) and not self.would_be_check(7,4,6,1) and not self.is_in_check():
						return True
			if 'bK' in from_piece and self.player_color == 'b':
				#Black Castle
				if to_col==2 and not self.rooks_moved[2] and not self.kings_moved[1]:
					if self.is_clear_path((0,4), (0,0)) and not self.would_be_check(0,4,2,-1) and not self.is_in_check():
						return True
				if to_col==6 and not self.rooks_moved[3] and not self.kings_moved[1]:
					if self.is_clear_path((0,4), (0,7)) and not self.would_be_check(0,4,6,1) and not self.is_in_check():
						return True
		return False

	def results_in_check(self, from_position, to_position):
		'''Check if a move results in self check.
		Makes the move, calls is_in_check on resulting board, undos move.
		Returns True or False.
		'''
		from_row = from_position[0]
		from_col = from_position[1]
		to_row = to_position[0]
		to_col = to_position[1]
		from_piece = self.board[from_row][from_col]
		to_piece = self.board[to_row][to_col]

		self.board[to_row][to_col] = from_piece
		self.board[from_row][from_col] = 'e'

		check = self.is_in_check()

		self.board[to_row][to_col] = to_piece
		self.board[from_row][from_col] = from_piece

		return check

	def is_in_check(self):
		'''
		Check current players king is in check.
		First, find current players king.
		Second, check if enemy has legal moves to king.
		'''
		king_position = (0,0)
		#Find the players king
		for row in range(8):
			for col in range(8):
				piece = self.board[row][col]
				if 'K' in piece and self.player_color in piece:
					king_position = (row,col)

		#is_legal_move checks for valid moves for player_color
		#Exchange of values needed.
		self.enemy_color, self.player_color = self.player_color, self.enemy_color
		for row in range(8):
			for col in range(8):
				piece = self.board[row][col]
				if self.player_color in piece:
					if self.is_legal_move((row,col), king_position):
						self.enemy_color, self.player_color = self.player_color, self.enemy_color
						return True

		self.enemy_color, self.player_color = self.player_color, self.enemy_color
		return False

	def is_stalemate(self):
		black_pieces = 0
		white_pieces = 0
		for row in range(8):
			for col in range(8):
				piece = self.board[row][col]
				if 'b' in piece:
					black_pieces+=1
				if 'w' in piece:
					white_pieces+=1
		if (black_pieces == 1 and white_pieces == 1) or self.get_list_moves()==None:
			return True
		return False 

	def would_be_check(self, king_row, king_col, col_to, direction):
		nudge = 1 * direction
		king_position = (king_row, king_col+nudge)
		self.enemy_color, self.player_color = self.player_color, self.enemy_color
		
		for row in range(8):
			for col in range(8):
				piece = self.board[row][col]
				if 'K' in piece:
					continue
				if self.player_color in piece:
					if self.is_legal_move((row,col), king_position):
						self.enemy_color, self.player_color = self.player_color, self.enemy_color
						return True
		
		king_position = (king_row, king_col+nudge*2)
		for row in range(8):
			for col in range(8):
				piece = self.board[row][col]
				if 'K' in piece:
					continue
				if self.player_color in piece:
					if self.is_legal_move((row,col), king_position):
						self.enemy_color, self.player_color = self.player_color, self.enemy_color
						return True
		self.enemy_color, self.player_color = self.player_color, self.enemy_color
		return False



	def is_clear_path(self, from_position, to_position):
		'''Check if all positions between the from_position and to_position are empty.
		Check for all 9 directions, recursively.
		Returns True or false.
		'''
		from_row = from_position[0]
		from_col = from_position[1]
		to_row = to_position[0]
		to_col = to_position[1]
		from_piece = self.board[from_row][from_col]

		if abs(from_row - to_row) <= 1 and \
		   abs(from_col - to_col) <= 1:
			return True
		else:
			if to_row > from_row and to_col == from_col:
				new_position = (from_row+1, from_col)
			elif to_row < from_row and to_col == from_col:
				new_position = (from_row-1, from_col)
			elif to_row == from_row and to_col > from_col:
				new_position = (from_row, from_col+1)
			elif to_row == from_row and to_col < from_col:
				new_position = (from_row, from_col-1)
			elif to_row > from_row and to_col > from_col:
				new_position = (from_row+1, from_col+1)
			elif to_row > from_row and to_col < from_col:
				new_position = (from_row+1, from_col-1)
			elif to_row < from_row and to_col > from_col:
				new_position = (from_row-1, from_col+1)
			elif to_row < from_row and to_col < from_col:
				new_position = (from_row-1, from_col-1)
		if self.board[new_position[0]][new_position[1]] != 'e':
			return False
		else:
			return self.is_clear_path(new_position,to_position)



