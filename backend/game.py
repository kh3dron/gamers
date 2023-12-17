import numpy as np

class Go:
    
    def __init__(self, board_size):
        self.board_size = board_size
        self.board = np.zeros((board_size, board_size), dtype=int)
        self.player = 1 # 1 = black, 2 = white
        
        self.ended = False
        
        self.moves = []
        self.captured_black = 0
        self.captured_white = 0

    def __str__(self):
        return str(self.board)
    
    def show(self):
        print("   ", end="")
        for col_label in range(self.board_size):
            print(f" {col_label} ", end="")
        print("\n   " + "---" * self.board_size)
        
        for i in range(self.board_size):
            print(f"{i}| ", end="")
            for j in range(self.board_size):
                if self.board[i, j] == 0:
                    print('🟧 ', end='')
                elif self.board[i, j] == 1:
                    print('⬛ ', end='')
                else:
                    print('⬜ ', end='')
            print()
        print()
        
    def is_empty(self, i, j):
        return self.board[i, j] == 0
    
    def place_stone(self, i, j):

        if self.is_empty(i, j):
            self.board[i, j] = self.player
            self.moves.append((i, j))
            self.process_captures(1 if self.player == 2 else 2)
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
        
    def get_possible_moves(self):
            
            open = np.array(self.board == 0, dtype=int)
            
            for i in range(self.board_size):
                for j in range(self.board_size):
                    if self.is_empty(i, j):
                        open[i, j] = self.is_empty(i, j)
                        
            if len(self.moves) > 1:
                open[self.moves[-1]] = False
            return open

    def get_groups(self, color):
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

    def get_liberties(self, color):
        # Returns an array with 1 for each cell that is a liberty of the group

        groups = self.get_groups(color)
        count_groups = groups.max()
        liberties = np.zeros(shape=(count_groups, self.board_size, self.board_size), dtype=int)
        
        for g in range(1, count_groups + 1):
            first_cell = np.where(groups == g)
            _, l = self._dfs(color, first_cell[0][0], first_cell[1][0], set())
            for x, y in l:
                liberties[g-1, x, y] = 1
            
        return liberties
    
    def process_captures(self, color):
        # for each group of this color, check if it has 0 liberties. 
        # If so, remove the group and add the number of stones to the captured stones count.
        groups = self.get_groups(color)
        liberties = self.get_liberties(color)
        
        
        for g in range(1, groups.max() + 1):
            if liberties[g-1].sum() == 0: #a group has been surrounded!
                for i in range(self.board_size):
                    for j in range(self.board_size):
                        if groups[i, j] == g:
                            self.board[i, j] = 0
                            if color == 1:
                                self.captured_black += 1
                            else:
                                self.captured_white += 1
        return

    def get_winner(self):
    
        # count all 1s and 2s on the board
        black = np.count_nonzero(self.board == 1) + self.captured_black
        white = np.count_nonzero(self.board == 2) + self.captured_white
        
        if black > white:
            return 1
        elif white > black:
            return 2
        else:
            return 0

    def stone_scores(self):
        # return JSON of stones on board and captured stones
        return {
            "white_deployed": np.count_nonzero(self.board == 2),
            "black_deployed": np.count_nonzero(self.board == 1),
            "captured_black": self.captured_black,
            "captured_white": self.captured_white,
            "black_total": np.count_nonzero(self.board == 1) + self.captured_black,
            "white_total": np.count_nonzero(self.board == 2) + self.captured_white
        }

    def drawable(self):

        ans = self.board.copy()

        if self.board_size == 9:
            startp = [[4, 4]]
        elif self.board_size == 13:
            startp = [[3, 3], [3, 9], [6, 6], [9, 3], [9, 9]]
        else:
            startp = [[3, 3], [3, 9], [3, 15], [9, 3], [9, 9], [9, 15], [15, 3], [15, 9], [15, 15]]

        for i in range(len(startp)):
            if self.board[startp[i][0]][startp[i][1]] == 0:
                ans[startp[i][0]][startp[i][1]] = 11


        for i in range(self.board_size):
            if self.board[0, i] == 0:
                ans[0, i] = 3
            if self.board[self.board_size - 1, i] == 0:
                ans[self.board_size - 1, i] = 4
            if self.board[i, 0] == 0:
                ans[i, 0] = 5
            if self.board[i, self.board_size - 1] == 0:
                ans[i, self.board_size - 1] = 6

        if ans[0][0] == 5:
            ans[0][0] = 7
        if ans[0][self.board_size - 1] == 3:
            ans[0][self.board_size - 1] = 8
        if ans[self.board_size - 1][0] == 5:
            ans[self.board_size - 1][0] = 9
        if ans[self.board_size - 1][self.board_size - 1] == 6:
            ans[self.board_size - 1][self.board_size - 1] = 10

        return ans.tolist()