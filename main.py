from classes.board import Board
from classes.builder import Builder


def main():
    first_board = Board()
    b1 = Builder("Human", [0, 3], first_board.board)
    b2 = Builder("AI", [1, 2], first_board.board)
    first_board.board[1][4] = 4
    first_board.board[2][3] = 4

    print(first_board.get_valid_builds([1, 3], first_board.get_all_valid_moves(first_board.board)))
    print(first_board)
    b2.move_to([0, 0], first_board.board)
    b2.build([0, 1], first_board.board)
    b2.build([0, 1], first_board.board)
    b2.build([0, 1], first_board.board)
    print(first_board)
    b2.move_to([0, 1], first_board.board)
    print(first_board)
    b2.move_to([0, 0], first_board.board)
    print(first_board)


if __name__ == '__main__':
    main()
