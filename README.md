# Tetris Game

A classic Tetris game implemented in Python using Pygame.

## Features

- Classic Tetris gameplay
- Score tracking
- Level progression
- Next piece preview
- Game over detection

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/tetris.git
   cd tetris
   ```

2. Set up the environment and install dependencies:
   ```bash
   make setup
   ```

## Running the Game

To start the game, run:

```bash
make run
```

Or manually:

```bash
python -m tetris
```

## Controls

- Left Arrow: Move piece left
- Right Arrow: Move piece right
- Down Arrow: Move piece down (soft drop)
- Up Arrow: Rotate piece clockwise
- Space: Hard drop
- P: Pause/Resume game
- Esc: Quit game

## Development

### Install Development Dependencies

```bash
make dev
```

### Run Tests

```bash
make test
```

### Lint and Format Code

```bash
make lint
make format
```

## Project Structure

```
tetris/
├── src/
│   └── tetris/
│       ├── __init__.py
│       ├── __main__.py
│       ├── game.py
│       ├── board.py
│       ├── pieces.py
│       ├── renderer.py
│       └── constants.py
├── tests/
│   ├── __init__.py
│   ├── test_board.py
│   ├── test_pieces.py
│   └── test_game.py
├── pyproject.toml
├── Makefile
└── README.md
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
