import math
import os

from classes.board import Board
from classes.minimax import minimax


def main():
    first_board = Board()
    first_board.add_builder("AI", [0, 0], -2)
    first_board.add_builder("AI", [0, 4], -1)
    first_board.add_builder("HU", [3, 4], -4)
    first_board.add_builder("HU", [4, 4], -3)
    """
    
    first_board.board_state[0][2] = 4
    first_board.board_state[1][1] = 4
    first_board.board_state[1][2] = 4
    """

    first_board.board_state[3][3] = 3
    first_board.board_state[4][3] = 2

    while True:
        print(first_board)
        if not first_board.check_win(first_board.get_all_available_moves()) is None:
            break

        id_string = input("enter id of player:")
        id_of_builder = int(id_string)

        move_to = input("enter move-to coordinates").split(' ')
        move_coords = list(map(int, move_to))

        build_on = input("enter build-on coordinates").split(' ')
        build_coords = list(map(int, build_on))

        first_board.do_move(id_of_builder, move_coords, build_coords)

        move = minimax(first_board, True, 4, None, None, None, -math.inf, math.inf)
        first_board.do_move(move[0], move[1], move[2])
        print(move)
        # os.system("clear")


if __name__ == '__main__':
    main()
