import math
from classes.board import Board
from classes.minimax import minimax


def main():
    first_board = Board()
    first_board.add_builder("AI", [0, 0], -1)
    first_board.add_builder("AI", [0, 1], -2)
    first_board.add_builder("HU", [3, 4], -3)
    first_board.add_builder("HU", [4, 4], -4)
    first_board.board_state[1][4] = 4
    first_board.board_state[2][3] = 4
    first_board.builders[0].move_to([2, 3], first_board.board_state)
    #print(first_board)
    print(minimax(first_board, True, 3, None, None, None, -math.inf, math.inf))


if __name__ == '__main__':
    main()
