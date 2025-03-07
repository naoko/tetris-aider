"""Tests for the Board class."""

import pytest
from tetris.board import Board
from tetris.pieces import Tetromino


def test_board_initialization():
    """Test that the board initializes correctly."""
    board = Board(10, 20)
    assert board.width == 10
    assert board.height == 20
    assert len(board.grid) == 20
    assert len(board.grid[0]) == 10
    assert board.current_piece is None
    assert board.next_piece is None


def test_board_reset():
    """Test that the board resets correctly."""
    board = Board(10, 20)
    
    # Add a piece to the grid
    board.current_piece = Tetromino("I")
    board.add_piece_to_grid(board.current_piece)
    
    # Reset the board
    board.reset()
    
    # Check that the board is empty
    for row in board.grid:
        for cell in row:
            assert cell is None
    
    assert board.current_piece is None
    assert board.next_piece is None


def test_is_valid_position():
    """Test the is_valid_position method."""
    board = Board(10, 20)
    
    # Create a piece
    piece = Tetromino("I")
    piece.x = 5
    piece.y = 5
    
    # The position should be valid
    assert board.is_valid_position(piece)
    
    # Move the piece out of bounds
    piece.x = -1
    assert not board.is_valid_position(piece)
    
    # Move the piece back in bounds
    piece.x = 5
    assert board.is_valid_position(piece)
    
    # Add a block to the grid where the piece would be
    board.grid[5][5] = "I"
    assert not board.is_valid_position(piece)


def test_add_piece_to_grid():
    """Test the add_piece_to_grid method."""
    board = Board(10, 20)
    
    # Create a piece
    piece = Tetromino("I")
    piece.x = 5
    piece.y = 5
    
    # Add the piece to the grid
    board.add_piece_to_grid(piece)
    
    # Check that the piece is in the grid
    for x, y in piece.get_positions():
        assert board.grid[y][x] == "I"


def test_move_piece():
    """Test the move_piece method."""
    board = Board(10, 20)
    
    # Create a piece
    board.current_piece = Tetromino("I")
    board.current_piece.x = 5
    board.current_piece.y = 5
    
    # Move the piece right
    assert board.move_piece(1, 0)
    assert board.current_piece.x == 6
    assert board.current_piece.y == 5
    
    # Move the piece down
    assert board.move_piece(0, 1)
    assert board.current_piece.x == 6
    assert board.current_piece.y == 6
    
    # Move the piece left
    assert board.move_piece(-1, 0)
    assert board.current_piece.x == 5
    assert board.current_piece.y == 6
    
    # Try to move the piece out of bounds
    board.current_piece.x = 0
    assert not board.move_piece(-1, 0)
    assert board.current_piece.x == 0  # Position should not change


def test_rotate_piece():
    """Test the rotate_piece method."""
    board = Board(10, 20)
    
    # Create a piece
    board.current_piece = Tetromino("I")
    board.current_piece.x = 5
    board.current_piece.y = 5
    original_rotation = board.current_piece.rotation
    
    # Rotate the piece
    assert board.rotate_piece()
    assert board.current_piece.rotation == (original_rotation + 1) % 4
    
    # Rotate the piece again
    assert board.rotate_piece()
    assert board.current_piece.rotation == (original_rotation + 2) % 4


def test_clear_lines():
    """Test the clear_lines method."""
    board = Board(10, 20)
    
    # Fill a row
    for x in range(10):
        board.grid[19][x] = "I"
    
    # Clear lines
    lines_cleared = board.clear_lines()
    assert lines_cleared == 1
    
    # Check that the row is cleared
    for x in range(10):
        assert board.grid[19][x] is None
    
    # Fill multiple rows
    for y in range(18, 20):
        for x in range(10):
            board.grid[y][x] = "I"
    
    # Clear lines
    lines_cleared = board.clear_lines()
    assert lines_cleared == 2


def test_is_game_over():
    """Test the is_game_over method."""
    board = Board(10, 20)
    
    # The game should not be over initially
    assert not board.is_game_over()
    
    # Add a block to the top row
    board.grid[0][5] = "I"
    
    # The game should be over
    assert board.is_game_over()


def test_drop_piece():
    """Test the drop_piece method."""
    board = Board(10, 20)
    
    # Create a piece
    board.current_piece = Tetromino("I")
    board.current_piece.x = 5
    board.current_piece.y = 0
    
    # Drop the piece
    assert board.drop_piece()
    
    # The piece should be at the bottom of the board
    assert board.current_piece is None
    assert board.grid[19][5] == "I"
