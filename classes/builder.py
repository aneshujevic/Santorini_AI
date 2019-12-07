class Builder:
    # 0 should be for human, 1 should be for AI in general
    def __init__(self, affiliation):
        self.affiliation = affiliation
        self.previous_value = 0
        self.coordinates = [0, 0]

    # move to new coordinates and return the value of old cell on board
    def move_to(self, coordinates, value):
        old_value = self.previous_value
        self.previous_value = value
        self.coordinates = coordinates
        return old_value

    def build(self, board_state, move):
        x = move[0]
        y = move[1]
        board_state[x][y] += 1
