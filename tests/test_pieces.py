"""Tests for the Tetromino class."""

import pytest
from tetris.pieces import Tetromino, get_random_tetromino


def test_tetromino_initialization():
    """Test that a tetromino initializes correctly."""
    # Test with a specific shape
    piece = Tetromino("I")
    assert piece.shape_type == "I"
    assert piece.rotation == 0
    assert piece.x == 5
    assert piece.y == 0
    
    # Test with a random shape
    piece = get_random_tetromino()
    assert piece.shape_type in Tetromino.SHAPES.keys()
    assert piece.rotation == 0
    assert piece.x == 5
    assert piece.y == 0


def test_tetromino_rotation():
    """Test that a tetromino rotates correctly."""
    piece = Tetromino("I")
    
    # Initial rotation
    assert piece.rotation == 0
    
    # Rotate clockwise
    piece.rotate()
    assert piece.rotation == 1
    
    # Rotate clockwise again
    piece.rotate()
    assert piece.rotation == 2
    
    # Rotate counterclockwise
    piece.rotate(clockwise=False)
    assert piece.rotation == 1
    
    # Rotate through all positions and back to the start
    piece.rotate()
    piece.rotate()
    piece.rotate()
    assert piece.rotation == 0


def test_get_positions():
    """Test that get_positions returns the correct positions."""
    piece = Tetromino("I")
    piece.x = 5
    piece.y = 5
    
    # Get the positions
    positions = piece.get_positions()
    
    # Check that there are 4 positions
    assert len(positions) == 4
    
    # Check that the positions are correct for an I piece
    expected_positions = [(5, 4), (5, 5), (5, 6), (5, 7)]
    assert set(positions) == set(expected_positions)
    
    # Rotate the piece and check again
    piece.rotate()
    positions = piece.get_positions()
    expected_positions = [(4, 5), (5, 5), (6, 5), (7, 5)]
    assert set(positions) == set(expected_positions)


def test_all_tetromino_shapes():
    """Test that all tetromino shapes are defined correctly."""
    for shape_type in Tetromino.SHAPES.keys():
        piece = Tetromino(shape_type)
        
        # Check that the piece has 4 blocks
        assert len(piece.shape) == 4
        
        # Check that the piece has 4 rotations
        assert len(Tetromino.SHAPES[shape_type]) == 4


def test_random_tetromino():
    """Test that get_random_tetromino returns a valid tetromino."""
    # Get multiple random pieces to ensure randomness
    pieces = [get_random_tetromino() for _ in range(10)]
    
    # Check that all pieces are valid
    for piece in pieces:
        assert piece.shape_type in Tetromino.SHAPES.keys()
        assert piece.rotation == 0
        assert piece.x == 5
        assert piece.y == 0
    
    # Check that we got at least 2 different shapes
    # (This could theoretically fail, but it's very unlikely)
    assert len(set(piece.shape_type for piece in pieces)) > 1
