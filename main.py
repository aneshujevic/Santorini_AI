from classes.board import Board
from classes.builder import Builder


def main():
    first_board = Board()
    first_board.board[1][4] = 4
    first_board.board[2][3] = 4

    print(first_board.get_valid_builds(first_board.builders[3].coordinates, first_board.board))
    print(first_board)
    first_board.builders[1].move_to([1, 1], first_board.board)
    print(first_board)


if __name__ == '__main__':
    main()
