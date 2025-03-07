"""Constants used throughout the Tetris game."""

# Game dimensions
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 720

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Tetromino colors
COLORS = {
    "I": CYAN,
    "J": BLUE,
    "L": ORANGE,
    "O": YELLOW,
    "S": GREEN,
    "T": MAGENTA,
    "Z": RED,
}

# Game settings
FPS = 60
INITIAL_FALL_FREQUENCY = 1.0  # Pieces fall every 1 second initially
LEVEL_SPEEDUP_FACTOR = 0.8  # Each level speeds up by this factor
LINES_PER_LEVEL = 10
SCORING = {
    1: 100,    # 1 line cleared
    2: 300,    # 2 lines cleared
    3: 500,    # 3 lines cleared
    4: 800,    # 4 lines cleared (Tetris)
}

# Key repeat settings
KEY_REPEAT_DELAY = 200  # ms
KEY_REPEAT_INTERVAL = 100  # ms
