import random

NUM_FOUR_DECK = 1  # Количество четырехпалубников
NUM_THREE_DECK = 2  # Количество трехпалубных
NUM_TWO_DECK = 3  # Количество двухпалубных
NUM_ONE_DECK = 4  # Количество однопалубных


class FleetMap:
    """
    Player's map with player's ships on it.
    """

    def __init__(self, map_width: int, map_height: int, fleet, hidden=False):
        self.width = map_width
        self.height = map_height
        self.fleet_map = [[" "] * self.width for i in range(self.height)]
        self.fleet = fleet
        self.hidden = hidden  # hidden map for the opponent
        self.ship_sizes = self.get_ship_sizes()
        self.fill_map()

    def get_ship_sizes(self):
        ship_sizes = []
        proportion = (self.width * self.height) / 100
        ship_sizes = (
            [4] * int(proportion * NUM_FOUR_DECK)
            + [3] * int(proportion * NUM_THREE_DECK)
            + [2] * int(proportion * NUM_TWO_DECK)
            + [1] * int(proportion * NUM_ONE_DECK)
        )
        return ship_sizes

    def fill_map(self):
        """
        Fill the map by ships randomly. And create these ships in player's fleet.
        """
        for ship_size in self.ship_sizes:
            while True:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                direction = random.choice(["vertical", "horizontal"])
                if not self.is_cross_border(
                    x, y, direction, ship_size
                ) and not self.is_cross_ship(x, y, direction, ship_size):
                    self.create_ship(x, y, direction, ship_size)
                    self.fleet.create_ship(x, y, direction, ship_size)
                    break

    def is_cross_ship(self, x: int, y: int, direction: str, ship_size: int):
        """
        Check if the ship crosses an existing one.
        """
        if direction == "vertical":
            for i in range(max(y - 1, 0), min(y + ship_size + 1, self.height)):
                for j in range(max(x - 1, 0), min(x + 2, self.width)):
                    if self.fleet_map[i][j] == "+":
                        return True
        else:
            for i in range(max(y - 1, 0), min(y + 2, self.height)):
                for j in range(max(x - 1, 0), min(x + ship_size + 1, self.width)):
                    if self.fleet_map[i][j] == "+":
                        return True
        return False

    def create_ship(self, x: int, y: int, direction: str, ship_size: int):
        """
        Create ship on the map.
        """
        if direction == "vertical":
            for y in range(y, y + ship_size):
                self.fleet_map[y][x] = "+"
        else:
            for x in range(x, x + ship_size):
                self.fleet_map[y][x] = "+"

    def is_cross_border(self, x: int, y: int, direction: str, ship_size: int):
        """
        Check if the ship crosses borders of the map.
        """
        border = self.width
        if direction == "vertical":
            x = y
            border = self.height
        if x + ship_size > border:
            return True
        return False

    def draw_map(self):
        """
        Return a string for displaying the map on the screen.
        """
        fleet_map = "   " + "".join(f" {letter} " for letter in range(self.width))
        for number in range(self.height):
            fleet_map += (
                f"\n{number} |"
                + "".join(f" {cell} " for cell in self.fleet_map[number])
                + "|"
            )
        if self.hidden:
            fleet_map = fleet_map.replace("+", " ")
        return fleet_map

    def set_shot(self, x: int, y: int):
        """
        Change the map after shot.
        """
        if x >= self.width or y >= self.height or x < 0 or y < 0:
            raise ValueError

        if self.fleet_map[y][x] == " ":
            self.fleet_map[y][x] = "."
            return "Мимо!"
        elif self.fleet_map[y][x] == "+":
            self.fleet_map[y][x] = "x"
            ship = self.fleet.get_ship_by_coordinates(x, y)
            ship.set_shot()
            if ship.is_dead:
                self.fill_area_around_ship(ship)
            return "Попал!"
        elif self.fleet_map[y][x] == ".":
            raise ValueError
        elif self.fleet_map[y][x] == "x":
            raise ValueError

    def fill_area_around_ship(self, ship):
        min_x, min_y = min(ship.get_coordinates())
        max_x, max_y = max(ship.get_coordinates())
        for x in range(max(0, min_x - 1), min(max_x + 2, self.width)):
            for y in range(max(0, min_y - 1), min(max_y + 2, self.height)):
                if self.fleet_map[y][x] == " ":
                    self.fleet_map[y][x] = "."

    def get_available_coordinates(self):
        """
        Return a list of coordinates to shoot at.
        """
        available_coordinates = []
        for y in range(self.height):
            for x in range(self.width):
                if self.fleet_map[y][x] in (" ", "+"):
                    available_coordinates.append((x, y))
        return available_coordinates
