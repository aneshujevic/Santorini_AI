# returns list of valid moves be it moving a worker or building a block
def get_valid_moves(starting_location, all_valid_moves):
    valid_moving_moves = []
    start_x = starting_location.x
    start_y = starting_location.y

    for x in range(3):
        for y in range(3):
            if [start_x + x - 1, start_y + y - 1] in all_valid_moves:
                valid_moving_moves.append([start_x + x - 1, start_y + y - 1])
    return valid_moving_moves


class Board:
    def __init__(self):
        self.board = [[0 for x in range(5)] for y in range(5)]

    def __str__(self):
        text_representation = ''
        for x in range(5):
            for y in range(5):
                text_representation += f'{self.board[x][y]}'
            text_representation += '\n'
        return text_representation

    def print_board(self):
        print(self.board)

    # returns a list of all moving moves
    def get_all_valid_moves(self):
        list_of_moves = []
        for i in range(5):
            for j in range(5):
                if self.board[i][j] == 0:
                    list_of_moves.append([i, j])
        return list_of_moves

    # returns a list of all valid build moves
    # TODO: implement Builder class
    def get_all_valid_builds(self):
        list_of_moves = []
        for i in range(5):
            for j in range(5):
                if self.board[i][j] != 3 and not self.board[i][j] is Builder:
                    list_of_moves.append([i, j])
        return list_of_moves
