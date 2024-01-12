# Fisiks

## Introduction
**"Fisiks"** is an engaging physics-based puzzle game where players use their creativity to draw lines, guiding a ball into a jar. This game elegantly combines realistic physics involving collisions and gravity across three levels of increasing difficulty, providing a blend of fun and intellectual challenge.

## Development
This project features a robust and comprehensive development setup, including:
- **Total Lines of Code:** 1707
- **Modules:** 4
- **Functions:** 26 (including those within classes)
- **Classes:** 4
- **Data Files:** 3 (excluding .png or .wav files)
- **Libraries:** Pygame, Pymunk, random, json

## Front-End Features
Players start by selecting their desired screen resolution from options suitable for a range of monitors and laptops. The main game window presents two interactive options: **Play** and **Exit**, with animated button hover effects for an enhanced user experience. A side panel displays random tips and jokes from .json files for added entertainment. The background music is set to a lower volume by default but can be toggled off as needed.

### Play Menu
Choosing the **Play** option leads to a level selection menu where top scores for each level are displayed. The gameplay core involves strategically drawing lines that transform into physical barriers or paths for the ball. Each line drawn is counted, adding to the challenge. Successfully guiding the ball into the jar opens a menu with options to restart, return to the main menu, or proceed to the next level.

## Back-End Mechanics
At startup, the game checks the `high_scores.json` file for initial game settings. The back-end manages resolution selection, volume control, and seamless transitions between the various menus and levels.

### Game Loop
The game loop includes handling event checks, volume control logic, button enlargement on hover, and level selection processes. Each level is uniquely designed, featuring static lines, triangles, jar boundaries, and the ball. A final menu is presented upon completing a level, offering choices for the next action.

## Key Classes
- **Button:** Manages the visual and interactive aspects of the game's buttons.
- **FreehandDrawing:** Enables players to draw lines that interact with the game's physics.
- **StaticLine:** Utilized for drawing level boundaries and the jar, with varying properties like elasticity in different levels.
- **Ball:** A central game element with low friction, designed to interact with the player-drawn lines and game's physics.

## Installation
1. Requires Python 3 (tested on Python 3.12, but compatible with any version supporting Pygame and Pymunk).
2. Install necessary libraries: Pygame, Pymunk, random, json.
3. Clone the game repository from GitHub.
4. Run `main.py` to start the game.

## Usage
- Launch the game by executing `main.py`.
- Use the mouse to navigate through menus and to draw lines in the game.
- Press the spacebar to cancel a line while drawing.

## Contributions
Contributions to the Fisiks game are welcome. Please adhere to the standard GitHub procedures for submitting issues or pull requests.
