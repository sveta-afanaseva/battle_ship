import curses
import os
import pickle
import random
import typer

from battleship import BattleShip
import messages


def play(game, screen):
    """
    Simulates a game of BattleShip.
    The game ends with a winner or when "quit" is typed.
    """
    flash_message = messages.EMPTY_MESSAGE
    while True:
        screen.clear()
        curses.resize_term(0, 0)

        # Check if screen is large enough to play game
        screen_height, screen_width = screen.getmaxyx()
        if screen_height < MAP_HEIGHT + 8:
            screen.addstr(0, 0, messages.SHORT_SCREEN_MESSAGE)
            screen.refresh()
            continue

        if game.winner:
            break

        screen.addstr(0, 0, flash_message)
        screen.addstr(1, 0, game.fleet_map_str(screen_width))

        # Get user input
        if game.current_player is game.player:
            curses.echo()
            screen.addstr(14, 0, messages.SHOT_X_MESSAGE)
            x = screen.getstr(15, 4).decode(encoding="utf-8")
            if x == "quit":
                return

            screen.addstr(16, 0, messages.SHOT_Y_MESSAGE)
            y = screen.getstr(16, 4).decode(encoding="utf-8")
            if y == "quit":
                return
        else:
            x, y = random.choice(game.computer.get_available_coordinates())

        try:
            result = game.current_player.take_shot(int(x), int(y))
            flash_message = messages.EMPTY_MESSAGE
            if result == "Мимо!":
                game.change_next_player()
        except (ValueError, TypeError):
            flash_message = messages.INPUT_ERROR_MESSAGE


def main(
    n: int = typer.Argument(..., min=5, max=10, help="map's width"),
    k: int = typer.Argument(..., min=5, max=10, help="map's height"),
):
    global MAP_WIDTH, MAP_HEIGHT
    MAP_WIDTH = n
    MAP_HEIGHT = k

    curses.wrapper(start_game)


def start_game(screen):
    screen.clear()
    game = None
    flash_message = messages.EMPTY_MESSAGE

    while True:
        screen.clear()
        curses.resize_term(0, 0)

        # Check if screen is large enough to play game
        screen_height, screen_width = screen.getmaxyx()
        if screen_height < 10:
            screen.addstr(0, 0, messages.SHORT_SCREEN_MESSAGE)
            screen.refresh()
            continue

        if game and game.winner:
            flash_message = messages.WINNER_MESSAGE.format(winner=game.winner.name)

        # Display instructions and winner message on screen
        screen.clear()
        screen.addstr(
            0,
            0,
            messages.WELCOME_MESSAGE + flash_message + messages.INSTRUCTION_MESSAGE,
        )

        # Get user input
        c = chr(screen.getch())
        if c == "q":
            # Quit the game
            return
        elif c == "p":
            # Play a new game
            game = BattleShip(MAP_WIDTH, MAP_HEIGHT)
            play(game, screen)
            flash_message = messages.EMPTY_MESSAGE
        elif c == "s":
            # Save the game
            with open("save.pkl", "wb") as f:
                pickle.dump(game, f)
            flash_message = messages.SAVE_MESSAGE
            continue
        elif c == "l":
            # Load saved game
            if os.path.exists("save.pkl"):
                with open("save.pkl", "rb") as f:
                    game = pickle.load(f)
                play(game, screen)
                flash_message = messages.EMPTY_MESSAGE
            else:
                flash_message = messages.NO_SAVED_GAMES_MESSAGE


if __name__ == "__main__":
    print(messages.PLAYING_MESSAGE)
    typer.run(main)
