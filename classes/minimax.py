import math
from .board import Board


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
    :return: List with [builder number, move, build, best score]
    """
    if maximizing_player:
        if board_obj.is_terminal_state() or depth == 0:
            return [builder_number, move_coords, build_coords, static_eval(board_obj, tuple(move_coords), tuple(build_coords))]
    elif not maximizing_player:
        if board_obj.is_terminal_state() or depth == 0:
            return [builder_number, move_coords, build_coords, -static_eval(board_obj, tuple(move_coords), tuple(build_coords))]

    if maximizing_player:
        max_eval = [-1, -1, -1, -math.inf]
        builder_all_moves = []
        builder_all_builds = []

        for builder_no in range(2):
            builder_all_moves.append(Board.get_valid_moving_moves(board_obj.builders[builder_no].coordinates, board_obj.board_state))
            builder_all_builds.append([])

            length = len(builder_all_moves[builder_no])
            for i in range(length):
                builder_all_builds[builder_no].append(Board.get_valid_builds(board_obj.builders[builder_no].coordinates, board_obj.board_state))

        for builder_no in range(2):
            for move in builder_all_moves[builder_no]:
                for builds in builder_all_builds[builder_no]:
                    for build in builds:
                        evaluation = minimax(board_obj, 1, depth - 1, builder_no, move, build, alpha, beta)
                        if evaluation[3] > max_eval[3] and move != build:
                            max_eval[0] = builder_no
                            max_eval[1] = move
                            max_eval[2] = build
                            max_eval[3] = evaluation[3]
                        alpha = max(alpha, max_eval[3])
                        if beta <= alpha:
                            break
        return max_eval
    else:
        min_eval = [-1, -1, -1, math.inf]
        builder_all_moves = []
        builder_all_builds = []

        for builder_no in range(2):
            builder_all_moves.append(Board.get_valid_moving_moves(board_obj.builders[builder_no].coordinates, board_obj.board_state))
            builder_all_builds.append([])

            length = len(builder_all_moves[builder_no])
            for i in range(length):
                builder_all_builds[builder_no].append(Board.get_valid_builds(board_obj.builders[builder_no].coordinates, board_obj.board_state))

        for builder_no in range(2):
            for move in builder_all_moves[builder_no]:
                for builds in builder_all_builds[builder_no]:
                    for build in builds:
                        evaluation = minimax(board_obj, 0, depth - 1, builder_no, move, build, alpha, beta)
                        if evaluation[3] < min_eval[3] and move != build:
                            min_eval[0] = builder_no
                            min_eval[1] = move
                            min_eval[2] = build
                            min_eval[3] = evaluation[3]
                        beta = min(beta, min_eval[3])
                        if beta <= alpha:
                            break
        return min_eval


def static_eval(board_obj, move_coords, build_coords):
    m = board_obj.board_state[move_coords[0]][move_coords[1]]
    ai_distance = 0
    hu_distance = 0

    for i in range(2):
        ai_distance += math.sqrt(
            math.pow(board_obj.builders[i].coordinates[0] - build_coords[0], 2) +
            math.pow(board_obj.builders[i].coordinates[1] - build_coords[1], 2)
        )

    for i in range(2, 4):
        hu_distance += math.sqrt(
            math.pow(board_obj.builders[i].coordinates[0] - build_coords[0], 2) +
            math.pow(board_obj.builders[i].coordinates[1] - build_coords[1], 2)
        )

    length = board_obj.board_state[build_coords[0]][build_coords[1]] * math.fabs(ai_distance - hu_distance)

    return m + length
