from .builder import Builder
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
        """
        :param id_of_builder: ID of builder that is on the move
        :param move_coords: Coordinates to which builder is being moved
        :param build_coords: Coordinates on which builder is building
        :return:
        """
        for builder in self.builders:
            if builder.id == id_of_builder:
                builder.move_and_build(move_coords, build_coords, self)

    def clone(self):
        new_board_object = Board(self.board_state)
        for builder in self.builders:
            new_board_object.add_builder(builder.affiliation, builder.coordinates, builder.id).previous_value_of_cell = builder.previous_value_of_cell
        return new_board_object

    def is_terminal_state(self):
        all_available_moves = self.get_all_available_moves()
        if self.game_over or self.check_win(all_available_moves) != 0:
            return True
        return False

    # 1 means AI won -1 mean HU won
    def check_win(self, all_available_moves):
        """
        :param all_available_moves: All moves that are available on board
        :return: 1 if AI won -1 if HU won
        """
        for builder in self.builders:
            if builder.previous_value_of_cell == 3:
                return 1 if builder.affiliation == "AI" else -1

        if not self.check_player_can_move(True, all_available_moves):
            print("ne more se pomeri human")
            return 1
        elif not self.check_player_can_move(False, all_available_moves):
            print("ne more se pomeri ai")
            return -1

        return 0

    def check_player_can_move(self, human, all_available_moves):
        """
        :param human: is player human
        :param all_available_moves: all available moves
        :return: True if player can move False otherwise
        """
        # first two builders are AI second two are Human
        if human:
            lower_bound, upper_bound = 2, 4
        else:
            lower_bound, upper_bound = 0, 2

        for id in range(lower_bound, upper_bound):
            # One move exists so we know that player can move
            for _ in Board.get_valid_moving_moves(self.builders[id].coordinates, self, all_available_moves):
                return True
        return False

    # returns list of all available moves
    def get_all_available_moves(self):
        return [
            [x, y]
            for x in range(5)
            for y in range(5)
            if self.board_state[x][y] not in self.not_available_cells_values
        ]

    @staticmethod
    def get_valid_builds(starting_location, all_available_moves):
        """
        :param starting_location: Starting coordinates of a builder that is on the move
        :param all_available_moves: List of all available moves
        :return: Coordinates of a build
        """
        start_x = starting_location[0] - 1
        start_y = starting_location[1] - 1

        range_x = Board.get_range_axis(start_x)
        range_y = Board.get_range_axis(start_y)

        for x in range(range_x[0], range_x[1]):
            for y in range(range_y[0], range_y[1]):
                final_build_coords = [start_x + x, start_y + y]
                if not final_build_coords == starting_location and final_build_coords in all_available_moves:
                    yield final_build_coords

    # returns a list of valid moving moves
    @staticmethod
    def get_valid_moving_moves(starting_location, board_object, all_available_moves):
        """
        :param starting_location: Starting coordinates of a builder that is on the move
        :param board_object: Board object
        :param all_available_moves: List of all available moves
        :return: Coordinates of a build
        """
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
                final_move_coords = [start_x + x, start_y + y]
                if final_move_coords in all_available_moves and final_move_coords != starting_location and \
                        board_state[final_move_coords[0]][final_move_coords[1]] - previous_value_of_current_cell <= 1:
                    yield final_move_coords

    @staticmethod
    def get_range_axis(z):
        """
        :param z: Ordinate
        :return: Range for given ordinate
        """
        if z == -1:
            range_z = [1, 3]
        elif z == 3:
            range_z = [0, 2]
        else:
            range_z = [0, 3]
        return range_z
