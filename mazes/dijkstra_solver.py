import pygame
import random
import time
import heapq

# --- Pygame Initialization ---
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
GRAY = (100, 100, 100)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Solver with Dijkstra's Algorithm")

# Maze dimensions
CELL_SIZE = 20
ROWS = SCREEN_HEIGHT // CELL_SIZE
COLS = SCREEN_WIDTH // CELL_SIZE
FPS = 60

# --- Maze Cell Class ---
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

    def __lt__(self, other):
        # This is needed for heapq to work with Cell objects
        return False

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

# --- Dijkstra's Maze Solver Function ---
def solve_maze(grid):
    start_cell = grid[0][0]
    end_cell = grid[ROWS - 1][COLS - 1]
    
    # Dijkstra's uses a priority queue based on the cost from the start (g_score)
    # The queue stores tuples of (g_score, cell)
    open_set = [(0, start_cell)]
    
    # Dictionary to reconstruct the path after finding the solution
    came_from = {}
    
    # Dictionary to store the cost from start to a cell
    g_score = {cell: float('inf') for row in grid for cell in row}
    g_score[start_cell] = 0
    
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

        # Visualization of the search process
        # Color the cells in the open set (currently being considered)
        for g, cell in open_set:
            pygame.draw.rect(screen, ORANGE, (cell.x * CELL_SIZE, cell.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Color the cells that have been fully evaluated
        for cell in g_score:
            if g_score[cell] != float('inf') and cell != start_cell and cell not in [item[1] for item in open_set]:
                pygame.draw.rect(screen, CYAN, (cell.x * CELL_SIZE, cell.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        # Check if the open set is empty (no solution)
        if not open_set:
            running = False
            print("No solution found!")
            break

        # Get the cell with the lowest g_score from the priority queue
        current_g, current_cell = heapq.heappop(open_set)

        # If the end is reached, reconstruct the path and break
        if current_cell == end_cell:
            path = []
            while current_cell in came_from:
                path.append(current_cell)
                current_cell = came_from[current_cell]
            path.append(start_cell)
            path.reverse()
            
            # Final path visualization
            for cell in path:
                pygame.draw.rect(screen, BLUE, (cell.x * CELL_SIZE + CELL_SIZE//4, cell.y * CELL_SIZE + CELL_SIZE//4, CELL_SIZE//2, CELL_SIZE//2))
            
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False
            break

        # Check neighbors
        neighbor_coords = [
            (current_cell.x, current_cell.y - 1, 'top'),
            (current_cell.x + 1, current_cell.y, 'right'),
            (current_cell.x, current_cell.y + 1, 'bottom'),
            (current_cell.x - 1, current_cell.y, 'left')
        ]
        
        for nx, ny, wall_to_check in neighbor_coords:
            if 0 <= nx < COLS and 0 <= ny < ROWS:
                neighbor = grid[ny][nx]
                
                # Check if there is no wall between current and neighbor
                if not current_cell.walls[wall_to_check]:
                    tentative_g_score = g_score[current_cell] + 1 # cost to move is 1
                    
                    if tentative_g_score < g_score[neighbor]:
                        # This path is better than a previously found one
                        came_from[neighbor] = current_cell
                        g_score[neighbor] = tentative_g_score
                        
                        # Add the neighbor to the open set
                        heapq.heappush(open_set, (g_score[neighbor], neighbor))
        
        pygame.draw.rect(screen, GREEN, (start_cell.x * CELL_SIZE, start_cell.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, (end_cell.x * CELL_SIZE, end_cell.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)
    
    pygame.quit()

# Run the maze solver
if __name__ == '__main__':
    try:
        maze_grid = create_maze()
        solve_maze(maze_grid)
    except pygame.error as e:
        print(f"Pygame error: {e}. Make sure Pygame is correctly installed.")
