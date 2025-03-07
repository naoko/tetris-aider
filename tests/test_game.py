"""Tests for the TetrisGame class."""

import pytest
import pygame
from unittest.mock import patch, MagicMock
from tetris.game import TetrisGame


@pytest.fixture
def game():
    """Create a TetrisGame instance for testing."""
    # Initialize pygame for testing
    pygame.init()
    
    # Create a game instance
    game = TetrisGame()
    
    # Return the game instance
    yield game
    
    # Clean up
    pygame.quit()


def test_game_initialization(game):
    """Test that the game initializes correctly."""
    assert game.board is not None
    assert game.renderer is not None
    assert game.clock is not None
    assert game.score == 0
    assert game.level == 1
    assert game.lines_cleared == 0
    assert not game.game_over
    assert not game.paused
    assert game.board.current_piece is not None
    assert game.board.next_piece is not None


def test_reset_game(game):
    """Test that the game resets correctly."""
    # Change some game state
    game.score = 1000
    game.level = 5
    game.lines_cleared = 50
    game.game_over = True
    game.paused = True
    
    # Reset the game
    game.reset_game()
    
    # Check that the game state is reset
    assert game.score == 0
    assert game.level == 1
    assert game.lines_cleared == 0
    assert not game.game_over
    assert not game.paused
    assert game.board.current_piece is not None
    assert game.board.next_piece is not None


def test_update_score(game):
    """Test that the score updates correctly."""
    # Initial state
    assert game.score == 0
    assert game.level == 1
    assert game.lines_cleared == 0
    
    # Clear 1 line
    game._update_score(1)
    assert game.score == 100  # 100 points for 1 line at level 1
    assert game.lines_cleared == 1
    assert game.level == 1  # Level shouldn't change yet
    
    # Clear 2 lines
    game._update_score(2)
    assert game.score == 100 + 300  # 300 points for 2 lines at level 1
    assert game.lines_cleared == 3
    assert game.level == 1  # Level shouldn't change yet
    
    # Clear enough lines to level up
    game._update_score(7)  # Total lines: 10
    assert game.lines_cleared == 10
    assert game.level == 2  # Level should increase


def test_get_state(game):
    """Test that get_state returns the correct state."""
    # Set some game state
    game.score = 1000
    game.level = 5
    game.lines_cleared = 50
    game.game_over = True
    game.paused = True
    
    # Get the state
    state = game.get_state()
    
    # Check that the state is correct
    assert state["score"] == 1000
    assert state["level"] == 5
    assert state["lines_cleared"] == 50
    assert state["game_over"] is True
    assert state["paused"] is True


@patch('pygame.event.get')
def test_handle_events_quit(mock_event_get, game):
    """Test that the game quits when the quit event is received."""
    # Mock the event
    mock_event = MagicMock()
    mock_event.type = pygame.QUIT
    mock_event_get.return_value = [mock_event]
    
    # Handle events
    result = game._handle_events()
    
    # Check that the game should quit
    assert not result


@patch('pygame.event.get')
def test_handle_events_escape(mock_event_get, game):
    """Test that the game quits when escape is pressed."""
    # Mock the event
    mock_event = MagicMock()
    mock_event.type = pygame.KEYDOWN
    mock_event.key = pygame.K_ESCAPE
    mock_event_get.return_value = [mock_event]
    
    # Handle events
    result = game._handle_events()
    
    # Check that the game should quit
    assert not result


@patch('pygame.event.get')
def test_handle_events_pause(mock_event_get, game):
    """Test that the game pauses when P is pressed."""
    # Mock the event
    mock_event = MagicMock()
    mock_event.type = pygame.KEYDOWN
    mock_event.key = pygame.K_p
    mock_event_get.return_value = [mock_event]
    
    # Initial state
    assert not game.paused
    
    # Handle events
    result = game._handle_events()
    
    # Check that the game is paused
    assert result  # Game should continue
    assert game.paused
    
    # Handle events again
    result = game._handle_events()
    
    # Check that the game is unpaused
    assert result  # Game should continue
    assert not game.paused
