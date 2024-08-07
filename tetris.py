import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 800  # Full window dimensions
PLAY_WIDTH, PLAY_HEIGHT = 300, 600  # Dimensions of the game area
BLOCK_SIZE = 30  # Size of each block in pixels

# Top left coordinates of the play area
TOP_LEFT_X = (WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = HEIGHT - PLAY_HEIGHT - 50  # Ensuring space for the title

# Define the shapes and their colors
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['.....',
      '..0..',
      '..0..',
      '..0..',
      '..0..'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
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
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
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
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
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
      '.....']]

# List of shapes and their colors
SHAPES = [S, Z, I, O, J, L, T]
SHAPE_COLORS = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

# Define Piece class
class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0

# Create a grid for the game area
def create_grid(locked_positions={}):
    grid = [[(0,0,0) for x in range(10)] for y in range(20)]  # Empty grid
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in locked_positions:
                color = locked_positions[(x, y)]
                grid[y][x] = color
    return grid

# Convert shape format to grid coordinates
def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j, piece.y + i))
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    return positions

# Check if the piece fits in the grid
def valid_space(piece, grid):
    accepted_positions = [[(x, y) for x in range(10) if grid[y][x] == (0, 0, 0)] for y in range(20)]
    accepted_positions = [x for item in accepted_positions for x in item]
    formatted = convert_shape_format(piece)
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

# Check if the game is lost
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

# Generate a new piece
def get_new_piece():
    return Piece(5, 0, random.choice(SHAPES))

# Draw grid lines on the game area
def draw_grid(surface, grid):
    for y in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (TOP_LEFT_X, TOP_LEFT_Y + y * BLOCK_SIZE), (TOP_LEFT_X + PLAY_WIDTH, TOP_LEFT_Y + y * BLOCK_SIZE))
        for x in range(len(grid[y])):
            pygame.draw.line(surface, (128, 128, 128), (TOP_LEFT_X + x * BLOCK_SIZE, TOP_LEFT_Y), (TOP_LEFT_X + x * BLOCK_SIZE, TOP_LEFT_Y + PLAY_HEIGHT))

# Clear full rows and move down the remaining rows
def clear_rows(grid, locked):
    increment = 0
    for y in range(len(grid) - 1, -1, -1):
        row = grid[y]
        if (0, 0, 0) not in row:
            increment += 1
            index = y
            for x in range(len(row)):
                try:
                    del locked[(x, y)]
                except:
                    continue
    if increment > 0:
        for key in sorted(list(locked), key=lambda k: k[1])[::-1]:
            x, y = key
            if y < index:
                new_key = (x, y + increment)
                locked[new_key] = locked.pop(key)
    return increment

# Draw the next shape preview
def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comic sans ms', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))
    start_x = TOP_LEFT_X + PLAY_WIDTH + 50
    start_y = TOP_LEFT_Y + (PLAY_HEIGHT // 2 - 100)
    format = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (start_x + j * BLOCK_SIZE, start_y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    surface.blit(label, (start_x + 10, start_y - 30))

# Draw the game window
def draw_window(surface, grid, score=0):
    surface.fill((0, 0, 0))  # Fill background with black
    pygame.font.init()
    font = pygame.font.SysFont('comic sans ms', 60)
    label = font.render('Tetris', 1, (255, 255, 255))  # Title
    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH / 2 - (label.get_width() / 2), 10))  # Position title at the top
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(surface, grid[y][x], (TOP_LEFT_X + x * BLOCK_SIZE, TOP_LEFT_Y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    draw_grid(surface, grid)
    pygame.draw.rect(surface, (0, 255, 255), (TOP_LEFT_X - 5, TOP_LEFT_Y - 5, PLAY_WIDTH + 10, PLAY_HEIGHT + 10), 5)  # Cyan border

# Main game loop
def main():
    locked_positions = {}
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
        
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True
        
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
                    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)
        
        shape_pos = convert_shape_format(current_piece)
        
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color
        
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_new_piece()
            change_piece = False
            clear_rows(grid, locked_positions)
        
        draw_window(win, grid)
        draw_next_shape(next_piece, win)
        pygame.display.update()
        
        if check_lost(locked_positions):
            run = False
    
    draw_text_middle("Game Over", 80, (255, 255, 255), win)
    pygame.display.update()
    pygame.time.delay(2000)

# Initialize the Pygame window and main menu
def main_menu():
    global win
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Tetris')
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle('Press Any Key To Play', 60, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()
    pygame.display.quit()

# Draw text in the middle of the screen
def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comic sans ms', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH / 2 - (label.get_width() / 2), TOP_LEFT_Y + PLAY_HEIGHT / 2 - (label.get_height() / 2)))

# Start the game with the main menu
main_menu()