"""Main game logic for Tetris."""

import pygame
import time
from typing import Dict, Any
from tetris.board import Board
from tetris.pieces import Tetromino, get_random_tetromino
from tetris.renderer import Renderer
from tetris.constants import (
    FPS, INITIAL_FALL_FREQUENCY, LEVEL_SPEEDUP_FACTOR,
    LINES_PER_LEVEL, SCORING, KEY_REPEAT_DELAY, KEY_REPEAT_INTERVAL
)


class TetrisGame:
    """Main Tetris game class."""

    def __init__(self):
        """Initialize a new Tetris game."""
        self.board = Board()
        self.renderer = Renderer()
        self.clock = pygame.time.Clock()
        self.reset_game()
        
        # Set up key repeat for smoother controls
        pygame.key.set_repeat(KEY_REPEAT_DELAY, KEY_REPEAT_INTERVAL)

    def reset_game(self) -> None:
        """Reset the game to its initial state."""
        self.board.reset()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_frequency = INITIAL_FALL_FREQUENCY
        self.last_fall_time = time.time()
        self.game_over = False
        self.paused = False
        
        # Create initial pieces
        self.board.next_piece = get_random_tetromino()
        self._spawn_new_piece()

    def _spawn_new_piece(self) -> None:
        """Spawn a new piece and check for game over."""
        self.board.current_piece = self.board.next_piece
        self.board.next_piece = get_random_tetromino()
        
        # Check if the new piece can be placed
        if not self.board.is_valid_position(self.board.current_piece):
            self.game_over = True

    def _update_score(self, lines_cleared: int) -> None:
        """Update the score based on lines cleared.

        Args:
            lines_cleared: Number of lines cleared.
        """
        if lines_cleared > 0:
            # Update lines count
            self.lines_cleared += lines_cleared
            
            # Update score
            self.score += SCORING.get(lines_cleared, 0) * self.level
            
            # Update level
            new_level = (self.lines_cleared // LINES_PER_LEVEL) + 1
            if new_level > self.level:
                self.level = new_level
                # Increase falling speed
                self.fall_frequency *= LEVEL_SPEEDUP_FACTOR

    def _handle_events(self) -> bool:
        """Handle pygame events.

        Returns:
            False if the game should quit, True otherwise.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.reset_game()
                    continue
                
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                    continue
                
                if self.paused:
                    continue
                
                if event.key == pygame.K_LEFT:
                    self.board.move_piece(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.board.move_piece(1, 0)
                elif event.key == pygame.K_DOWN:
                    self.board.move_piece(0, 1)
                    self.last_fall_time = time.time()  # Reset fall timer
                elif event.key == pygame.K_UP:
                    self.board.rotate_piece()
                elif event.key == pygame.K_SPACE:
                    self.board.drop_piece()
                    lines_cleared = self.board.clear_lines()
                    self._update_score(lines_cleared)
                    self._spawn_new_piece()
        
        return True

    def _update_game(self) -> None:
        """Update the game state."""
        if self.game_over or self.paused:
            return
        
        # Check if it's time for the piece to fall
        current_time = time.time()
        if current_time - self.last_fall_time > self.fall_frequency:
            # Try to move the piece down
            if not self.board.move_piece(0, 1):
                # If the piece can't move down, place it
                self.board.add_piece_to_grid(self.board.current_piece)
                
                # Clear completed lines
                lines_cleared = self.board.clear_lines()
                self._update_score(lines_cleared)
                
                # Spawn a new piece
                self._spawn_new_piece()
            
            self.last_fall_time = current_time

    def _render(self) -> None:
        """Render the game."""
        self.renderer.clear_screen()
        self.renderer.draw_board(self.board)
        self.renderer.draw_next_piece(self.board.next_piece)
        self.renderer.draw_score(self.score, self.level, self.lines_cleared)
        self.renderer.draw_controls()
        
        if self.game_over:
            self.renderer.draw_game_over()
        elif self.paused:
            self.renderer.draw_pause()
        
        self.renderer.update_display()

    def run(self) -> None:
        """Run the game loop."""
        running = True
        while running:
            running = self._handle_events()
            self._update_game()
            self._render()
            self.clock.tick(FPS)
        
        pygame.quit()

    def get_state(self) -> Dict[str, Any]:
        """Get the current game state.

        Returns:
            A dictionary containing the current game state.
        """
        return {
            "score": self.score,
            "level": self.level,
            "lines_cleared": self.lines_cleared,
            "game_over": self.game_over,
            "paused": self.paused
        }
