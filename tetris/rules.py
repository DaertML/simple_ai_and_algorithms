# --- Rules for the Tetris AI ---

# A dictionary of weights for each heuristic.
# You can adjust these values to change the AI's strategy.
# A higher positive weight means the AI tries to maximize the score for that feature.
# A higher negative weight means the AI tries to minimize the score for that feature.
WEIGHTS = {
    'height': -0.51,
    'lines_cleared': 0.76,
    'holes': -0.36,
    'bumpiness': -0.18,
}

def score_board(grid, final_piece_position):
    """
    Scores a board state after a piece has been placed.
    
    Args:
        grid (Grid): The grid object from tetris.py.
        final_piece_position (tuple): A tuple containing the final (x, y) of the piece.

    Returns:
        float: The calculated score based on the defined heuristics.
    """
    
    # 1. Simulate placing the piece
    temp_grid = [row[:] for row in grid.grid]
    piece_x, piece_y = final_piece_position
    
    # A simple way to check lines cleared in the simulation.
    temp_grid_score = 0
    
    # Place the piece
    for y, row in enumerate(grid.grid):
        for x, cell in enumerate(row):
            if (x, y) in final_piece_position[2]:  # Using a placeholder for the placed piece cells
                temp_grid[y][x] = 1 # Mark as filled

    # Count lines cleared
    lines_cleared = 0
    for row in temp_grid:
        if all(cell != (0,0,0) for cell in row):
            lines_cleared += 1

    # 2. Calculate the board's features (heuristics)
    height = 0
    for col in range(grid.width):
        for row in range(grid.height):
            if temp_grid[row][col] != (0,0,0):
                height += grid.height - row
                break

    holes = 0
    for col in range(grid.width):
        found_block = False
        for row in range(grid.height):
            if temp_grid[row][col] != (0,0,0):
                found_block = True
            elif found_block:
                holes += 1

    bumpiness = 0
    column_heights = [0] * grid.width
    for col in range(grid.width):
        for row in range(grid.height):
            if temp_grid[row][col] != (0,0,0):
                column_heights[col] = grid.height - row
                break
    
    for i in range(grid.width - 1):
        bumpiness += abs(column_heights[i] - column_heights[i+1])

    # 3. Calculate the weighted score
    score = (
        WEIGHTS['height'] * height +
        WEIGHTS['lines_cleared'] * lines_cleared +
        WEIGHTS['holes'] * holes +
        WEIGHTS['bumpiness'] * bumpiness
    )

    return score

