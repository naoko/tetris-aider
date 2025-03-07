"""Tetromino pieces for the Tetris game."""

from typing import Dict, List, Tuple
import random


class Tetromino:
    """A Tetris piece (tetromino)."""

    # Tetromino shapes defined as relative coordinates from a center point
    SHAPES: Dict[str, List[List[Tuple[int, int]]]] = {
        "I": [
            [(0, -1), (0, 0), (0, 1), (0, 2)],
            [(-1, 0), (0, 0), (1, 0), (2, 0)],
            [(0, -1), (0, 0), (0, 1), (0, 2)],
            [(-1, 0), (0, 0), (1, 0), (2, 0)],
        ],
        "J": [
            [(-1, -1), (0, -1), (0, 0), (0, 1)],
            [(-1, 0), (0, 0), (1, 0), (1, -1)],
            [(0, -1), (0, 0), (0, 1), (1, 1)],
            [(-1, 1), (-1, 0), (0, 0), (1, 0)],
        ],
        "L": [
            [(0, -1), (0, 0), (0, 1), (-1, 1)],
            [(-1, 0), (0, 0), (1, 0), (-1, -1)],
            [(0, -1), (0, 0), (0, 1), (1, -1)],
            [(-1, 0), (0, 0), (1, 0), (1, 1)],
        ],
        "O": [
            [(-1, 0), (0, 0), (-1, 1), (0, 1)],
            [(-1, 0), (0, 0), (-1, 1), (0, 1)],
            [(-1, 0), (0, 0), (-1, 1), (0, 1)],
            [(-1, 0), (0, 0), (-1, 1), (0, 1)],
        ],
        "S": [
            [(0, -1), (0, 0), (1, 0), (1, 1)],
            [(1, 0), (0, 0), (0, 1), (-1, 1)],
            [(0, -1), (0, 0), (1, 0), (1, 1)],
            [(1, 0), (0, 0), (0, 1), (-1, 1)],
        ],
        "T": [
            [(0, -1), (0, 0), (0, 1), (1, 0)],
            [(-1, 0), (0, 0), (1, 0), (0, 1)],
            [(0, -1), (0, 0), (0, 1), (-1, 0)],
            [(-1, 0), (0, 0), (1, 0), (0, -1)],
        ],
        "Z": [
            [(0, -1), (0, 0), (-1, 0), (-1, 1)],
            [(-1, 0), (0, 0), (0, -1), (1, -1)],
            [(0, -1), (0, 0), (-1, 0), (-1, 1)],
            [(-1, 0), (0, 0), (0, -1), (1, -1)],
        ],
    }

    def __init__(self, shape_type: str = None):
        """Initialize a new tetromino.

        Args:
            shape_type: The type of tetromino to create. If None, a random one is chosen.
        """
        if shape_type is None:
            shape_type = random.choice(list(self.SHAPES.keys()))
        
        self.shape_type = shape_type
        self.rotation = 0
        self.x = 5  # Start in the middle of the board
        self.y = 0  # Start at the top

    @property
    def shape(self) -> List[Tuple[int, int]]:
        """Get the current shape based on rotation."""
        return self.SHAPES[self.shape_type][self.rotation]

    def rotate(self, clockwise: bool = True) -> None:
        """Rotate the tetromino.

        Args:
            clockwise: Whether to rotate clockwise (True) or counterclockwise (False).
        """
        if clockwise:
            self.rotation = (self.rotation + 1) % 4
        else:
            self.rotation = (self.rotation - 1) % 4

    def get_positions(self) -> List[Tuple[int, int]]:
        """Get the absolute positions of the tetromino blocks on the board."""
        return [(self.x + dx, self.y + dy) for dx, dy in self.shape]


def get_random_tetromino() -> Tetromino:
    """Create a new random tetromino."""
    return Tetromino()
