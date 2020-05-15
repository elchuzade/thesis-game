# Dashboard / Scoreboard configurations
FONT_NAME = 'freesansbold.ttf'
FONT_SIZE = 20
TEXT_COLOR = (240, 200, 250)
TEXT_WIDTH = 100
SCOREBOARD_HEIGHT = 100
SCOREBOARD_BACKGROUND = (50, 50, 50)
SCOREBOARD_SEPARATOR_WIDTH = 2
SCOREBOARD_SEPARATOR_COLOR = (150, 150, 150)

# Game configurations
# - Tunable
GOLD_AMOUNT = 10
# CELL_AMOUNT_Y = 9
# CELL_AMOUNT_X = 21
CELLS = {
    "x": 11,
    "y": 5
}
EXIT = {
    "x": CELLS["x"] - 1,
    "y": CELLS["y"] // 2
}
# EXIT_Y = CELL_AMOUNT_Y // 2
# EXIT_X = CELL_AMOUNT_X - 1
GAME_SPEED = 1
GAME_MODE = "player"
GNOME = {
    "x": 0,
    "y": 0,
    "vision_size": 2
}
# - Fixed
FPS = 30
SPEED = [1, 2, 3, 5, 6, 10, 15, 30]
CELL_SIZE = 20
GRID_LINE_COLOR = (50, 50, 50)
GRID_LINE_WIDTH = 2
GOLD_COLOR = (255, 215, 0)
GOLD_RADIUS = 8
EXIT_COLOR = (240, 200, 160)
WALL_COLOR = (100, 150, 50)
GNOME_RADIUS = 10
GNOME_COLOR = (200, 50, 100)
GNOME_VISION_COLOR = (50, 200, 50)
MARGIN = GNOME["vision_size"] * CELL_SIZE
MODE = ["player", "ai"]
GAME_BACKGROUND = (0, 0, 0)
MARGIN_BACKGROUND = (150, 0, 0)
POSSIBLE_ACTIONS = {
    "gnome": [0, 1, 2, 3]
}

# Player / Gnome
# GNOME_Y = 0
# GNOME_X = 0
# GNOME_VISION_SIZE = 2

# Calculated values
# SCREEN_WIDTH = CELL_SIZE * CELL_AMOUNT_X + MARGIN * 2
# SCREEN_HEIGHT = CELL_SIZE * CELL_AMOUNT_Y + MARGIN * 2 + SCOREBOARD_HEIGHT
# GAME_PLAY_HEIGHT = CELL_SIZE * CELL_AMOUNT_Y
# GAME_PLAY_WIDTH = CELL_SIZE * CELL_AMOUNT_X
# old - new
SCREEN_WIDTH = CELL_SIZE * CELLS["x"] + MARGIN * 2
SCREEN_HEIGHT = CELL_SIZE * CELLS["y"] + MARGIN * 2 + SCOREBOARD_HEIGHT
GAME_PLAY_HEIGHT = CELL_SIZE * CELLS["y"]
GAME_PLAY_WIDTH = CELL_SIZE * CELLS["x"]

# Walls map(11 x 5)
WALL_1 = [{"x": 4, "y": 0}, {"x": 4, "y": 1}, {"x": 4, "y": 2}, {"x": 3, "y": 2}, {"x": 2, "y": 2}]

WALL_2 = [{"x": 6, "y": 2}, {"x": 7, "y": 2}, {"x": 8, "y": 2}, {"x": 8, "y": 3}, {"x": 8, "y": 4}]


# Walls
# WALL_1 = [{"x": 4, "y": 4}, {"x": 5, "y": 4}, {"x": 6, "y": 4}, {"x": 6, "y": 5}, {"x": 6, "y": 6},
#           {"x": 6, "y": 7}, {"x": 6, "y": 8}, {"x": 5, "y": 8}, {"x": 4, "y": 8}]
#
# WALL_2 = [{"x": 20, "y": 4}, {"x": 21, "y": 4}, {"x": 22, "y": 4}, {"x": 22, "y": 5}, {"x": 22, "y": 6},
#           {"x": 22, "y": 7}, {"x": 22, "y": 8}, {"x": 21, "y": 8}, {"x": 20, "y": 8}]
