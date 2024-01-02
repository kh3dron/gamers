from dlgo.gotypes import *


def is_point_an_eye(board, point, color):
    if board.get(point) is not None:
        return False
    for neighbor in point.neighbors():
        if board.is_on_grid(neighbor):
            neighbor_color = board.get(neighbor)
            if neighbor_color != color:
                return False
            friendly_corners = 0
            off_board_corners = 0
    corners = [
        Point(point.row - 1, point.col - 1),
        Point(point.row - 1, point.col + 1),
        Point(point.row + 1, point.col - 1),
        Point(point.row + 1, point.col + 1),
    ]
    for corner in corners:
        if board.is_on_grid(corner):
            corner_color = board.get(corner)
            if corner_color == color:
                friendly_corners += 1
        else:
            off_board_corners += 1
    if off_board_corners > 0:
        return off_board_corners + friendly_corners == 4
    return friendly_corners >= 3


def best_result(game_state):
    if game_state.is_over():
        if game_state.winner() == game_state.next_player:
            return GameResult.win
        elif game_state.winner() is None:
            return GameResult.draw
    else:
        return GameResult.loss
    best_result_so_far = GameResult.loss
    for candidate_move in game_state.legal_moves():
        next_state = game_state.apply_move(candidate_move)
        opponent_best_result = best_result(next_state)
        our_result = reverse_game_result(opponent_best_result)
        if our_result.value > best_result_so_far.value:
            best_result_so_far = our_result
    return best_result_so_far

def capture_diff(game_state):
    black_stones = 0
    white_stones = 0
    for r in range(1, game_state.board.num_rows + 1):
        for c in range(1, game_state.board.num_cols + 1):
            p = gotypes.Point(r, c)
        color = game_state.board.get(p)
        if color == gotypes.Player.black:
            black_stones += 1
        elif color == gotypes.Player.white:
            white_stones += 1
        diff = black_stones - white_stones
        if game_state.next_player == gotypes.Player.black:
            return diff
    return -1 * diff

def best_result(game_state, max_depth, eval_fn):
    if game_state.is_over():
        if game_state.winner() == game_state.next_player:
            return MAX_SCORE
        else:
            return MIN_SCORE
    if max_depth == 0:
        return eval_fn(game_state)
    
    best_so_far = MIN_SCORE
    for candidate_move in game_state.legal_moves():
        next_state = game_state.apply_move(candidate_move)
        opponent_best_result = self.best_result(
        next_state, max_depth - 1, eval_fn)
        our_result = -1 * opponent_best_result
        if our_result > best_so_far:
            best_so_far = our_result
        return best_so_far