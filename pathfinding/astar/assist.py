import heapq
import random

# --- Generic Proving System Components ---

class Property:
    """Represents a logical property of an algorithm's output."""
    def __init__(self, name, check_function):
        self.name = name
        self.check_function = check_function

    def check(self, input_data, output_data):
        return self.check_function(input_data, output_data)

class Proof:
    """A generic class for an inductive proof."""
    def __init__(self, algorithm_to_prove, properties):
        self.algorithm = algorithm_to_prove
        self.properties = properties
        self.log = []

    def log_step(self, message, status="INFO"):
        self.log.append(f"[{status}] {message}")

    def run_base_case(self):
        raise NotImplementedError("Subclasses must implement run_base_case()")

    def run_inductive_step(self, num_tests=100):
        raise NotImplementedError("Subclasses must implement run_inductive_step()")
        
    def get_log(self):
        return "\n".join(self.log)

# --- A* Specific Utilities ---

class Node:
    """Represents a node in the grid."""
    def __init__(self, x, y, cost):
        self.x, self.y, self.cost = x, y, cost
        self.g = float('inf')  # Cost from start
        self.h = 0             # Heuristic to end
        self.f = float('inf')  # Total cost (g + h)
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f

def get_neighbors(grid, node):
    """Returns valid neighbors of a node."""
    neighbors = []
    x, y = node.x, node.y
    rows, cols = len(grid), len(grid[0])
    possible_moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for dx, dy in possible_moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != -1:
            neighbors.append(Node(nx, ny, grid[nx][ny]))
    return neighbors

def get_path(node):
    """Reconstructs the path from a node's parents."""
    path = []
    current = node
    while current:
        path.append((current.x, current.y))
        current = current.parent
    return path[::-1]

def find_optimal_cost(grid, start, end):
    """
    Finds the true optimal cost using a simple breadth-first search.
    Used as a reference for the proof's 'optimality' property.
    """
    queue = [(0, start)]  # (cost, node_coords)
    visited = {start: 0}
    while queue:
        cost, (x, y) = heapq.heappop(queue)
        if (x, y) == end:
            return cost
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] != -1:
                new_cost = cost + grid[nx][ny]
                if new_cost < visited.get((nx, ny), float('inf')):
                    visited[(nx, ny)] = new_cost
                    heapq.heappush(queue, (new_cost, (nx, ny)))
    return float('inf')

def is_valid_path(grid, path):
    """Checks if a path is a sequence of valid, connected nodes."""
    if not path:
        return False
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i+1]
        if abs(x1 - x2) + abs(y1 - y2) > 1:
            return False
        if grid[x2][y2] == -1:
            return False
    return True

### 2. The Correct and Buggy A* Implementations

#Here are two implementations to be tested by our proof system.

#### Correct A* Implementation

#```python
def astar_correct(grid, start_coords, end_coords):
    start_node = Node(start_coords[0], start_coords[1], grid[start_coords[0]][start_coords[1]])
    start_node.g, start_node.f = 0, 0
    end_node_coords = end_coords

    open_set = [start_node]
    closed_set = set()

    def heuristic(node):
        return abs(node.x - end_node_coords[0]) + abs(node.y - end_node_coords[1])

    while open_set:
        current_node = heapq.heappop(open_set)
        if (current_node.x, current_node.y) == end_node_coords:
            return get_path(current_node), current_node.g
        
        closed_set.add((current_node.x, current_node.y))
        
        for neighbor in get_neighbors(grid, current_node):
            if (neighbor.x, neighbor.y) in closed_set:
                continue
            
            new_g = current_node.g + neighbor.cost
            if new_g < neighbor.g:
                neighbor.g = new_g
                neighbor.h = heuristic(neighbor)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.parent = current_node
                heapq.heappush(open_set, neighbor)
    return None, float('inf')

