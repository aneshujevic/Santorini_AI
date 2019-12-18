class Builder:
    # affiliation -> 0 should be for human, 1 should be for AI in general
    def __init__(self, affiliation, coordinates, board_state, id):
        self.affiliation = affiliation
        self.id = id
        self.previous_value_of_cell = 0
        self.coordinates = coordinates
        board_state[coordinates[0]][coordinates[1]] = id

    def __str__(self):
        return f"{self.affiliation}"

    # move to new coordinates and return the value of old cell on board
    def move_to(self, new_coordinates, board_object):
        board_state = board_object.board_state
        board_state[self.coordinates[0]][self.coordinates[1]] = self.previous_value_of_cell

        self.coordinates = new_coordinates
        self.previous_value_of_cell = board_state[self.coordinates[0]][self.coordinates[1]]
        board_state[self.coordinates[0]][self.coordinates[1]] = self.id

        if self.previous_value_of_cell == 3:
            board_object.game_over = True

    def __build(self, build_coords, board_object):
        x = build_coords[0]
        y = build_coords[1]
        board_object.board_state[x][y] += 1

    def move_and_build(self, move_coords, build_coords, board_object):
        self.move_to(move_coords, board_object)
        self.__build(build_coords, board_object)
