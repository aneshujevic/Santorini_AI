from functools import lru_cache

from .builder import Builder


# save builders as a number in matrix instead of using isinstance

# -4, -3 human builders
# -2, -1 AI builders
class Board:
    def __init__(self, board_state=None):
        self.not_available_cells_values = [-4, -3, -2, -1, 4]
        if board_state is None:
            self.board_state = [[0 for _ in range(5)] for _ in range(5)]
        else:
            self.board_state = [[self.board_state[x][y] for x in range(5)] for y in range(5)]

        self.builders = []

    def __str__(self):
        text_representation = ''
        for x in range(5):
            for y in range(5):
                text_representation += f'{self.board_state[x][y]}\t'
            text_representation += '\n'
        return text_representation

    def print_board(self):
        print(self)

    def add_builder(self, coordinates, affiliation, builder_id):
        self.builders.append(Builder(affiliation, coordinates, self.board_state, builder_id))

    def clone(self):
        new_board_object = Board(self.board_state)
        for builder in self.builders:
            new_board_object.add_builder(builder.coordinates, builder.affiliation, builder.id)

        return new_board_object

    def is_terminal_state(self, all_available_moves):
        for builder in self.builders:
            if builder.previous_value_of_cell == 3:
                return True
        if (Board.get_valid_moving_moves(self.builders[0].coordinates, self.board_state, all_available_moves) is None and
            Board.get_valid_moving_moves(self.builders[1].coordinates, self.board_state, all_available_moves) is None) or \
                (Board.get_valid_moving_moves(self.builders[2].coordinates, self.board_state, all_available_moves) is None and
                 Board.get_valid_moving_moves(self.builders[3].coordinates, self.board_state, all_available_moves) is None):
            return True
        else:
            return False

    def check_win(self, all_available_moves):
        for builder in self.builders:
            if builder.previous_value_of_cell == 3:
                return f"{builder.affiliation} has won!"

        if Board.get_valid_moving_moves(self.builders[0].coordinates, self.board_state, all_available_moves) is None and \
                Board.get_valid_moving_moves(self.builders[1].coordinates, self.board_state, all_available_moves) is None:
            return "Human won!"
        elif Board.get_valid_moving_moves(self.builders[2].coordinates, self.board_state, all_available_moves) is None and \
                Board.get_valid_moving_moves(self.builders[3].coordinates, self.board_state, all_available_moves) is None:
            return "AI won!"

    # returns tuple of all available moves
    def get_all_available_moves(self):
        return tuple([
            [x, y] for x in range(5) for y in range(5)
            if not self.board_state[x][y] in self.not_available_cells_values
        ])

    # returns a tuple of valid build moves
    @staticmethod
    def get_valid_builds(starting_location, board_state, all_available_moves):
        start_x = starting_location[0]
        start_y = starting_location[1]

        range_x = Board.get_range_x(start_x)
        range_y = Board.get_range_y(start_y)

        valid_building_moves = [
            [start_x + x - 1, start_y + y - 1]
            for x in range(range_x[0], range_x[1])
            for y in range(range_y[0], range_y[1])
            if [start_x + x - 1, start_y + y - 1] in all_available_moves
        ]

        return tuple(valid_building_moves)

    # returns a tuple of valid moving moves
    @staticmethod
    def get_valid_moving_moves(starting_location, board_state, all_available_moves):
        start_x = starting_location[0]
        start_y = starting_location[1]

        range_x = Board.get_range_x(start_x)
        range_y = Board.get_range_y(start_y)

        valid_moving_moves = [
            [start_x + x - 1, start_y + y - 1]
            for x in range(range_x[0], range_x[1])
            for y in range(range_y[0], range_y[1])
            if [start_x + x - 1, start_y + y - 1] in all_available_moves and
            board_state[start_x][start_y].previous_value - board_state[start_x + x - 1][start_y + y - 1] >= -1
        ]

        return tuple(valid_moving_moves)

    @staticmethod
    def get_range_x(x):
        if x == 0:
            range_x = [1, 3]
        elif x == 4:
            range_x = [0, 2]
        else:
            range_x = [0, 3]
        return range_x

    @staticmethod
    def get_range_y(y):
        if y == 0:
            range_y = [1, 3]
        elif y == 4:
            range_y = [0, 2]
        else:
            range_y = [0, 3]
        return range_y