def astar_buggy(grid, start_coords, end_coords):
    start_node = Node(start_coords[0], start_coords[1], grid[start_coords[0]][start_coords[1]])
    start_node.g, start_node.f = 0, 0
    end_node_coords = end_coords
    
    open_set = [start_node]
    closed_set = set()

    def heuristic(node):
        return abs(node.x - end_node_coords[0]) + abs(node.y - end_node_coords[1])

    while open_set:
        current_node = heapq.heappop(open_set)
        if (current_node.x, current_node.y) == end_node_coords:
            return get_path(current_node), current_node.g
        
        closed_set.add((current_node.x, current_node.y))
        
        for neighbor in get_neighbors(grid, current_node):
            if (neighbor.x, neighbor.y) in closed_set:
                continue
            
            # BUG: Only consider the heuristic (h) for the priority queue
            neighbor.h = heuristic(neighbor)
            neighbor.f = neighbor.h  # A* should be f = g + h
            neighbor.parent = current_node
            heapq.heappush(open_set, neighbor)
            
    return None, float('inf')

class AStarProof(Proof):
    def __init__(self, algorithm_to_prove):
        is_optimal_prop = Property(
            name="Optimality Property",
            check_function=lambda input_data, output_data: output_data[1] == input_data["optimal_cost"]
        )
        is_valid_prop = Property(
            name="Validity Property",
            check_function=lambda input_data, output_data: is_valid_path(input_data["grid"], output_data[0])
        )
        super().__init__(algorithm_to_prove, [is_optimal_prop, is_valid_prop])

    def run_base_case(self):
        self.log_step("--- Proving Base Case: Start == End ---")
        grid = [[1, 1], [1, 1]]
        start, end = (0, 0), (0, 0)
        path, cost = self.algorithm(grid, start, end)
        if path != [(0, 0)] or cost != 0:
            self.log_step("Base case failed: start == end.", "FAIL")
            return False
        self.log_step("Base case holds. ✅", "SUCCESS")
        return True

    def run_inductive_step(self, num_tests=100):
        self.log_step("--- Proving Inductive Step ---")
        self.log_step("Hypothesis: Assume A* is correct for simple grids.")
        self.log_step(f"Verifying for {num_tests} random grids...")

        for i in range(num_tests):
            grid_size = random.randint(5, 15)
            grid = [[random.randint(1, 10) for _ in range(grid_size)] for _ in range(grid_size)]
            
            start = (0, 0)
            end = (grid_size - 1, grid_size - 1)
            
            # Find the true optimal cost for our test
            optimal_cost = find_optimal_cost(grid, start, end)
            
            # Run the A* algorithm
            astar_path, astar_cost = self.algorithm(grid, start, end)
            
            # Check the properties
            test_data = {"grid": grid, "optimal_cost": optimal_cost, "start": start, "end": end}
            result_data = (astar_path, astar_cost)

            if astar_path is None:
                self.log_step(f"Test {i+1} failed: No path found.", "FAIL")
                return False

            for prop in self.properties:
                if not prop.check(test_data, result_data):
                    self.log_step(f"Test {i+1} failed for {prop.name}.", "FAIL")
                    self.log_step(f"Grid: {grid}", "INFO")
                    self.log_step(f"Start: {start}, End: {end}", "INFO")
                    self.log_step(f"Optimal Cost: {optimal_cost}, A* Cost: {astar_cost}", "INFO")
                    return False

        self.log_step(f"All {num_tests} property checks passed. Inductive step holds. ✅", "SUCCESS")
        return True

# --- Main Execution ---

if __name__ == "__main__":
    print("= Running Proof on Correct A* =")
    proof_correct = AStarProof(astar_correct)
    if proof_correct.run_base_case() and proof_correct.run_inductive_step():
        print(proof_correct.get_log())
        print("\nCorrect A* verified. ✅")

    print("\n\n= Running Proof on Buggy A* =")
    proof_buggy = AStarProof(astar_buggy)
    if proof_buggy.run_base_case() and proof_buggy.run_inductive_step():
        print(proof_buggy.get_log())
        print("\nBuggy A* verified. ❌")
    else:
        print(proof_buggy.get_log())
        print("\nBuggy A* failed proof. Correctly detected the issue. ✅")
