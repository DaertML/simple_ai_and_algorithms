import pygame
import copy
import tetris
from rules import WEIGHTS

def get_best_move(grid, piece):
    """
    Determines the best move for the current piece using a heuristic-based AI.
    
    Args:
        grid (tetris.Grid): The current state of the game grid.
        piece (tetris.Piece): The current piece to be placed.

    Returns:
        dict: A dictionary containing 'x' position and 'rotations' for the best move.
    """
    best_score = float('-inf')
    best_move = None
    
    # Iterate through all possible rotations
    for rotations in range(4):
        rotated_piece = copy.deepcopy(piece)
        for _ in range(rotations):
            rotated_piece.rotate()

        # Iterate through all possible x positions
        for x in range(grid.width - len(rotated_piece.shape[0]) + 1):
            
            # Create a temporary piece for this potential move
            temp_piece = copy.deepcopy(rotated_piece)
            temp_piece.x = x

            # Check if the move is valid (doesn't start in a collision)
            if grid.check_collision(temp_piece):
                continue

            # Simulate dropping the piece
            temp_grid = copy.deepcopy(grid)
            while not temp_grid.check_collision(temp_piece, dy=1):
                temp_piece.y += 1
            
            temp_grid.place_piece(temp_piece)
            
            # Calculate the score for this move
            score = (
                WEIGHTS['lines_cleared'] * temp_grid.score / 100 +
                WEIGHTS['height'] * sum([grid.height - r for r in range(grid.height) if any(temp_grid.grid[r][c] != (0,0,0) for c in range(grid.width))]) +
                WEIGHTS['holes'] * sum([1 for r in range(grid.height) for c in range(grid.width) if temp_grid.grid[r][c] == (0,0,0) and any(temp_grid.grid[i][c] != (0,0,0) for i in range(r))])
            )
            
            # The original `rules.py` was a bit too simple, let's include the logic directly
            # since it's cleaner and more self-contained.
            
            column_heights = [0] * temp_grid.width
            for col in range(temp_grid.width):
                for row in range(temp_grid.height):
                    if temp_grid.grid[row][col] != (0,0,0):
                        column_heights[col] = temp_grid.height - row
                        break
            
            bumpiness = sum(abs(column_heights[i] - column_heights[i+1]) for i in range(temp_grid.width - 1))
            score += WEIGHTS['bumpiness'] * bumpiness

            # Check if this is the best score found so far
            if score > best_score:
                best_score = score
                best_move = {'x': x, 'rotations': rotations}

    return best_move

if __name__ == '__main__':
    # Start the game with the AI enabled.
    tetris.main_loop(ai_enabled=True, get_ai_move_func=get_best_move)

