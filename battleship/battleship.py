from fleetmap import FleetMap
from fleet import Fleet
from player import Player


class BattleShip:
    def __init__(self, map_width=10, map_height=10):
        self.map_width = map_width
        self.map_height = map_height
        self.player = Player(
            name="You", fleet_map=FleetMap(map_width, map_height, Fleet())
        )
        self.computer = Player(
            name="Computer",
            fleet_map=FleetMap(map_width, map_height, Fleet(), hidden=True),
        )
        self.player.set_opponent(self.computer)
        self.computer.set_opponent(self.player)
        self.current_player = self.player

    def fleet_map_str(self, screen_width: int):
        """
        Returns a string for 2 maps
        """
        fleet_map_str = ""
        fleet_map_1 = self.player.fleet_map.draw_map().split("\n")
        fleet_map_2 = self.computer.fleet_map.draw_map().split("\n")
        padding = screen_width - (len(fleet_map_1[0]) + len(fleet_map_2[0])) - 10

        for i in range(len(fleet_map_1)):
            fleet_map_str += fleet_map_1[i] + (" " * padding) + fleet_map_2[i] + "\n"

        name_padding = len(fleet_map_1[0]) - len(self.player.name) - 3
        player_name_str = "\n   " + self.player.name + " " * name_padding
        computer_name_str = "   " + self.computer.name

        fleet_map_str += player_name_str + (" " * padding) + computer_name_str + "\n"
        return fleet_map_str

    @property
    def winner(self):
        """
        Returns the winning player.
        """
        if all(
            ship.is_dead for ship in set(self.player.fleet_map.fleet.ships.values())
        ):
            return self.computer
        elif all(
            ship.is_dead for ship in set(self.computer.fleet_map.fleet.ships.values())
        ):
            return self.player

    def change_next_player(self):
        """
        Turn the current player.
        """
        if self.current_player is self.player:
            self.current_player = self.computer
        else:
            self.current_player = self.player
