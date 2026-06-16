# Pac-Man (Python/Pygame) 🕹️

*A 10th-grade school project recreating the classic arcade game, Pac-Man!*

## Overview

This project is a 2D arcade game where the player controls Pac-Man to eat points while avoiding ghosts. It features a customizable map, adjustable difficulty levels, and game settings loaded from external files. It was originally built as a school project during my 10th-grade class.

## Features
- **Classic Gameplay:** Eat points, avoid ghosts, and try to survive!
- **Customizable Maps:** The level layout can be easily modified by editing a simple text file (`data/config/Map.txt`).
- **Adjustable Difficulty:** Tweak speeds, fps, and more in the `data/config/Settings.txt` file.
- **Hunt Mode:** Eat a cherry to turn the tables and hunt the ghosts!

## Tech Stack
- **Language:** Python 3
- **Library:** [Pygame](https://www.pygame.org/) for graphics, sound, and input handling.

## Getting Started

### Prerequisites
- Python 3.x

### Installation
1. Clone the repository or download the source code.
2. Install the required dependencies using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Game
Start the game by running the main Python script from the project root:
```bash
python src/main.py
```

## Project Structure
- `src/`: Contains all the Python source code (`main.py`, `entities.py`, `globals.py`, etc.).
- `data/config/`: Configuration files.
  - `Map.txt`: Defines the game level layout (`0` for walls, `1` for paths).
  - `Settings.txt`: Game parameters like screen dimensions, FPS, entity speeds, etc.
- `data/images/`: Sprite assets for Pac-Man and ghosts.
- `data/audio/`: Background music and sound files.

## Controls
- **Movement:** `Arrow Keys` or `W`, `A`, `S`, `D`
- **Menu Navigation:** Use your `Mouse` to click through the lobby menus (Start, Difficulty, Exit).
