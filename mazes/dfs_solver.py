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
RED = (255, 0, 0)
PURPLE = (128, 0, 128)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Solver with DFS Animation")

# Maze dimensions
CELL_SIZE = 20
ROWS = SCREEN_HEIGHT // CELL_SIZE
COLS = SCREEN_WIDTH // CELL_SIZE
FPS = 60

# --- Maze Cell Class (same as generator) ---
class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

    def draw(self, surface):
        x, y = self.x * CELL_SIZE, self.y * CELL_SIZE
        if self.walls['top']:
            pygame.draw.line(surface, BLACK, (x, y), (x + CELL_SIZE, y))
        if self.walls['right']:
            pygame.draw.line(surface, BLACK, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE))
        if self.walls['bottom']:
            pygame.draw.line(surface, BLACK, (x + CELL_SIZE, y + CELL_SIZE), (x, y + CELL_SIZE))
        if self.walls['left']:
            pygame.draw.line(surface, BLACK, (x, y + CELL_SIZE), (x, y))

# --- Maze Generation (for a self-contained solver) ---
def create_maze():
    grid = [[Cell(x, y) for x in range(COLS)] for y in range(ROWS)]
    stack = []
    
    current_cell = grid[random.randint(0, ROWS - 1)][random.randint(0, COLS - 1)]
    current_cell.visited = True
    
    while True:
        neighbors = []
        
        # Relative coordinates of neighbors
        neighbor_coords = [
            (current_cell.x, current_cell.y - 1, 'top', 'bottom'),
            (current_cell.x + 1, current_cell.y, 'right', 'left'),
            (current_cell.x, current_cell.y + 1, 'bottom', 'top'),
            (current_cell.x - 1, current_cell.y, 'left', 'right')
        ]
        
        for nx, ny, wall1, wall2 in neighbor_coords:
            if 0 <= nx < COLS and 0 <= ny < ROWS:
                neighbor = grid[ny][nx]
                if not neighbor.visited:
                    neighbors.append((neighbor, wall1, wall2))
        
        if neighbors:
            next_cell, wall1, wall2 = random.choice(neighbors)
            stack.append(current_cell)
            current_cell.walls[wall1] = False
            next_cell.walls[wall2] = False
            current_cell = next_cell
            current_cell.visited = True
        elif stack:
            current_cell = stack.pop()
        else:
            break
            
    # Reset visited flags for the solver
    for row in grid:
        for cell in row:
            cell.visited = False
            
    return grid

# --- Maze Solver Function ---
def solve_maze(grid):
    # Set the start and end points
    start_cell = grid[0][0]
    end_cell = grid[ROWS - 1][COLS - 1]
    
    # Use a stack for the DFS algorithm
    stack = [start_cell]
    start_cell.visited = True
    
    # Path to visualize the solution
    path = []
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # Fill the screen with white
        screen.fill(WHITE)
        
        # Draw the maze
        for row in grid:
            for cell in row:
                cell.draw(screen)

        # Animate the path
        for cell in path:
            pygame.draw.rect(screen, PURPLE, (cell.x * CELL_SIZE + CELL_SIZE//4, cell.y * CELL_SIZE + CELL_SIZE//4, CELL_SIZE//2, CELL_SIZE//2))

        # Check if the end is reached
        if not stack or stack[-1] == end_cell:
            running = False
            break
            
        current_cell = stack[-1]
        
        # Check neighbors for a path
        next_cell = None
        # Relative coordinates of neighbors
        neighbor_coords = [
            (current_cell.x, current_cell.y - 1, 'top'),
            (current_cell.x + 1, current_cell.y, 'right'),
            (current_cell.x, current_cell.y + 1, 'bottom'),
            (current_cell.x - 1, current_cell.y, 'left')
        ]
        
        for nx, ny, wall_to_check in neighbor_coords:
            if 0 <= nx < COLS and 0 <= ny < ROWS:
                neighbor = grid[ny][nx]
                # Check if there is no wall and the neighbor hasn't been visited
                if not current_cell.walls[wall_to_check] and not neighbor.visited:
                    next_cell = neighbor
                    break
        
        if next_cell:
            # If a valid, unvisited neighbor is found, move to it
            next_cell.visited = True
            stack.append(next_cell)
            path.append(current_cell) # Add the current cell to the path visualization
        else:
            # If no unvisited neighbors, backtrack by popping from the stack
            if len(path) > 0:
                backtracked_cell = path.pop()
                # Change the color of the backtracked cell to show the process
                pygame.draw.rect(screen, GRAY, (backtracked_cell.x * CELL_SIZE + CELL_SIZE//4, backtracked_cell.y * CELL_SIZE + CELL_SIZE//4, CELL_SIZE//2, CELL_SIZE//2))
            stack.pop() # Pop from the main stack
            
        pygame.draw.rect(screen, GREEN, (start_cell.x * CELL_SIZE, start_cell.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, (end_cell.x * CELL_SIZE, end_cell.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)
    
    # Final rendering of the solution path
    screen.fill(WHITE)
    for row in grid:
        for cell in row:
            cell.draw(screen)
            
    # Draw the final path without the backtracking visualization
    for cell in stack:
        pygame.draw.rect(screen, BLUE, (cell.x * CELL_SIZE + CELL_SIZE//4, cell.y * CELL_SIZE + CELL_SIZE//4, CELL_SIZE//2, CELL_SIZE//2))
    
    pygame.draw.rect(screen, GREEN, (start_cell.x * CELL_SIZE, start_cell.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (end_cell.x * CELL_SIZE, end_cell.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    pygame.display.flip()
    
    # Wait before quitting
    pygame.time.wait(3000)
    pygame.quit()

# Run the maze solver
if __name__ == '__main__':
    try:
        maze_grid = create_maze()
        solve_maze(maze_grid)
    except pygame.error as e:
        print(f"Pygame error: {e}. Make sure Pygame is correctly installed.")

