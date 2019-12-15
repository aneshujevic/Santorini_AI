import math
from classes.board import Board
from classes.minimax import minimax


def main():
    first_board = Board()
    first_board.board_state[1][4] = 4
    first_board.board_state[2][3] = 4
    first_board.builders[0].move_to([2, 3], first_board.board_state)
    #print(first_board)
    print(minimax(first_board, True, 3, None, None, None, -math.inf, math.inf))


if __name__ == '__main__':
    main()
