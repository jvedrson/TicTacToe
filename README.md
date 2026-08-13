# Tic-Tac-Toe Arcade

## Overview

Tic-Tac-Toe Arcade is a local multiplayer game for two players, developed with Python and the Arcade framework. This game is a modern take on the classic game, designed to be played on the same computer by two people sitting side-by-side. It supports mouse and keyboard input, making it accessible and comfortable for different play styles.

The game features a clean visual interface with a 3x3 grid. Player 1 plays with the **X** (blue) and Player 2 with the **O** (red).

#### How to play?
- You can place your piece by clicking on a square with the mouse or using the keyboard.

- Player 1 uses the left-hand keys (`Q W E A S D Z X C`) and Player 2 uses the right-hand keys (`U I O J K L M , .`), so both players can play simultaneously without needing to use the mouse.

#### Levels
What sets this version apart is its timer-based difficulty system. You can choose between Easy (10 seconds per turn), Medium (5 seconds), or Hard (3 seconds). If a player runs out of time, they lose the round. The game records the scores for each round, and the winner of each round always starts the next.

[Software Demo Video](https://youtu.be/hO1sK9sODZA)

## Development Environment

- **Editor:** Visual Studio Code
- **Language:** Python 3.10+
- **Game Framework:** Arcade 3.x

## Useful Websites

These resources were really helpful while building this project:

- [Arcade Academy — Official Documentation](https://api.arcade.academy/en/latest/) — The main reference for everything Arcade, from drawing shapes to handling input and managing views.
- [Arcade Examples on GitHub](https://github.com/pythonarcade/arcade/tree/master/arcade/examples) — Lots of short, working examples that show how to use specific features.
- [Real Python — Object-Oriented Programming in Python 3](https://realpython.com/python3-object-oriented-programming/) — Helped me structure my code with classes and dataclasses.

## Future Work

There are a few things I'd like to improve and add later:

- **Improved menu** — Add a "how to play" panel and display difficulty descriptions when hovering.
- **Single-player mode** — Add a computer opponent with simple AI (random moves, then minimax for harder difficulty).
- **Save scores** — Store high scores between sessions using a local JSON file.
- **Better sound effects** — Replace the bundled coin and game-over sounds with custom audio.
