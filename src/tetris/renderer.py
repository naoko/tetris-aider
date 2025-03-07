"""Renderer for the Tetris game."""

import pygame
from typing import Tuple, Optional
from tetris.board import Board
from tetris.pieces import Tetromino
from tetris.constants import (
    BLOCK_SIZE, GRID_WIDTH, GRID_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT,
    BLACK, WHITE, GRAY, COLORS
)


class Renderer:
    """Handles rendering of the Tetris game."""

    def __init__(self, screen_width: int = SCREEN_WIDTH, screen_height: int = SCREEN_HEIGHT):
        """Initialize the renderer.

        Args:
            screen_width: Width of the screen in pixels.
            screen_height: Height of the screen in pixels.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Tetris")
        
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Calculate board position to center it
        self.board_width = GRID_WIDTH * BLOCK_SIZE
        self.board_height = GRID_HEIGHT * BLOCK_SIZE
        self.board_x = (screen_width - self.board_width) // 2  # Center the board
        self.board_y = (screen_height - self.board_height) // 2
        
        # Next piece preview box
        self.preview_x = self.board_x + self.board_width + 50
        self.preview_y = self.board_y + 100
        self.preview_size = 4 * BLOCK_SIZE

    def draw_block(self, x: int, y: int, color: Tuple[int, int, int]) -> None:
        """Draw a single block.

        Args:
            x: X coordinate in pixels.
            y: Y coordinate in pixels.
            color: RGB color tuple.
        """
        pygame.draw.rect(
            self.screen,
            color,
            (x, y, BLOCK_SIZE, BLOCK_SIZE)
        )
        pygame.draw.rect(
            self.screen,
            WHITE,
            (x, y, BLOCK_SIZE, BLOCK_SIZE),
            1  # Border width
        )

    def draw_board(self, board: Board) -> None:
        """Draw the game board.

        Args:
            board: The game board to draw.
        """
        # Draw board background
        pygame.draw.rect(
            self.screen,
            BLACK,
            (self.board_x, self.board_y, self.board_width, self.board_height)
        )
        
        # Draw grid lines
        for x in range(GRID_WIDTH + 1):
            pygame.draw.line(
                self.screen,
                GRAY,
                (self.board_x + x * BLOCK_SIZE, self.board_y),
                (self.board_x + x * BLOCK_SIZE, self.board_y + self.board_height),
                1
            )
        
        for y in range(GRID_HEIGHT + 1):
            pygame.draw.line(
                self.screen,
                GRAY,
                (self.board_x, self.board_y + y * BLOCK_SIZE),
                (self.board_x + self.board_width, self.board_y + y * BLOCK_SIZE),
                1
            )
        
        # Draw placed blocks
        for y in range(board.height):
            for x in range(board.width):
                block_type = board.get_cell_type(x, y)
                if block_type:
                    self.draw_block(
                        self.board_x + x * BLOCK_SIZE,
                        self.board_y + y * BLOCK_SIZE,
                        COLORS[block_type]
                    )
        
        # Draw current piece
        if board.current_piece:
            for x, y in board.current_piece.get_positions():
                if 0 <= y < board.height and 0 <= x < board.width:
                    self.draw_block(
                        self.board_x + x * BLOCK_SIZE,
                        self.board_y + y * BLOCK_SIZE,
                        COLORS[board.current_piece.shape_type]
                    )

    def draw_next_piece(self, piece: Optional[Tetromino]) -> None:
        """Draw the next piece preview.

        Args:
            piece: The next piece to draw.
        """
        # Draw preview box
        pygame.draw.rect(
            self.screen,
            BLACK,
            (self.preview_x, self.preview_y, self.preview_size, self.preview_size)
        )
        pygame.draw.rect(
            self.screen,
            WHITE,
            (self.preview_x, self.preview_y, self.preview_size, self.preview_size),
            2  # Border width
        )
        
        # Draw "Next" text
        next_text = self.font.render("Next", True, WHITE)
        self.screen.blit(
            next_text,
            (self.preview_x, self.preview_y - 40)
        )
        
        if piece:
            # Center the piece in the preview box
            center_x = self.preview_x + self.preview_size // 2
            center_y = self.preview_y + self.preview_size // 2
            
            # Draw the piece
            for dx, dy in piece.shape:
                self.draw_block(
                    center_x + dx * BLOCK_SIZE,
                    center_y + dy * BLOCK_SIZE,
                    COLORS[piece.shape_type]
                )

    def draw_score(self, score: int, level: int, lines: int) -> None:
        """Draw the score, level, and lines information.

        Args:
            score: Current score.
            level: Current level.
            lines: Number of lines cleared.
        """
        # Draw score
        score_text = self.font.render(f"Score: {score}", True, WHITE)
        self.screen.blit(
            score_text,
            (self.preview_x, self.preview_y + self.preview_size + 50)
        )
        
        # Draw level
        level_text = self.font.render(f"Level: {level}", True, WHITE)
        self.screen.blit(
            level_text,
            (self.preview_x, self.preview_y + self.preview_size + 100)
        )
        
        # Draw lines
        lines_text = self.font.render(f"Lines: {lines}", True, WHITE)
        self.screen.blit(
            lines_text,
            (self.preview_x, self.preview_y + self.preview_size + 150)
        )

    def draw_game_over(self) -> None:
        """Draw the game over screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with alpha
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = self.font.render("GAME OVER", True, WHITE)
        restart_text = self.small_font.render("Press R to restart or ESC to quit", True, WHITE)
        
        self.screen.blit(
            game_over_text,
            (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50)
        )
        self.screen.blit(
            restart_text,
            (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10)
        )

    def draw_pause(self) -> None:
        """Draw the pause screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with alpha
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.font.render("PAUSED", True, WHITE)
        continue_text = self.small_font.render("Press P to continue", True, WHITE)
        
        self.screen.blit(
            pause_text,
            (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50)
        )
        self.screen.blit(
            continue_text,
            (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10)
        )

    def draw_controls(self) -> None:
        """Draw the controls information."""
        controls = [
            "Controls:",
            "← → : Move",
            "↑ : Rotate",
            "↓ : Soft Drop",
            "Space : Hard Drop",
            "P : Pause",
            "R : Restart",
            "Esc : Quit"
        ]
        
        # Position controls on the left with proper margin
        x_pos = 20  # Fixed margin from left edge
        y_pos = self.board_y
        
        for text in controls:
            control_text = self.small_font.render(text, True, WHITE)
            self.screen.blit(
                control_text,
                (x_pos, y_pos)
            )
            y_pos += 30

    def clear_screen(self) -> None:
        """Clear the screen."""
        self.screen.fill(BLACK)

    def update_display(self) -> None:
        """Update the display."""
        pygame.display.flip()
