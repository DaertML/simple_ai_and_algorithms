import pygame
import random

# --- Constants ---
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Tetromino shapes (I, J, L, O, S, T, Z)
SHAPES = [
    # I shape
    [[1, 1, 1, 1]],
    # J shape
    [[1, 0, 0], [1, 1, 1]],
    # L shape
    [[0, 0, 1], [1, 1, 1]],
    # O shape
    [[1, 1], [1, 1]],
    # S shape
    [[0, 1, 1], [1, 1, 0]],
    # T shape
    [[0, 1, 0], [1, 1, 1]],
    # Z shape
    [[1, 1, 0], [0, 1, 1]],
]
# Corresponding colors for each shape
SHAPE_COLORS = [
    (0, 255, 255),  # Cyan
    (0, 0, 255),    # Blue
    (255, 165, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Green
    (128, 0, 128),  # Purple
    (255, 0, 0),    # Red
]

class Piece:
    """Represents a single Tetris piece."""
    def __init__(self, x, y, shape_index):
        self.x = x
        self.y = y
        self.shape_index = shape_index
        self.shape = SHAPES[shape_index]
        self.color = SHAPE_COLORS[shape_index]
        self.rotation = 0

    def rotate(self):
        """Rotates the piece 90 degrees clockwise."""
        self.rotation = (self.rotation + 1) % 4
        self.shape = [list(row) for row in zip(*self.shape[::-1])]
        
class Grid:
    """Manages the Tetris game board."""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[BLACK for _ in range(width)] for _ in range(height)]
        self.score = 0

    def draw(self, screen):
        """Draws the grid and all settled pieces."""
        for y in range(self.height):
            for x in range(self.width):
                # Draw the block itself
                pygame.draw.rect(
                    screen,
                    self.grid[y][x],
                    (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    0
                )
                # Draw a border for each block
                pygame.draw.rect(
                    screen,
                    GRAY,
                    (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    1
                )

    def check_collision(self, piece, dx=0, dy=0):
        """Checks for collision with other pieces or the grid boundaries."""
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    nx = piece.x + x + dx
                    ny = piece.y + y + dy
                    if nx < 0 or nx >= self.width or ny >= self.height or self.grid[ny][nx] != BLACK:
                        return True
        return False
    
    def place_piece(self, piece):
        """Places the current piece onto the grid."""
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[piece.y + y][piece.x + x] = piece.color
        self.score += self.clear_lines()

    def clear_lines(self):
        """Removes any full lines and shifts the grid down."""
        lines_cleared = 0
        new_grid = [row for row in self.grid if not all(cell != BLACK for cell in row)]
        lines_cleared = self.height - len(new_grid)
        self.grid = [[BLACK for _ in range(self.width)] for _ in range(lines_cleared)] + new_grid
        return lines_cleared * 100 # Arbitrary score increase

def draw_text(screen, text, x, y, size=30, color=WHITE):
    """Helper function to draw text on the screen."""
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def get_new_piece():
    """Returns a new random piece at the top of the grid."""
    shape_index = random.randint(0, len(SHAPES) - 1)
    return Piece(GRID_WIDTH // 2 - len(SHAPES[shape_index][0]) // 2, 0, shape_index)

def draw_piece(screen, piece):
    """Draws a piece on the screen."""
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen,
                    piece.color,
                    ((piece.x + x) * BLOCK_SIZE, (piece.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    0
                )
                pygame.draw.rect(
                    screen,
                    WHITE,
                    ((piece.x + x) * BLOCK_SIZE, (piece.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    1
                )

def main_loop(ai_enabled=False, get_ai_move_func=None):
    """
    Main game loop.
    
    ai_enabled: If True, the game will use the AI to play.
    get_ai_move_func: A function to get the AI's next move.
    """
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    game_over = False
    grid = Grid(GRID_WIDTH, GRID_HEIGHT)
    current_piece = get_new_piece()

    # Game state variables
    fall_time = 0
    fall_speed = 500  # ms
    score = 0

    while not game_over:
        if not ai_enabled:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and not grid.check_collision(current_piece, dx=-1):
                        current_piece.x -= 1
                    if event.key == pygame.K_RIGHT and not grid.check_collision(current_piece, dx=1):
                        current_piece.x += 1
                    if event.key == pygame.K_DOWN and not grid.check_collision(current_piece, dy=1):
                        current_piece.y += 1
                    if event.key == pygame.K_UP:
                        current_piece.rotate()
                        if grid.check_collision(current_piece):
                            # Rotate back if the rotation is invalid
                            current_piece.rotate()
                            current_piece.rotate()
                            current_piece.rotate()
                    if event.key == pygame.K_SPACE:
                        while not grid.check_collision(current_piece, dy=1):
                            current_piece.y += 1
                        grid.place_piece(current_piece)
                        current_piece = get_new_piece()
        else: # AI is enabled
            # Get the AI's move and apply it
            # The AI function needs to handle the drop and placement logic
            best_move = get_ai_move_func(grid, current_piece)
            if best_move:
                current_piece.x = best_move['x']
                for _ in range(best_move['rotations']):
                    current_piece.rotate()
                
                # Drop the piece to the bottom
                while not grid.check_collision(current_piece, dy=1):
                    current_piece.y += 1

                grid.place_piece(current_piece)
                current_piece = get_new_piece()
            
            # Reset fall time for the next piece
            fall_time = 0
        
        # Automatic falling
        fall_time += clock.tick(60)
        if fall_time > fall_speed:
            fall_time = 0
            if not grid.check_collision(current_piece, dy=1):
                current_piece.y += 1
            else:
                grid.place_piece(current_piece)
                current_piece = get_new_piece()

        # Check for game over condition
        if grid.check_collision(current_piece):
            game_over = True
        
        # Drawing
        screen.fill(BLACK)
        grid.draw(screen)
        draw_piece(screen, current_piece)
        draw_text(screen, f"Score: {grid.score}", SCREEN_WIDTH - 150, 20)

        pygame.display.flip()

    draw_text(screen, "Game Over", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 40)
    draw_text(screen, f"Final Score: {grid.score}", SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 50, 30)
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    exit()

if __name__ == '__main__':
    # You can change this to False to play the game manually.
    # To run with AI, run the tetris_ai.py script instead.
    main_loop(ai_enabled=False)
