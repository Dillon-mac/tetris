import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Shapes - Each shape is a list of strings representing its rotations
SHAPES = [
    [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']],

    [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']],

    [['.....',
      '..0..',
      '..0..',
      '..0..',
      '..0..'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']],

    [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']],

    [['.....',
      '.....',
      '..0..',
      '.000.',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']],

    [['.....',
      '.....',
      '.0...',
      '.000.',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']],

    [['.....',
      '.....',
      '...0.',
      '.000.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....']]
]

# Shape colors
SHAPE_COLORS = [CYAN, MAGENTA, ORANGE, BLUE, YELLOW, GREEN, RED]

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Clock
clock = pygame.time.Clock()

def create_grid(locked_positions={}):
    """Creates a grid of the game with locked positions filled"""
    grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if (x, y) in locked_positions:
                grid[y][x] = locked_positions[(x, y)]
    return grid

def draw_grid(surface, grid):
    """Draws the grid on the screen"""
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(surface, grid[y][x], (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)
            pygame.draw.rect(surface, WHITE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

class Piece:
    """Class representing a Tetris piece"""
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0

    def rotate(self):
        """Rotate the piece to the next rotation"""
        self.rotation = (self.rotation + 1) % len(self.shape)

    def current_shape(self):
        """Returns the current rotation of the piece"""
        return self.shape[self.rotation]

def get_new_piece():
    """Generates a new random piece"""
    return Piece(GRID_WIDTH // 2 - 2, 0, random.choice(SHAPES))

def draw_piece(surface, piece):
    """Draws the current piece on the screen"""
    shape = piece.current_shape()
    for y, line in enumerate(shape):
        for x, cell in enumerate(line):
            if cell == '0':
                pygame.draw.rect(surface, piece.color, ((piece.x + x) * GRID_SIZE, (piece.y + y) * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)

def valid_space(piece, grid):
    """Checks if the piece can be placed at its current position"""
    accepted_positions = [[(j, i) for j in range(GRID_WIDTH) if grid[i][j] == BLACK] for i in range(GRID_HEIGHT)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(piece)
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] >= 0:
                return False
    return True

def convert_shape_format(piece):
    """Converts the shape format into grid positions"""
    positions = []
    shape = piece.current_shape()
    for y, line in enumerate(shape):
        row = list(line)
        for x, cell in enumerate(row):
            if cell == '0':
                positions.append((piece.x + x, piece.y + y))
    for i, pos in enumerate(positions):
        positions[i] = (pos[0], pos[1])
    return positions

def clear_rows(grid, locked_positions):
    """Clears filled rows and updates the locked positions"""
    increment = 0
    for y in range(GRID_HEIGHT - 1, -1, -1):
        row = grid[y]
        if BLACK not in row:
            increment += 1
            for x in range(GRID_WIDTH):
                try:
                    del locked_positions[(x, y)]
                except KeyError:
                    continue
    if increment > 0:
        for key in sorted(list(locked_positions), key=lambda k: k[1])[::-1]:
            x, y = key
            if y < y + increment:
                new_key = (x, y + increment)
                locked_positions[new_key] = locked_positions.pop(key)
    return increment

def main():
    """Main game loop"""
    locked_positions = {}  # Positions of locked pieces
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    current_piece = get_new_piece()
    next_piece = get_new_piece()
    clock = pygame.time.Clock()
    fall_time = 0

    while run:
        grid = create_grid(locked_positions)
        fall_speed = 0.27

        fall_time += clock.get_rawtime()
        clock.tick()

        # Handle falling pieces
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        # Handle user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotate()
                    if not valid_space(current_piece, grid):
                        current_piece.rotate()
                        current_piece.rotate()
                        current_piece.rotate()

        # Update grid with current piece position
        shape_pos = convert_shape_format(current_piece)
        for x, y in shape_pos:
            if y >= 0:
                grid[y][x] = current_piece.color

        # Lock piece and generate new piece if needed
        if change_piece:
            for x, y in shape_pos:
                locked_positions[(x, y)] = current_piece.color
            current_piece = next_piece
            next_piece = get_new_piece()
            change_piece = False
            clear_rows(grid, locked_positions)

        # Draw everything
        draw_grid(screen, grid)
        draw_piece(screen, current_piece)
        pygame.display.update()

    pygame.display.quit()

if __name__ == "__main__":
    main()