"""Main entry point for the Tetris game."""

import sys
from tetris.game import TetrisGame


def main():
    """Run the Tetris game."""
    # Check if we should record a demo
    if "--record-demo" in sys.argv:
        print("Recording a demo of the Tetris game...")
        from tetris.recorder import create_demo_recording
        game = TetrisGame()
        create_demo_recording(game)
        return 0
    else:
        game = TetrisGame()
        game.run()
        return 0


if __name__ == "__main__":
    sys.exit(main())
