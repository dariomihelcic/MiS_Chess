from ChessBoard import ChessBoard
from ChessRules import ChessRules
import random
from time import sleep
from random import shuffle


class ChessAI:
	SLEEP_TIME = 3

	def __init__(self):
		self.Rules = ChessRules()
		self.stale_move = []

	def get_list_moves(self, board, castle_variables, player):
		list_moves = []
		if player:
			for row in range(8):
				for col in range(8):
					#Only for black pieces
					if 'b' in board[row][col]:
						from_position = (row, col)

						self.Rules.set_up(board, castle_variables, 'Black')
						list_to_position = self.Rules.get_valid_moves((row,col))

						for to_position in list_to_position:
							list_moves.append((from_position, to_position))
		if not player:
			for row in range(8):
				for col in range(8):
					#Only for white pieces
					if 'w' in board[row][col]:
						from_position = (row, col)

						self.Rules.set_up(board, castle_variables, 'White')
						list_to_position = self.Rules.get_valid_moves((row,col))

						for to_position in list_to_position:
							list_moves.append((from_position, to_position))
		return list_moves						

	def silly_bot(self, castle_variables, board, player):
		list_moves = self.get_list_moves(board, castle_variables, player)
		move = random.choice(list_moves)
		return move


	def evaluate_board(self, board, player):
		piece_value = {'bP': -10, 'bN': -30, 'bB': -30, 'bR': -50, 'bQ': -90, 'bK': -900,
					   'wP': 10, 'wN': 30, 'wB': 30, 'wR': 50, 'wQ': 90, 'wK': 900}
		score = 0
		for row in range(8):
			for col in range(8):
				if board[row][col] != 'e':
					score += piece_value[board[row][col]]
		return score

	def eating_bot(self, castle_variables, board, player):
		list_moves = self.get_list_moves(board, castle_variables, player)
		best_move = ((),())
		FakeBoard = ChessBoard(board)
		
		if player:
			#If black move.
			best_score = 9999
			for move in list_moves:

				FakeBoard.move_piece(move)
				current_score = self.evaluate_board(FakeBoard.get_state(), player)
				if current_score < best_score:
					best_move = move
					best_score = current_score
				FakeBoard.undo_move()
			sleep(self.SLEEP_TIME-1)
			return best_move

		if not player:
			#If white move.
			best_score = -9999
			for move in list_moves:

				FakeBoard.move_piece(move)
				current_score = self.evaluate_board(FakeBoard.get_state(), player)
				if current_score > best_score:
					best_move = move
					best_score = current_score
				FakeBoard.undo_move()
			sleep(self.SLEEP_TIME-1)
			return best_move

		
		

	def minmax(self, depth, board, castle_variables, player, alpha=-9999, beta=9999):
		if depth == 0:
			return (self.evaluate_board(board, player), None)

		FakeBoard = ChessBoard(board)
		best_move = None
		list_moves = self.get_list_moves(board, castle_variables, player)
		shuffle(list_moves)

		white_boring_move = [None]*4
		black_boring_move = [None]*4

		if player:
			#If black move.
			current_score = 9999
			best_score = 9999
			if black_boring_move[0]==black_boring_move[2] and \
			   black_boring_move[1]==black_boring_move[3] and \
			   black_boring_move[0] != None:
				list_moves.remove(black_boring_move)
			for move in list_moves:
				FakeBoard.move_piece(move)
				current_score = min(current_score,
									self.minmax(depth-1,
												FakeBoard.get_state(),
												castle_variables,
												not player,
												alpha,
												beta)[0])
				if current_score < best_score:
					best_move = move
					best_score = current_score
				FakeBoard.undo_move()
				beta = min(beta, current_score)
				if beta <= alpha:
					self.update_boring_moves(black_boring_move, best_move)
					return (best_score, best_move)
			self.update_boring_moves(black_boring_move, best_move)

		if not player:
			#If white move.
			current_score = -9999
			best_score = -9999
			if white_boring_move[0]==white_boring_move[2] and \
			   white_boring_move[2]==white_boring_move[3] and\
			   white_boring_move[0] != None:
				list_moves.remove(white_boring_move[0])
			for move in list_moves:
				FakeBoard.move_piece(move)
				current_score = max(current_score, self.minmax(depth-1, FakeBoard.get_state(), castle_variables , not player, alpha, beta)[0])
				if current_score > best_score:
					best_move = move
					best_score = current_score
				FakeBoard.undo_move()
				alpha = max(alpha, current_score)
				if beta <= alpha:
					self.update_boring_moves(white_boring_move, best_move)
					return (best_score, best_move)
			self.update_boring_moves(white_boring_move, best_move)

		return (best_score, best_move)

	def update_boring_moves(self, list, move):
		list[0] = list[1]
		list[1] = list[2]
		list[2] = list[3]
		list[3] = move








