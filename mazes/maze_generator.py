import pygame
import random
import time

# --- Pygame Initialization ---
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)
BLUE = (0, 0, 255)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Recursive Backtracking Maze Generator")

# Maze dimensions
CELL_SIZE = 20
ROWS = SCREEN_HEIGHT // CELL_SIZE
COLS = SCREEN_WIDTH // CELL_SIZE
FPS = 60

# --- Maze Cell Class ---
class Cell:
    def __init__(self, x, y):
        # Coordinates of the cell in the grid
        self.x, self.y = x, y
        # Walls: top, right, bottom, left
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.is_current = False

    def draw(self, surface):
        # Draw the cell and its walls on the screen
        x, y = self.x * CELL_SIZE, self.y * CELL_SIZE
        if self.visited:
            pygame.draw.rect(surface, GRAY, (x, y, CELL_SIZE, CELL_SIZE))
        if self.is_current:
            pygame.draw.rect(surface, BLUE, (x, y, CELL_SIZE, CELL_SIZE))

        # Draw the walls
        if self.walls['top']:
            pygame.draw.line(surface, BLACK, (x, y), (x + CELL_SIZE, y))
        if self.walls['right']:
            pygame.draw.line(surface, BLACK, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE))
        if self.walls['bottom']:
            pygame.draw.line(surface, BLACK, (x + CELL_SIZE, y + CELL_SIZE), (x, y + CELL_SIZE))
        if self.walls['left']:
            pygame.draw.line(surface, BLACK, (x, y + CELL_SIZE), (x, y))

    def get_neighbors(self, grid):
        # Find unvisited neighbors of the current cell
        neighbors = []
        # Relative coordinates of neighbors
        neighbor_coords = [
            (self.x, self.y - 1, 'top', 'bottom'), # Top
            (self.x + 1, self.y, 'right', 'left'), # Right
            (self.x, self.y + 1, 'bottom', 'top'), # Bottom
            (self.x - 1, self.y, 'left', 'right')  # Left
        ]

        for nx, ny, wall1, wall2 in neighbor_coords:
            if 0 <= nx < COLS and 0 <= ny < ROWS:
                neighbor = grid[ny][nx]
                if not neighbor.visited:
                    neighbors.append((neighbor, wall1, wall2))
        return neighbors

# --- Maze Generation Function ---
def generate_maze():
    # Create a 2D grid of Cell objects
    grid = [[Cell(x, y) for x in range(COLS)] for y in range(ROWS)]
    
    # Use a stack to keep track of the path for backtracking
    stack = []
    
    # Choose a random starting cell
    current_cell = grid[0][0]
    current_cell.visited = True
    current_cell.is_current = True
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        screen.fill(WHITE)

        # Draw the grid
        for row in grid:
            for cell in row:
                cell.draw(screen)

        # Get unvisited neighbors
        neighbors = current_cell.get_neighbors(grid)

        if neighbors:
            # Pick a random neighbor
            next_cell, wall1, wall2 = random.choice(neighbors)
            
            # Push the current cell to the stack for backtracking
            stack.append(current_cell)
            current_cell.is_current = False
            
            # Knock down the wall between the current and next cell
            current_cell.walls[wall1] = False
            next_cell.walls[wall2] = False
            
            # Move to the next cell
            current_cell = next_cell
            current_cell.visited = True
            current_cell.is_current = True
        elif stack:
            # No unvisited neighbors, so backtrack
            current_cell.is_current = False
            current_cell = stack.pop()
            current_cell.is_current = True
        else:
            # The stack is empty, meaning the maze is fully generated
            running = False
            
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

    # Final rendering of the maze
    screen.fill(WHITE)
    for row in grid:
        for cell in row:
            cell.is_current = False # Clear the current cell highlight
            cell.draw(screen)
    pygame.display.flip()
    
    # Wait before quitting
    pygame.time.wait(2000)
    pygame.quit()
    
# Run the maze generator
if __name__ == '__main__':
    try:
        generate_maze()
    except pygame.error as e:
        print(f"Pygame error: {e}. Make sure Pygame is correctly installed.")

