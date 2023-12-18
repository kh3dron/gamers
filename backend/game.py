import numpy as np


class Go:
    def __init__(self, board_size):
        self.board_size = board_size

        """
        Each 2 layers represent a state of the board, the current player's stones and the opponent's stones.
        These 8 pairs of layers are stacked on top of each other to form a tensor of shape (board_size, board_size, 16).
        The last layer is a single layer of shape (board_size, board_size) that represents the current player - 1 for black, 0 for white.
        Last layer starts with 1s since black goes first.
        """

        self.board = np.zeros((board_size, board_size, 17), dtype=int)
        self.board[:, :, 16] = 1

        self.ended = False

        self.moves = []
        self.captured_black = 0
        self.captured_white = 0
        self.player = self.board[0, 0, 16]



    def __str__(self):
        return str(self.board.tolist())

    def show(self):
        ret = np.zeros((self.board_size, self.board_size), dtype=int)
        state1 = self.board[:, :, 0]
        state2 = self.board[:, :, 8]

        if self.board[0, 0, 16] == 1:  # if current player is black
            ret[state1 == 1] = 1
            ret[state2 == 1] = 2
        else:
            ret[state1 == 1] = 2
            ret[state2 == 1] = 1

        return ret.tolist()

    def is_empty(self, i, j):
        return self.board[i, j, 0] == 0 and self.board[i, j, 8] == 0

    # This function assumes the move is valid, IE not on an existing stone or KO violation.
    # Passes are handled as a move to (-1, -1). 
    def place_stone(self, i, j):

        # bump historic states down by 2
        self.board[:, :, 2:16] = self.board[:, :, 0:14]

        # place stone in current player's frame. IF pass, no new stone is placed.
        if not i == -1 and j == -1:
            self.board[i, j, 0] = 1

        # alternate current player: switch frames 0:1, 2:3, 4:5, etc
        self.board[:, :, 0:14:2], self.board[:, :, 1:15:2] = self.board[:, :, 1:15:2], self.board[:, :, 0:14:2]

        # switch state layer 16
        self.board[:, :, 16] = 0 if self.board[0, 0, 16] == 1 else 1

        # add move to history
        self.moves.append((i, j))

    def get_possible_moves(self):
        opens = self.board[:, :, 0] == 0 and self.board[:, :, 1] == 0
        if len(self.moves) > 1:
            opens[self.moves[-1]] = False
        return opens

    def get_groups(self, frame):
        groups = np.zeros((self.board_size, self.board_size), dtype=int)
        visited = set()
        group_number = 1

        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i, j, frame] == 1 and (i, j) not in visited:
                    group, liberty_set = self._dfs(i, j, frame, visited)

                    for x, y in group:
                        groups[x, y] = group_number

                    group_number += 1

        return groups

    def _dfs(self, start_x, start_y, frame, visited):
        group = set()
        liberty_set = set()
        stack = [(start_x, start_y)]

        while stack:
            x, y = stack.pop()
            if (x, y) not in visited:
                visited.add((x, y))
                group.add((x, y))

                for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
                    if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                        if self.board[nx, ny, frame] == 0:
                            liberty_set.add((nx, ny))

                for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
                    if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                        if self.board[nx, ny, frame] == 1:
                            stack.append((nx, ny))

        return group, liberty_set

    def get_liberties(self, frame):
        groups = self.get_groups(frame)
        opponent_frame = 1 if frame == 0 else 0

        count_groups = groups.max()
        liberties = np.zeros(shape=(count_groups, self.board_size, self.board_size), dtype=int)

        for g in range(1, count_groups + 1):
            first_cell = np.where(groups == g)
            _, l = self._dfs(first_cell[0][0], first_cell[1][0], opponent_frame, set())
            for x, y in l:
                liberties[g-1, x, y] = 1

        return liberties


    def process_captures(self, frame):
        groups = self.get_groups(frame)
        liberties = self.get_liberties(frame)

        for g in range(1, groups.max() + 1):
            if liberties[g-1].sum() == 0:
                for i in range(self.board_size):
                    for j in range(self.board_size):
                        if groups[i, j] == g:
                            self.board[i, j, frame] = 0

                            if frame == 0:
                                if self.board[i, j, 16] == 1:
                                    self.captured_black += 1
                                else:
                                    self.captured_white += 1
                            else:
                                if self.board[i, j, 16] == 1:
                                    self.captured_white += 1
                                else:
                                    self.captured_black += 1
        return

    def crunch_board_state(self):
        # See if current player has capatured any stones
        self.process_captures(frame=0)
        # See if any ataris have been created
        self.process_captures(frame=1)


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
            "white_total": np.count_nonzero(self.board == 2) + self.captured_white,
        }

    def drawable(self):
        ans = self.board.copy()

        if self.board_size == 9:
            startp = [[4, 4]]
        elif self.board_size == 13:
            startp = [[3, 3], [3, 9], [6, 6], [9, 3], [9, 9]]
        else:
            startp = [
                [3, 3],
                [3, 9],
                [3, 15],
                [9, 3],
                [9, 9],
                [9, 15],
                [15, 3],
                [15, 9],
                [15, 15],
            ]

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
