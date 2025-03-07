"""Main entry point for the Tetris game."""

import sys
from tetris.game import TetrisGame


def main():
    """Run the Tetris game."""
    game = TetrisGame()
    game.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
