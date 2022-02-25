class Player:
    """
    A player for the game of BattleShip. Keeps track of name and fleet map.
    """

    def __init__(self, name, fleet_map):
        self.name = name
        self.fleet_map = fleet_map

    def set_opponent(self, opponent):
        self.opponent = opponent

    @property
    def num_ships(self):
        return len(self.fleet_map.fleet.ships)

    def __repr__(self):
        return f"Player: {self.name}"

    def take_shot(self, x: int, y: int):
        return self.opponent.update_map_after_shot(x, y)

    def update_map_after_shot(self, x: int, y: int):
        return self.fleet_map.set_shot(x, y)

    def get_available_coordinates(self):
        return self.opponent.fleet_map.get_available_coordinates()
