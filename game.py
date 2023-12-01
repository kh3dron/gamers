import numpy as np

class Go:
    
    def __init__(self, board_size):
        self.board_size = board_size
        self.board = np.zeros((board_size, board_size))
        self.player = 1 # 1 = black, 2 = white
        
        self.ended = False
        
        self.moves = []
        self.captured_black = 0
        self.captured_white = 0
        
    def is_empty(self, i, j):
        return self.board[i, j] == 0
    
    def place_stone(self, i, j):
        if self.is_empty(i, j):
            self.board[i, j] = self.player
            self.moves.append((i, j))
        else:
            raise Exception('Invalid move: ({}, {}) occupied'.format(i, j))        
        
        self.player = 1 if self.player == 2 else 2

    def pass_turn(self):
        if self.moves and self.moves[-1] == (-1, -1): #double pass
            self.ended = True
        else:
            self.moves.append((-1, -1))
            self.player = 1 if self.player == 2 else 2
        
        return
    
    def get_winner(self):
        if self.captured_black > self.captured_white:
            return 1