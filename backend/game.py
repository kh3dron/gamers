import numpy as np


class Go:
    def __init__(self, board_size):
        self.board_size = board_size

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

        state0 = self.board[:, :, 0]
        state1 = self.board[:, :, 1]

        if self.board[0, 0, 16] == 1:  # if current player is black
            ret[state0 == 1] = 1
            ret[state1 == 1] = 2
        else:
            ret[state0 == 1] = 2
            ret[state1 == 1] = 1

        return ret

    def is_empty(self, i, j):
        return self.board[i, j, 0] == 0 and self.board[i, j, 8] == 0

    # This function assumes the move is valid, IE not on an existing stone or KO violation.
    # Passes are handled as a move to (-1, -1). 
    def place_stone(self, i, j):

        if self.ended:
            return

        if self.board[i, j, 0] == 1 or self.board[i, j, 1] == 1:
            raise Exception("Illegal Move")

        # bump historic states down by 2
        self.board[:, :, 2:16] = self.board[:, :, 0:14]

        # place stone in current player's frame. IF pass, no new stone is placed.
        if not (i == -1 and j == -1):
            self.board[i, j, 0] = 1

        # alternate current player: switch frames 0:1, 2:3, 4:5, etc
        for e in range(0, 16, 2):
            temp_slice = self.board[:, :, e].copy()
            self.board[:, :, e] = self.board[:, :, e+1]
            self.board[:, :, e+1] = temp_slice
        
        # switch state layer 16
        self.board[:, :, 16] = 0 if self.board[0, 0, 16] == 1 else 1

        # add move to history
        self.moves.append((i, j))
        if self.moves[-2:] == [(-1, -1), (-1, -1)]:
            self.ended = True

        self.crunch_board_state()

        return

    def place_stone_sequence(self, sequence):
        for move in sequence:
            self.place_stone(move[0], move[1])

    def get_possible_moves(self):
        flat = self.board[:, :, 0] + self.board[:, :, 1]
        if len(self.moves) > 1:
            flat[self.moves[-1]] = 1
        return flat == 0

    def get_groups(self, frame):
        groups = np.zeros((self.board_size, self.board_size), dtype=int)
        visited = set()
        group_number = 1

        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i, j, frame] == 1 and (i, j) not in visited:
                    stack = [(i, j)]
                    group = set()

                    while stack:
                        x, y = stack.pop()

                        if (x, y) not in visited:
                            visited.add((x, y))
                            group.add((x, y))
                            
                            for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
                                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                                    if self.board[nx, ny, frame] == 1 and (nx, ny) not in visited:
                                        stack.append((nx, ny))

                    for x, y in group:
                        groups[x, y] = group_number

                    group_number += 1

        return groups

    def get_liberties(self, frame):
        groups = self.get_groups(frame)

        occupied_stones = self.board[:, :, 0] + self.board[:, :, 1]

        count_groups = groups.max()
        liberties = np.zeros(shape=(count_groups, self.board_size, self.board_size), dtype=int)

        for g in range(1, count_groups + 1):
            group_indices = np.where(groups == g)
            adjacent_stones = set()
            
            for x, y in zip(group_indices[0], group_indices[1]):
                for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
                    if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                        adjacent_stones.add((nx, ny))
            
            # Remove duplicates and eliminate occupied stones
            liberties_indices = set(adjacent_stones) - set(zip(group_indices[0], group_indices[1]))
            liberties_indices = [(x, y) for x, y in liberties_indices if occupied_stones[x, y] == 0]
            
            # Write to liberties array
            for x, y in liberties_indices:
                liberties[g-1, x, y] = 1

        return liberties

    def process_captures(self, frame):
        groups = self.get_groups(frame)
        liberties = self.get_liberties(frame)

        for e in range(len(liberties)): 
            if liberties[e, :, :].sum() == 0:

                # set all stones in group to 0 on the board
                group = np.where(groups == e+1)
                self.board[group[0], group[1], frame] = 0

                if frame == 0:
                    self.captured_black += len(group[0])
                else:
                    self.captured_white += len(group[0])
        return

    def crunch_board_state(self):
        # See if current player has capatured any stones
        self.process_captures(frame=0)
        # See if any ataris have been created
        #self.process_captures(frame=0)

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
        state = self.show()

        scores = {
            "game_over": self.ended,
            "white_alive": np.count_nonzero(state == 2),
            "black_alive": np.count_nonzero(state == 1),
            "captured_black": self.captured_black,
            "captured_white": self.captured_white,
            "black_total_points": np.count_nonzero(state == 1) + self.captured_white,
            "white_total_points": np.count_nonzero(state == 2) + self.captured_black,
        }

        return scores

    def drawable(self):
        ans = self.show()

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
            if ans[startp[i][0]][startp[i][1]] == 0:
                ans[startp[i][0]][startp[i][1]] = 11

        for i in range(self.board_size):
            if ans[0, i] == 0:
                ans[0, i] = 3
            if ans[self.board_size - 1, i] == 0:
                ans[self.board_size - 1, i] = 4
            if ans[i, 0] == 0:
                ans[i, 0] = 5
            if ans[i, self.board_size - 1] == 0:
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
