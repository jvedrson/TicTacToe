import arcade

from constants import SCREEN_HEIGHT, SCREEN_TITLE, SCREEN_WIDTH
from views import MenuView


def main() -> None:
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu = MenuView()
    window.show_view(menu)
    arcade.run()


if __name__ == "__main__":
    main()