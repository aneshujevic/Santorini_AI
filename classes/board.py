from functools import lru_cache

from .builder import Builder


class Board:
    def __init__(self):
        self.board_state = [[0 for x in range(5)] for y in range(5)]
        self.builders = []
        self.builders.append(Builder("AI", [0, 0], self.board_state))
        self.builders.append(Builder("AI", [0, 1], self.board_state))
        self.builders.append(Builder("HU", [4, 3], self.board_state))
        self.builders.append(Builder("HU", [4, 4], self.board_state))

    def __str__(self):
        text_representation = ''
        for x in range(5):
            for y in range(5):
                text_representation += f'{self.board_state[x][y]}\t'
            text_representation += '\n'
        return text_representation

    def print_board(self):
        print(self)

    def is_terminal_state(self):
        for builder in self.builders:
            if builder.previous_value == 3:
                return True
        if (Board.get_valid_moving_moves(self.builders[0].coordinates, self.board_state) is None and
            Board.get_valid_moving_moves(self.builders[1].coordinates, self.board_state) is None) or \
                (Board.get_valid_moving_moves(self.builders[2].coordinates, self.board_state) is None and
                 Board.get_valid_moving_moves(self.builders[3].coordinates, self.board_state) is None):
            return True
        else:
            return False

    def check_win(self):
        for builder in self.builders:
            if builder.previous_value == 3:
                return f"{builder.affiliation} has won!"

        if Board.get_valid_moving_moves(self.builders[0].coordinates, self.board_state) is None and \
                Board.get_valid_moving_moves(self.builders[1].coordinates, self.board_state) is None:
            return "Human won!"
        elif Board.get_valid_moving_moves(self.builders[2].coordinates, self.board_state) is None and \
                Board.get_valid_moving_moves(self.builders[3].coordinates, self.board_state) is None:
            return "AI won!"

    # returns a tuple of valid build moves
    @staticmethod
    def get_valid_builds(starting_location, board_state):
        valid_building_moves = []
        start_x = starting_location[0]
        start_y = starting_location[1]

        if start_x == 0:
            range_x = [1, 3]
        elif start_x == 4:
            range_x = [0, 2]
        else:
            range_x = [0, 3]

        if start_y == 0:
            range_y = [1, 3]
        elif start_y == 4:
            range_y = [0, 2]
        else:
            range_y = [0, 3]

        for x in range(range_x[0], range_x[1]):
            for y in range(range_y[0], range_y[1]):
                i = start_x + x
                j = start_y + y
                #   if i - 1 < 0 or i + 1 > 6 or j - 1 < 0 or j + 1 > 6:
                #       pass
                # elif in the next line
                if board_state[i - 1][j - 1] != 4 and not isinstance(board_state[i - 1][j - 1], Builder):
                    valid_building_moves.append([i - 1, j - 1])

        return tuple(valid_building_moves)

    # returns a tuple of valid moving moves
    @staticmethod
    def get_valid_moving_moves(starting_location, board_state):
        valid_moving_moves = []
        start_x = starting_location[0]
        start_y = starting_location[1]

        if start_x == 0:
            range_x = [1, 3]
        elif start_x == 4:
            range_x = [0, 2]
        else:
            range_x = [0, 3]

        if start_y == 0:
            range_y = [1, 3]
        elif start_y == 4:
            range_y = [0, 2]
        else:
            range_y = [0, 3]

        """ backup lolz
        for x in range(range_x[0], range_x[1]):
            for y in range(range_y[0], range_y[1]):
                i = start_x + x
                j = start_y + y
                #    if i - 1 < 0 or i - 1 > 4 or j - 1 < 0 or j - 1 > 4:
                #        pass
                # elif in the next line
                if not isinstance(board_state[i - 1][j - 1], Builder) and 
                        board_state[i - 1][j - 1] != 4 and 
                        board_state[start_x][start_y].previous_value - board_state[i - 1][j - 1] >= -1:
                    valid_moving_moves.append([i - 1, j - 1])
        """

        valid_moving_moves = [
            [start_x + x - 1, start_y + y - 1] for x in range(range_x[0], range_x[1]) for y in range(range_y[0], range_y[1])
            if not isinstance(board_state[start_x + x - 1][start_y + y - 1], Builder) and
               board_state[start_x + x - 1][start_y + y - 1] != 4 and
               board_state[start_x][start_y].previous_value - board_state[start_x + x - 1][start_y + y - 1] >= -1
        ]

        return tuple(valid_moving_moves)
