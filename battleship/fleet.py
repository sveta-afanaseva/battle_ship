from ship import Ship


class Fleet:
    """
    A fleet in the game of BattleShip.
    """

    def __init__(self):
        self.ships = {}

    def create_ship(self, x: int, y: int, direction: str, ship_size: int):
        """
        Add new ship in the fleet.
        """
        ship = Ship(x, y, direction, ship_size)
        for (x, y) in ship.get_coordinates():
            self.ships[(x, y)] = ship

    def get_ship_by_coordinates(self, x: int, y: int):
        """
        Return the ship from the fleet that replace on coordinates x, y.
        """
        return self.ships.get((x, y))
