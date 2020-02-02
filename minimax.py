import math
from .board import Board


def alpha_beta_custom(board_obj, maximizing_player, depth, builder_number, move_coords, build_coords, alpha, beta):
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
    if board_obj.is_terminal_state() or depth == 0:
        return [builder_number, move_coords, build_coords,
                static_eval_custom(board_obj, move_coords, build_coords)]

    all_available_moves = board_obj.get_all_available_moves()

    if maximizing_player:
        max_eval = [-1, -1, -1, -math.inf]
        builders_id = (-1, -2)

        for builder_no in range(2):
            should_break = False
            for move in Board.get_valid_moving_moves(board_obj.builders[builder_no].coordinates, board_obj,
                                                     all_available_moves):
                for build in Board.get_valid_builds(move, all_available_moves):
                    board_copy = board_obj.clone()
                    board_copy.do_move(builders_id[builder_no], move, build)
                    evaluation = alpha_beta_custom(board_copy, False, depth - 1, builder_no, move, build, alpha, beta)
                    if evaluation[3] > max_eval[3]:
                        max_eval[0] = builders_id[builder_no]
                        max_eval[1] = move
                        max_eval[2] = build
                        max_eval[3] = evaluation[3]
                    alpha = max(alpha, max_eval[3])
                    if beta <= alpha:
                        should_break = True
                        break
                if should_break:
                    break
        return max_eval
    else:
        min_eval = [-1, -1, -1, math.inf]
        builders_id = (-3, -4)

        for builder_no in range(2):
            should_break = False
            for move in Board.get_valid_moving_moves(board_obj.builders[builder_no + 2].coordinates, board_obj,
                                                     all_available_moves):
                for build in Board.get_valid_builds(move, all_available_moves):
                    board_copy = board_obj.clone()
                    board_copy.do_move(builders_id[builder_no], move, build)
                    evaluation = alpha_beta_custom(board_copy, True, depth - 1, builder_no, move, build, alpha, beta)
                    if evaluation[3] < min_eval[3]:
                        min_eval[0] = builders_id[builder_no]
                        min_eval[1] = move
                        min_eval[2] = build
                        min_eval[3] = evaluation[3]
                    beta = min(beta, min_eval[3])
                    if beta <= alpha:
                        should_break = True
                        break
                if should_break:
                    break
        return min_eval


def static_eval_custom(board_obj, move_coords, build_coords):
    """
        :param board_obj: Board object
        :param move_coords: Coordinates to which player moved
        :param build_coords: Coordinates to which player built
        :return:
    """
    all_available_moves = board_obj.get_all_available_moves()
    anyone_won = board_obj.check_win(all_available_moves)

    if anyone_won == 1:
        return 10000
    elif anyone_won == -1:
        return -10000

    b_x, b_y = build_coords
    build_blocks = board_obj.board_state[b_x][b_y]

    m_x, m_y = move_coords
    move_blocks = board_obj.board_state[m_x][m_y]
    for builder in board_obj.builders:
        if builder.id == move_blocks:
            move_blocks = builder.previous_value_of_cell
            break

    ai_distance = 0
    hu_distance = 0

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

    hu_level = board_obj.builders[2].previous_value_of_cell + board_obj.builders[3].previous_value_of_cell
    ai_level = board_obj.builders[0].previous_value_of_cell + board_obj.builders[1].previous_value_of_cell

    length = ai_distance - hu_distance

    return length * build_blocks + move_blocks * 10 + 15 * (ai_level - hu_level)


