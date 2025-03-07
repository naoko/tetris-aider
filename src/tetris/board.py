"""Game board for Tetris."""

from typing import List, Optional, Tuple, Set
from tetris.pieces import Tetromino
from tetris.constants import GRID_WIDTH, GRID_HEIGHT


class Board:
    """Represents the Tetris game board."""

    def __init__(self, width: int = GRID_WIDTH, height: int = GRID_HEIGHT):
        """Initialize a new game board.

        Args:
            width: Width of the board in blocks.
            height: Height of the board in blocks.
        """
        self.width = width
        self.height = height
        self.grid: List[List[Optional[str]]] = [[None for _ in range(width)] for _ in range(height)]
        self.current_piece: Optional[Tetromino] = None
        self.next_piece: Optional[Tetromino] = None

    def reset(self) -> None:
        """Reset the board to its initial state."""
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.current_piece = None
        self.next_piece = None

    def is_valid_position(self, piece: Tetromino) -> bool:
        """Check if the piece is in a valid position.

        Args:
            piece: The tetromino to check.

        Returns:
            True if the position is valid, False otherwise.
        """
        for x, y in piece.get_positions():
            # Check if the piece is within the board boundaries
            if x < 0 or x >= self.width or y >= self.height:
                return False
            
            # Check if the piece overlaps with existing blocks
            if y >= 0 and self.grid[y][x] is not None:
                return False
        
        return True

    def add_piece_to_grid(self, piece: Tetromino) -> None:
        """Add the piece to the grid.

        Args:
            piece: The tetromino to add to the grid.
        """
        for x, y in piece.get_positions():
            if 0 <= y < self.height and 0 <= x < self.width:
                self.grid[y][x] = piece.shape_type

    def move_piece(self, dx: int, dy: int) -> bool:
        """Move the current piece.

        Args:
            dx: Horizontal movement (-1 for left, 1 for right).
            dy: Vertical movement (1 for down).

        Returns:
            True if the move was successful, False otherwise.
        """
        if not self.current_piece:
            return False

        # Save original position
        original_x = self.current_piece.x
        original_y = self.current_piece.y

        # Try to move
        self.current_piece.x += dx
        self.current_piece.y += dy

        # Check if the new position is valid
        if not self.is_valid_position(self.current_piece):
            # Restore original position
            self.current_piece.x = original_x
            self.current_piece.y = original_y
            return False

        return True

    def rotate_piece(self) -> bool:
        """Rotate the current piece clockwise.

        Returns:
            True if the rotation was successful, False otherwise.
        """
        if not self.current_piece:
            return False

        # Save original rotation
        original_rotation = self.current_piece.rotation

        # Try to rotate
        self.current_piece.rotate()

        # Check if the new rotation is valid
        if not self.is_valid_position(self.current_piece):
            # Restore original rotation
            self.current_piece.rotation = original_rotation
            return False

        return True

    def drop_piece(self) -> bool:
        """Drop the current piece as far as it can go.

        Returns:
            True if the piece was placed, False otherwise.
        """
        if not self.current_piece:
            return False

        # Move the piece down until it can't move anymore
        while self.move_piece(0, 1):
            pass

        # Add the piece to the grid
        self.add_piece_to_grid(self.current_piece)
        self.current_piece = None
        return True

    def clear_lines(self) -> int:
        """Clear completed lines and return the number of lines cleared.

        Returns:
            The number of lines cleared.
        """
        lines_cleared = 0
        y = self.height - 1
        while y >= 0:
            # Check if the line is complete
            if all(cell is not None for cell in self.grid[y]):
                # Remove the line
                self.grid.pop(y)
                # Add a new empty line at the top
                self.grid.insert(0, [None for _ in range(self.width)])
                lines_cleared += 1
            else:
                y -= 1
        
        return lines_cleared

    def is_game_over(self) -> bool:
        """Check if the game is over.

        Returns:
            True if the game is over, False otherwise.
        """
        # Game is over if there are blocks in the top row
        return any(cell is not None for cell in self.grid[0])

    def get_occupied_cells(self) -> Set[Tuple[int, int]]:
        """Get the positions of all occupied cells on the board.

        Returns:
            A set of (x, y) coordinates of occupied cells.
        """
        occupied = set()
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] is not None:
                    occupied.add((x, y))
        return occupied

    def get_cell_type(self, x: int, y: int) -> Optional[str]:
        """Get the type of block at the given position.

        Args:
            x: X coordinate.
            y: Y coordinate.

        Returns:
            The type of block at the position, or None if empty.
        """
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.grid[y][x]
        return None
