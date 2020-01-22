from functools import lru_cache
from math import fabs

from .builder import Builder


# save builders as a number in matrix instead of using isinstance

# -4, -3 human builders
# -2, -1 AI builders
class Board:
    def __init__(self, board_state=None):
        """
        :param board_state: a matrix from which the board should be made
        """
        self.not_available_cells_values = (-4, -3, -2, -1, 4)
        if board_state is None:
            self.board_state = [[0 for _ in range(5)] for _ in range(5)]
        else:
            self.board_state = [[board_state[y][x] for x in range(5)] for y in range(5)]

        self.builders = []
        self.game_over = False

    def __str__(self):
        text_representation = ''
        for x in range(5):
            for y in range(5):
                text_representation += f'{self.board_state[x][y]}\t'
            text_representation += '\n'
        return text_representation

    def print_board(self):
        print(self)

    def add_builder(self, affiliation, coordinates, builder_id):
        """
        :param affiliation: string that represents affiliation (AI or HU)
        :param coordinates: list of coordinates [x, y]
        :param builder_id: integer that represents id of builder
        :return: reference to a builder
        """
        new_builder = Builder(affiliation, coordinates, self.board_state, builder_id)
        self.builders.append(new_builder)
        return new_builder

    def do_move(self, id_of_builder, move_coords, build_coords):
        for builder in self.builders:
            if builder.id == id_of_builder:
                last_builder_coords = builder.coordinates
                builder.move_and_build(move_coords, build_coords, self)
                return [id_of_builder, last_builder_coords, build_coords]

    def undo_move(self, last_move):
        for builder in self.builders:
            if builder.id == last_move[0]:
                builder.move_to(last_move[1], self)
                self.board_state[last_move[2][0]][last_move[2][1]] -= 1
                break

    def clone(self):
        new_board_object = Board(self.board_state)
        for builder in self.builders:
            new_board_object.add_builder(builder.affiliation, builder.coordinates, builder.id)
        return new_board_object

    def is_terminal_state(self):
        all_available_moves = self.get_all_available_moves()
        if self.game_over:
            return True
        if (not Board.get_valid_moving_moves(self.builders[0].coordinates, self, all_available_moves) and
            not Board.get_valid_moving_moves(self.builders[1].coordinates, self, all_available_moves)) or \
                (not Board.get_valid_moving_moves(self.builders[2].coordinates, self, all_available_moves) and
                 not Board.get_valid_moving_moves(self.builders[3].coordinates, self, all_available_moves)):
            return True
        else:
            return False

    # 1 means AI won -1 mean HU won
    def check_win(self, all_available_moves):
        for builder in self.builders:
            if builder.previous_value_of_cell == 3:
                return 1 if builder.affiliation == "AI" else -1

        if Board.get_valid_moving_moves(self.builders[0].coordinates, self, all_available_moves) == [] and \
                Board.get_valid_moving_moves(self.builders[1].coordinates, self, all_available_moves) == []:
            print("ne more se pomeri human")
            return 1
        elif Board.get_valid_moving_moves(self.builders[2].coordinates, self, all_available_moves) == [] and \
                Board.get_valid_moving_moves(self.builders[3].coordinates, self, all_available_moves) == []:
            print("ne more se pomeri ai")
            return -1

        return 0

    # returns list of all available moves
    def get_all_available_moves(self):
        return [
            [x, y]
            for x in range(5)
            for y in range(5)
            if not self.board_state[x][y] in self.not_available_cells_values
        ]

    @staticmethod
    def get_valid_builds(starting_location, all_available_moves):
        start_x = starting_location[0] - 1
        start_y = starting_location[1] - 1

        range_x = Board.get_range_axis(start_x)
        range_y = Board.get_range_axis(start_y)

        for x in range(range_x[0], range_x[1]):
            for y in range(range_y[0], range_y[1]):
                if not [start_x + x, start_y + y] == starting_location and \
                        [start_x + x, start_y + y] in all_available_moves:
                    yield [start_x + x, start_y + y]

    # returns a list of valid moving moves
    @staticmethod
    def get_valid_moving_moves(starting_location, board_object, all_available_moves):
        start_x = starting_location[0] - 1
        start_y = starting_location[1] - 1

        board_state = board_object.board_state

        range_x = Board.get_range_axis(start_x)
        range_y = Board.get_range_axis(start_y)

        previous_value_of_current_cell = 0
        for builder in board_object.builders:
            if builder.coordinates == starting_location:
                previous_value_of_current_cell = builder.previous_value_of_cell
                break

        for x in range(range_x[0], range_x[1]):
            for y in range(range_y[0], range_y[1]):
                if [start_x + x, start_y + y] in all_available_moves and \
                        not [start_x + x, start_y + y] == starting_location and \
                        board_state[start_x + x][start_y + y] - previous_value_of_current_cell <= 1:
                    yield [start_x + x, start_y + y]

    @staticmethod
    def get_range_axis(z):
        if z == -1:
            range_z = [1, 3]
        elif z == 4:
            range_z = [0, 2]
        else:
            range_z = [0, 3]
        return range_z