def alpha_beta_project(board_obj, maximizing_player, depth, builder_number, move_coords, build_coords, alpha, beta):
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
    if board_obj.is_terminal_state() or depth == 0:
        return [builder_number, move_coords, build_coords,
                static_eval_project(board_obj, move_coords, build_coords)]

    all_available_moves = board_obj.get_all_available_moves()

    if maximizing_player:
        max_eval = [-1, -1, -1, -math.inf]
        builders_id = (-1, -2)

        for builder_no in range(2):
            should_break = False
            for move in Board.get_valid_moving_moves(board_obj.builders[builder_no].coordinates, board_obj,
                                                     all_available_moves):
                for build in Board.get_valid_builds(move, all_available_moves):
                    board_copy = board_obj.clone()
                    board_copy.do_move(builders_id[builder_no], move, build)
                    evaluation = alpha_beta_project(board_copy, False, depth - 1, builder_no, move, build, alpha, beta)
                    if evaluation[3] > max_eval[3]:
                        max_eval[0] = builders_id[builder_no]
                        max_eval[1] = move
                        max_eval[2] = build
                        max_eval[3] = evaluation[3]
                    alpha = max(alpha, max_eval[3])
                    if beta <= alpha:
                        should_break = True
                        break
                if should_break:
                    break
        return max_eval
    else:
        min_eval = [-1, -1, -1, math.inf]
        builders_id = (-3, -4)

        for builder_no in range(2):
            should_break = False
            for move in Board.get_valid_moving_moves(board_obj.builders[builder_no + 2].coordinates, board_obj,
                                                     all_available_moves):
                for build in Board.get_valid_builds(move, all_available_moves):
                    board_copy = board_obj.clone()
                    board_copy.do_move(builders_id[builder_no], move, build)
                    evaluation = alpha_beta_project(board_copy, True, depth - 1, builder_no, move, build, alpha, beta)
                    if evaluation[3] < min_eval[3]:
                        min_eval[0] = builders_id[builder_no]
                        min_eval[1] = move
                        min_eval[2] = build
                        min_eval[3] = evaluation[3]
                    beta = min(beta, min_eval[3])
                    if beta <= alpha:
                        should_break = True
                        break
                if should_break:
                    break
        return min_eval


def minimax(board_obj, maximizing_player, depth, builder_number, move_coords, build_coords):
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
    if board_obj.is_terminal_state() or depth == 0:
        return [builder_number, move_coords, build_coords,
                static_eval_project(board_obj, move_coords, build_coords)]

    all_available_moves = board_obj.get_all_available_moves()

    if maximizing_player:
        max_eval = [-1, -1, -1, -math.inf]
        builders_id = (-1, -2)

        for builder_no in range(2):
            for move in Board.get_valid_moving_moves(board_obj.builders[builder_no].coordinates, board_obj,
                                                     all_available_moves):
                for build in Board.get_valid_builds(move, all_available_moves):
                    board_copy = board_obj.clone()
                    board_copy.do_move(builders_id[builder_no], move, build)
                    evaluation = minimax(board_copy, False, depth - 1, builder_no, move, build)
                    if evaluation[3] > max_eval[3]:
                        max_eval[0] = builders_id[builder_no]
                        max_eval[1] = move
                        max_eval[2] = build
                        max_eval[3] = evaluation[3]
        return max_eval
    else:
        min_eval = [-1, -1, -1, math.inf]
        builders_id = (-3, -4)

        for builder_no in range(2):
            for move in Board.get_valid_moving_moves(board_obj.builders[builder_no + 2].coordinates, board_obj,
                                                     all_available_moves):
                for build in Board.get_valid_builds(move, all_available_moves):
                    board_copy = board_obj.clone()
                    board_copy.do_move(builders_id[builder_no], move, build)
                    evaluation = minimax(board_copy, True, depth - 1, builder_no, move, build)
                    if evaluation[3] < min_eval[3]:
                        min_eval[0] = builders_id[builder_no]
                        min_eval[1] = move
                        min_eval[2] = build
                        min_eval[3] = evaluation[3]
        return min_eval


def static_eval_project(board_obj, move_coords, build_coords):
    """
    :param board_obj: Board object
    :param move_coords: Coordinates to which player moved
    :param build_coords: Coordinates to which player built
    :return:
    """
    b_x, b_y = build_coords
    build = board_obj.board_state[b_x][b_y]

    m_x, m_y = move_coords
    m = board_obj.board_state[m_x][m_y]
    for builder in board_obj.builders:
        if builder.id == m:
            m = builder.previous_value_of_cell
            break

    ai_distance = 0
    hu_distance = 0

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

    L = build * (ai_distance - hu_distance)
    return L + m
