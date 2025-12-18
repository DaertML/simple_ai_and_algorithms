import pygame
import random
import minesweeper
from rules import find_certain_moves

def get_ai_move(board):
    """
    Decides the next move for the AI.
    
    Args:
        board (minesweeper.Board): The current game board.
    
    Returns:
        tuple: A move in the format: ((row, col), 'action'), or None if no certain move found.
    """
    # 1. Look for certain moves based on rules
    certain_moves = find_certain_moves(board)
    if certain_moves:
        # Return the first certain move found
        return certain_moves[0]
        
    # 2. If no certain moves, we must guess.
    # A simple strategy is to find a random hidden cell and click it.
    hidden_cells = []
    for r in range(board.height):
        for c in range(board.width):
            cell = board.grid[r][c]
            if not cell.is_revealed and not cell.is_flagged:
                hidden_cells.append((r, c))
    
    if hidden_cells:
        row, col = random.choice(hidden_cells)
        return ((row, col), 'reveal')
        
    # No more moves possible
    return None
    
if __name__ == '__main__':
    # Run the main game loop with the AI enabled
    minesweeper.main_loop(ai_enabled=True, get_ai_move_func=get_ai_move)

