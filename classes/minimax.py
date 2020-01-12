import math
from .board import Board


# TODO: Check near-win state move_coords being null
def minimax(board_obj, maximizing_player, depth, builder_number, move_coords, build_coords, alpha, beta):
    """
    player 0 is AI (maximizing player)
    player 1 is Human (minimizing player)
    :param board_obj: Object of class board
    :param maximizing_player: Which player is it (0 - AI, 1 - HU)
    :param depth: The depth of the search tree
    :param builder_number: The number of builder of the player
    :param move_coords: Coordinates of move
    :param build_coords: Coordinates of build
    :param alpha: Alpha value needed for pruning
    :param beta: Beta value needed for pruning
    :return: List with [builder number, move, build, best score]
    """
    if maximizing_player:
        if board_obj.is_terminal_state() or depth == 0:
            return [builder_number, move_coords, build_coords,
                    static_eval(board_obj, move_coords, build_coords)]
    else:
        if board_obj.is_terminal_state() or depth == 0:
            return [builder_number, move_coords, build_coords,
                    -static_eval(board_obj, move_coords, build_coords)]

    all_available_moves = board_obj.get_all_available_moves()

    if maximizing_player:
        max_eval = [-1, -1, -1, -math.inf]
        builders_id = (-1, -2)

        for builder_no in range(2):
            for move in Board.get_valid_moving_moves(board_obj.builders[builder_no].coordinates, board_obj, all_available_moves):
                for build in Board.get_valid_builds(move, all_available_moves):
                    # TODO: here should the move be done on a copy of a board object by builder with appropriate id doing the move
                    if build == move:
                        continue
                    board_copy = board_obj.clone()
                    board_copy.do_move(builders_id[builder_no], move, build)
                    evaluation = minimax(board_copy, False, depth - 1, builder_no, move, build, alpha, beta)
                    if evaluation[3] > max_eval[3]:
                        max_eval[0] = builders_id[builder_no]
                        max_eval[1] = move
                        max_eval[2] = build
                        max_eval[3] = evaluation[3]
                    alpha = max(alpha, max_eval[3])
                    # TODO: Check if return instead of break
                    if beta <= alpha:
                        return max_eval
        return max_eval
    else:
        min_eval = [-1, -1, -1, math.inf]
        builders_id = (-3, -4)

        for builder_no in range(2):
            for move in Board.get_valid_moving_moves(board_obj.builders[builder_no + 2].coordinates, board_obj, all_available_moves):
                for build in Board.get_valid_builds(move, all_available_moves):
                    if build == move:
                        continue
                    board_copy = board_obj.clone()
                    board_copy.do_move(builders_id[builder_no], move, build)
                    evaluation = minimax(board_copy, True, depth - 1, builder_no, move, build, alpha, beta)
                    if evaluation[3] < min_eval[3]:
                        min_eval[0] = builders_id[builder_no]
                        min_eval[1] = move
                        min_eval[2] = build
                        min_eval[3] = evaluation[3]
                    beta = min(beta, min_eval[3])
                    if beta <= alpha:
                        return min_eval
        return min_eval


def static_eval(board_obj, move_coords, build_coords):
    if not move_coords or not build_coords:
        return 0
    m = board_obj.board_state[move_coords[0]][move_coords[1]]
    ai_distance = 0
    hu_distance = 0
    b_x = build_coords[0]
    b_y = build_coords[1]

    if board_obj.board_state[b_x][b_y] == 0:
        return m

    for i in [-1, -2]:
        ai_distance += max(
            math.fabs(board_obj.builders[i].coordinates[0] - b_x),
            math.fabs(board_obj.builders[i].coordinates[1] - b_y)
        )

    for i in [-3, -4]:
        hu_distance += max(
            math.fabs(board_obj.builders[i].coordinates[0] - b_x),
            math.fabs(board_obj.builders[i].coordinates[1] - b_y)
        )

    length = board_obj.board_state[b_x][b_y] * math.fabs(ai_distance - hu_distance)

    return m + length
