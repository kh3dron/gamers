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
        
    def __str__(self):
        return str(self.board)
        
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
        
    def get_groups(self, color):
        # Returns a tuple of two matrices, one for the groups and one for the liberties. 
        # The group matrix contains a unique number for each group of stones of the same color.
        # The liberties matrix contains a count of liberties for each group.

        groups = np.zeros((self.board_size, self.board_size), dtype=int)
        visited = set()
        group_number = 1

        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i, j] == color and (i, j) not in visited:
                    group, liberty_set = self._dfs(color, i, j, visited)

                    # Assign group number to the group cells
                    for x, y in group:
                        groups[x, y] = group_number

                    group_number += 1

        return groups

    def _dfs(self, color, start_x, start_y, visited):
        group = set()
        liberty_set = set()
        stack = [(start_x, start_y)]

        while stack:
            x, y = stack.pop()
            if (x, y) not in visited:
                visited.add((x, y))
                group.add((x, y))

                # Check and add liberties
                for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
                    if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                        if self.board[nx, ny] == 0:
                            liberty_set.add((nx, ny))

                # Check and add neighboring stones of the same color
                for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
                    if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                        if self.board[nx, ny] == color:
                            stack.append((nx, ny))

        return group, liberty_set

    def get_liberties(self, color, group):
        # Returns a 1 for each cell that is a liberty of the group
        liberties = np.zeros((self.board_size, self.board_size), dtype=int)

        for x, y in group:
            for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    if self.board[nx, ny] == 0:
                        liberties[nx, ny] = 1

        return liberties

        
    
    def get_winner(self):
        if self.captured_black > self.captured_white:
            return 1