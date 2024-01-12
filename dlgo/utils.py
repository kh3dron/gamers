from dlgo import gotypes
import numpy as np

COLS = "ABCDEFGHJKLMNOPQRST"
STONE_TO_CHAR = {
    None: " . ",
    gotypes.Player.black: " x ",
    gotypes.Player.white: " o ",
}


def print_move(player, move):
    if move.is_pass:
        move_str = "passes"
    elif move.is_resign:
        move_str = "resigns"
    else:
        move_str = "%s%d" % (COLS[move.point.col - 1], move.point.row)
    print("%s %s" % (player, move_str))

def print_board(board):
    for row in range(board.num_rows, 0, -1):
        bump = " " if row <= 9 else ""
        line = []
        for col in range(1, board.num_cols + 1):
            stone = board.get(gotypes.Point(row=row, col=col))
            line.append(STONE_TO_CHAR[stone])
        print("%s%d %s" % (bump, row, "".join(line)))
    print("    " + "  ".join(COLS[: board.num_cols]))

def point_from_coords(coords):
    col = COLS.index(coords[0]) + 1
    row = int(coords[1:])
    return gotypes.Point(row=row, col=col)

def view_boardtiles(board):

    ans = np.zeros((board.num_rows, board.num_rows), dtype=int)

    for i, row in enumerate(range(board.num_rows, 0, -1)):
        for j, col in enumerate(range(1, board.num_cols + 1)):
            stone = board.get(gotypes.Point(row=row, col=col))
            if stone == gotypes.Player.black:
                ans[i][j] = 1
            elif stone == gotypes.Player.white:
                ans[i][j] = 2

    if board.num_rows == 9:
        startp = [[4, 4]]
    elif board.num_rows == 13:
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

    for i in range(board.num_rows):
        if ans[0, i] == 0:
            ans[0, i] = 3
        if ans[board.num_rows - 1, i] == 0:
            ans[board.num_rows - 1, i] = 4
        if ans[i, 0] == 0:
            ans[i, 0] = 5
        if ans[i, board.num_rows - 1] == 0:
            ans[i, board.num_rows - 1] = 6

    if ans[0][0] == 3:
        ans[0][0] = 7
    if ans[0][board.num_rows - 1] == 6:
        ans[0][board.num_rows - 1] = 8
    if ans[board.num_rows - 1][0] == 4:
        ans[board.num_rows - 1][0] = 9
    if ans[board.num_rows - 1][board.num_rows - 1] == 4:
        ans[board.num_rows - 1][board.num_rows - 1] = 10

    return ans.tolist()


# TODO
def stone_scores(board):
    black = 0
    white = 0
    for row in range(board.num_rows, 0, -1):
        for col in range(1, board.num_cols + 1):
            stone = board.get(gotypes.Point(row=row, col=col))
            if stone == gotypes.Player.black:
                black += 1
            elif stone == gotypes.Player.white:
                white += 1
    return {
        "black stones": black,
        "white stones": white,
    }