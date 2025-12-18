import pygame
import random

# --- Constants ---
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BOARD_WIDTH = 20
BOARD_HEIGHT = 20
CELL_SIZE = 30
MINE_COUNT = 50

# Colors
GRAY = (180, 180, 180)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (120, 120, 120)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 128)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)

NUMBER_COLORS = [
    (0, 0, 0),
    BLUE, GREEN, RED, DARK_BLUE,
    MAGENTA, CYAN, YELLOW, BLACK
]

# --- Cell Class ---
class Cell:
    """Represents a single cell on the Minesweeper board."""
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

# --- Board Class ---
class Board:
    """Manages the Minesweeper game board."""
    def __init__(self, width, height, mine_count):
        self.width = width
        self.height = height
        self.mine_count = mine_count
        self.grid = [[Cell(r, c) for c in range(width)] for r in range(height)]
        self.revealed_count = 0
        self.game_over = False
        self.win = False

    def setup_board(self, initial_click_pos):
        """Randomly places mines and calculates adjacent mine counts."""
        mines_placed = 0
        while mines_placed < self.mine_count:
            row = random.randint(0, self.height - 1)
            col = random.randint(0, self.width - 1)
            # Ensure no mine is placed on the initial click or its neighbors
            if not self.grid[row][col].is_mine and (row, col) != initial_click_pos:
                self.grid[row][col].is_mine = True
                mines_placed += 1
        
        for r in range(self.height):
            for c in range(self.width):
                if not self.grid[r][c].is_mine:
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if 0 <= r + i < self.height and 0 <= c + j < self.width and self.grid[r + i][c + j].is_mine:
                                self.grid[r][c].adjacent_mines += 1

    def reveal_cell(self, row, col):
        """Recursively reveals cells, handling mines and empty cells."""
        if not (0 <= row < self.height and 0 <= col < self.width):
            return
        cell = self.grid[row][col]
        
        if cell.is_revealed or cell.is_flagged:
            return

        cell.is_revealed = True
        self.revealed_count += 1

        if cell.is_mine:
            self.game_over = True
            return

        if self.revealed_count == (self.width * self.height) - self.mine_count:
            self.game_over = True
            self.win = True
            return
            
        if cell.adjacent_mines == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (i, j) != (0, 0):
                        self.reveal_cell(row + i, col + j)

    def draw(self, screen, font):
        """Draws the entire board state to the screen."""
        for r in range(self.height):
            for c in range(self.width):
                cell = self.grid[r][c]
                rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)

                if cell.is_revealed:
                    pygame.draw.rect(screen, LIGHT_GRAY, rect)
                    pygame.draw.rect(screen, DARK_GRAY, rect, 1)
                    if cell.is_mine:
                        pygame.draw.circle(screen, BLACK, rect.center, CELL_SIZE // 3)
                    elif cell.adjacent_mines > 0:
                        number_text = font.render(str(cell.adjacent_mines), True, NUMBER_COLORS[cell.adjacent_mines])
                        text_rect = number_text.get_rect(center=rect.center)
                        screen.blit(number_text, text_rect)
                else:
                    pygame.draw.rect(screen, GRAY, rect)
                    pygame.draw.rect(screen, DARK_GRAY, rect, 1)
                    if cell.is_flagged:
                        pygame.draw.polygon(screen, RED, [
                            (rect.centerx, rect.top + 5),
                            (rect.centerx + 5, rect.top + 10),
                            (rect.centerx, rect.top + 15),
                            (rect.centerx - 5, rect.top + 10)
                        ])

def main_loop(ai_enabled=False, get_ai_move_func=None):
    """
    Main game loop for both human and AI play.
    
    Args:
        ai_enabled (bool): If True, the game will be played by the AI.
        get_ai_move_func (function): A function to get the AI's next move.
    """
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Minesweeper")
    font = pygame.font.SysFont('Arial', 20)
    clock = pygame.time.Clock()

    board = Board(BOARD_WIDTH, BOARD_HEIGHT, MINE_COUNT)
    first_click = True

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if not ai_enabled and not board.game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    col = x // CELL_SIZE
                    row = y // CELL_SIZE
                    
                    if first_click:
                        board.setup_board((row, col))
                        board.reveal_cell(row, col)
                        first_click = False
                    else:
                        if event.button == 1: # Left click
                            board.reveal_cell(row, col)
                        elif event.button == 3: # Right click
                            cell = board.grid[row][col]
                            if not cell.is_revealed:
                                cell.is_flagged = not cell.is_flagged
        
        if ai_enabled and not board.game_over and not first_click:
            # AI's turn
            move = get_ai_move_func(board)
            if move:
                (row, col), action = move
                if action == 'reveal':
                    board.reveal_cell(row, col)
                elif action == 'flag':
                    board.grid[row][col].is_flagged = True
            else:
                # No certain move found, AI has to guess.
                # Find a random un-revealed, un-flagged cell.
                hidden_cells = [(r, c) for r in range(board.height) for c in range(board.width)
                                if not board.grid[r][c].is_revealed and not board.grid[r][c].is_flagged]
                if hidden_cells:
                    r, c = random.choice(hidden_cells)
                    board.reveal_cell(r, c)
        elif ai_enabled and first_click:
            # First AI click
            r, c = random.randint(0, board.height - 1), random.randint(0, board.width - 1)
            board.setup_board((r, c))
            board.reveal_cell(r, c)
            first_click = False

        # Drawing
        screen.fill(BLACK)
        board.draw(screen, font)

        if board.game_over:
            if board.win:
                status_text = font.render("You Win!", True, GREEN)
            else:
                status_text = font.render("Game Over", True, RED)
            text_rect = status_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(status_text, text_rect)

        pygame.display.flip()
        clock.tick(10) # AI runs at a limited speed for visual clarity

    pygame.quit()
    exit()

if __name__ == '__main__':
    main_loop(ai_enabled=False)
