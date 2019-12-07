from classes.board import Board
from classes.builder import Builder


def main():
    first_board = Board()
    first_board.board[0][3] = Builder()
    first_board.board[1][2] = Builder()
    first_board.board[1][4] = 4
    first_board.board[2][3] = 4

    print(first_board.get_valid_builds([1, 3], first_board.get_all_valid_moves(first_board.board)))


if __name__ == '__main__':
    main()
