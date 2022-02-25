from itertools import repeat


class Ship:
    def __init__(self, x0: int, y0: int, direction: str, ship_size: int):
        self.x0 = x0
        self.y0 = y0
        self.direction = direction
        self.ship_size = ship_size
        self.num_shots = 0

    def get_coordinates(self):
        if self.direction == "horizontal":
            return zip(
                range(self.x0, self.x0 + self.ship_size),
                repeat(self.y0, self.ship_size),
            )
        else:
            return zip(
                repeat(self.x0, self.ship_size),
                range(self.y0, self.y0 + self.ship_size),
            )

    def set_shot(self):
        self.num_shots += 1

    @property
    def is_dead(self):
        return self.num_shots == self.ship_size
