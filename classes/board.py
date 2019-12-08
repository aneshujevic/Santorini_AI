from .builder import Builder


class Board:
    def __init__(self):
        self.board = [[0 for x in range(5)] for y in range(5)]

    def __str__(self):
        text_representation = ''
        for x in range(5):
            for y in range(5):
                text_representation += f'{self.board[x][y]}\t'
            text_representation += '\n'
        return text_representation

    def print_board(self):
        print(self)

    # returns a tuple of all valid moves
    # could be bottleneck
    @staticmethod
    def get_all_valid_moves(board_state):
        list_of_moves = []

        for i in range(5):
            for j in range(5):
                if board_state[i][j] != 4 and not isinstance(board_state[i][j], Builder):
                    list_of_moves.append([i, j])

        return tuple(list_of_moves)

    # returns a tuple of valid build moves
    @staticmethod
    def get_valid_builds(starting_location, all_valid_moves):
        valid_building_moves = []
        start_x = starting_location[0]
        start_y = starting_location[1]

        for x in range(3):
            for y in range(3):
                if start_x + x - 1 < 0 or start_x + x + 1 > 5 or start_y + y - 1 < 0 or start_y + y + 1 > 5:
                    pass
                if [start_x + x - 1, start_y + y - 1] in all_valid_moves:
                    valid_building_moves.append([start_x + x - 1, start_y + y - 1])
        valid_building_moves.remove(starting_location)

        return tuple(valid_building_moves)

    # returns a tuple of valid moving moves
    @staticmethod
    def get_valid_moving_moves(starting_location, board_state, all_valid_moves):
        valid_moving_moves = []
        start_x = starting_location[0]
        start_y = starting_location[1]

        for x in range(3):
            for y in range(3):
                if start_x + x - 1 < 0 or start_x + x + 1 > 4 or start_y + y - 1 < 0 or start_y + y + 1 > 4:
                    pass
                if board_state[start_x][start_y] - board_state[start_x + x - 1][start_y + y - 1] >= -1 and\
                        [start_x + x - 1, start_y + y - 1] in all_valid_moves:
                    valid_moving_moves.append([start_x + x - 1, start_y + y - 1])
        valid_moving_moves.remove(starting_location)

        return tuple(valid_moving_moves)
