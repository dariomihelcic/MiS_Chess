import copy


'''
Promotion set do default Q.
'''
class ChessBoard:
	def __init__(self, board = None):
		'''
		Initialize variables for state and history.
		Optional argument:
		board -- initialize state of specific board.
		'''
		self.state = []
		self.last_state = []
		self.last_state_variables = [[False] * 6 ]

		self.state = self.create_board()
		if board:
			self.set_state(board)
		#self.history.append(copy.deepcopy(self.state))

		self.wK_moved = False
		self.bK_moved = False
		self.wR_Qs_moved = False
		self.wR_Ks_moved = False
		self.bR_Qs_moved = False
		self.bR_Ks_moved = False


	def get_state(self):
		return self.state

	def set_state(self, board):
		self.state = [[1] * 8 for i in range(8)]
		for row in range(8):
				for col in range(8):
					self.state[row][col]=board[row][col]

	def get_last_state(self):
		return self.last_state

	def set_last_state(self, board):
		self.last_state = [[1] * 8 for i in range(8)]
		for row in range(8):
				for col in range(8):
					self.last_state[row][col]=board[row][col]

	def get_castle_variables(self):
		'''
		Return kings_moved and rooks_moved list.
		'''
		return 	[self.wK_moved, self.bK_moved, self.wR_Qs_moved, self.wR_Ks_moved, self.bR_Qs_moved, self.bR_Ks_moved]


	def set_castle_variables(self, last_castle_variables):
		self.wK_moved = last_castle_variables[0]
		self.bK_moved = last_castle_variables[1]
		self.wR_Qs_moved = last_castle_variables[2]
		self.wR_Ks_moved = last_castle_variables[3]
		self.bR_Qs_moved = last_castle_variables[4]
		self.bR_Ks_moved = last_castle_variables[5]


	def create_board(self):
		'''Return list of lists representing the starting board'''
		board = [[1] * 8 for i in range(8)]
		board[0] = ['bR','bN','bB','bQ','bK','bB','bN','bR']
		board[1] = ['bP','bP','bP','bP','bP','bP','bP','bP']
		board[2] = ['e','e','e','e','e','e','e','e']
		board[3] = ['e','e','e','e','e','e','e','e']
		board[4] = ['e','e','e','e','e','e','e','e']
		board[5] = ['e','e','e','e','e','e','e','e']
		board[6] = ['wP','wP','wP','wP','wP','wP','wP','wP']
		board[7] = ['wR','wN','wB','wQ','wK','wB','wN','wR']
		return board

	def create_board(self):
		'''Return list of lists representing the starting board'''
		board = [[1] * 8 for i in range(8)]
		board[0] = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR']
		board[1] =  ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP']
		board[2] =  ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e']
		board[3] = ['e','e','e','e','e','e','e','e']
		board[4] = ['e','e','e','e','e','e','e','e']
		board[5] = ['e','e','e','e','e','e','e','e']
		board[6] = ['wP','wP','wP','wP','wP','wP','wP','wP']
		board[7] = ['wR','wN','wB','wQ','wK','wB','wN','wR']
		return board

	def change_state(self, board):
		self.state = self.copy_board(board)

	def reset_board(self):
		'''Puts state to starting board, clears history.'''
		self.state = self.create_board()
		self.last_state = self.state
		self.reset_castle_variables()

	def reset_castle_variables(self):
		self.wK_moved = False
		self.bK_moved = False
		self.wR_Qs_moved = False
		self.wR_Ks_moved = False
		self.bR_Qs_moved = False
		self.bR_Ks_moved = False

	def undo_move(self):
		'''Set state to state before move, delete last history entry.'''
		if not self.last_state:
			print("No past moves.")
			return False
		self.set_state(self.last_state)
		self.set_castle_variables(self.last_castle_variables)
		return True

	def set_piece(self, piece, to_row, to_col):
		self.state[to_row][to_col] = piece

	def move_piece(self, move):
		'''Change position of pieces in state.
		Calls methods pawn_promotion and en_passant
		'''
		self.set_last_state(self.state)
		self.last_castle_variables = self.get_castle_variables()

		from_row = move[0][0]
		from_col = move[0][1]
		to_row = move[1][0]
		to_col = move[1][1]

		from_piece = self.state[from_row][from_col]
		to_piece = self.state[to_row][to_col]

		self.state[to_row][to_col] = from_piece
		self.state[from_row][from_col] = 'e'
		
		if 'P' in from_piece:
			self.pawn_promotion(from_piece, to_row, to_col)
			self.en_passant(from_piece, to_row, to_col)
		if 'R' in from_piece:
			self.rook_moved(from_row, from_col)
		if 'K' in from_piece:
			self.king_moved(from_piece)
			if abs(from_col-to_col)==2:
				self.castle_move(from_piece, to_piece, to_col)
		if from_piece == (0,0):
			print(ok)

	def pawn_promotion(self, from_piece, to_row, to_col):
		'''Checks if pawn is in position for a promotion.'''
		if 'wP' in from_piece and to_row == 0:
			if 1:
				self.state[to_row][to_col] = 'wQ'
				return
			piece_type = 'P'
			while piece_type not in ('Q', 'B', 'N', 'R'):
				piece_type = input("Promote pawn to Q-B-N-R?")
			self.state[to_row][to_col] = 'w' + piece_type
		if 'bP' in from_piece and to_row == 7:
			if 1:
				self.state[to_row][to_col] = 'bQ'
				return
			piece_type = 'P'
			while piece_type not in ('Q', 'B', 'N', 'R'):
				piece_type = input("Promote pawn to Q-B-N-R?")
			self.state[to_row][to_col] = 'b' + piece_type

	def en_passant(self, from_piece, to_row, to_col):
		'''If pown was eaten en passant, remove that pown.'''
		try:
			if 'wP' in from_piece and \
			   'bP' in self.state[to_row+1][to_col]:
				self.state[to_row+1][to_col] = 'e'
			if 'bP' in from_piece and \
			   'wP' in self.state[to_row-1][to_col]:
				self.state[to_row-1][to_col] = 'e'
		#corner pawns
		except IndexError:
			pass

	def rook_moved(self, row, col):
		if row == 0 and col == 0:
			self.bR_Qs_moved = True
		elif row == 0 and col == 7:
			self.bR_Ks_moved = True
		elif row == 7 and col == 7:
			self.wR_Qs_moved = True
		elif row == 7 and col == 0:
			self.wR_Ks_moved = True

	def king_moved(self, from_piece):
		if 'wK' in from_piece and not self.wK_moved:
			self.wK_moved = True
		if 'bK' in from_piece and not self.bK_moved:
			self.bK_moved = True

	def castle_move(self, from_piece, to_piece, to_col):
		if 'wK' in from_piece:
			if to_col==2:
				move =((7,0),(7,3)) 
				self.move_piece(move)
			if to_col==6:
				move =((7,7),(7,5)) 
				self.move_piece(move)
		if 'bK' in from_piece:
			if to_col==2:
				move =((0,0),(0,3)) 
				self.move_piece(move)
			if to_col==6:
				move =((0,7),(0,5)) 
				self.move_piece(move)

'''	def can_castle(self):
		if 'wK' in from_piece:
			if to_col==2 and not self.wR_Qs_moved and not self.wK_moved:
				return True
			if to_col==6 and not self.wR_Ks_moved and not self.wK_moved:
				return True
		if 'bK' in from_piece:
			if to_col==2 and not self.bR_Qs_moved and not self.bK_moved:
				return True
			if to_col==6 and not self.bR_Ks_moved and not self.bK_moved:
				return True
		return False'''


