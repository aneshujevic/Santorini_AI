class Builder:
    # affiliation -> 0 should be for human, 1 should be for AI in general
    def __init__(self, affiliation, coordinates, board_state):
        self.affiliation = affiliation
        self.previous_value = 0
        self.coordinates = coordinates
        board_state[coordinates[0]][coordinates[1]] = self

    def __str__(self):
        return f"{self.affiliation}"

    # move to new coordinates and return the value of old cell on board
    def move_to(self, new_coordinates, board_state):
        board_state[self.coordinates[0]][self.coordinates[1]] = self.previous_value
        self.coordinates = new_coordinates
        self.previous_value = board_state[self.coordinates[0]][self.coordinates[1]]
        board_state[self.coordinates[0]][self.coordinates[1]] = self

    def build(self, move, board_state):
        x = move[0]
        y = move[1]
        board_state[x][y] += 1
