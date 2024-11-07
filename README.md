# Pac-Man Motion Graphics Game

It is a simple Pac-Man-inspired game built using Python and Pygame. The game includes Pac-Man, moving ghosts, walls with openings, and collectible dots. Pac-Man can navigate through the maze, bounce off walls, collect dots for points, and avoid collisions with ghosts.

## Features

- **Pac-Man Movement**: Control Pac-Man with arrow keys to navigate around the screen.
- **Ghost Movement**: Ghosts move autonomously and bounce off walls.
- **Collision Detection**:
  - Pac-Man bounces off walls and collects dots.
  - The game ends if Pac-Man collides with a ghost.
- **Score Tracking**: Earn points by collecting dots.

## Setup

### Prerequisites

- Python 3.x
- Pygame library

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/victorrndungu/Pacman1.1
    ```

2. Install dependencies:

    ```bash
    pip install pygame sys math random
    ```

## Usage

1. Run the game:

    ```bash
    python Pac-Man.py
    ```

2. Use arrow keys to move Pac-Man.
3. Avoid ghosts and collect all dots to maximize your score!

## Game Over Conditions

- Colliding with a ghost will end the game.
- Collect all score-multiplying dots to win the game.
