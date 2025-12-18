import minesweeper

def find_certain_moves(board):
    """
    Applies logical rules to find certain moves (reveals or flags).
    
    Args:
        board (minesweeper.Board): The current game board.

    Returns:
        list: A list of moves, where each move is a tuple: ((row, col), 'action').
    """
    moves = []
    
    for r in range(board.height):
        for c in range(board.width):
            cell = board.grid[r][c]
            if cell.is_revealed and cell.adjacent_mines > 0:
                
                hidden_neighbors = []
                flagged_neighbors = []
                
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        nr, nc = r + i, c + j
                        if 0 <= nr < board.height and 0 <= nc < board.width:
                            neighbor = board.grid[nr][nc]
                            if not neighbor.is_revealed:
                                if neighbor.is_flagged:
                                    flagged_neighbors.append(neighbor)
                                else:
                                    hidden_neighbors.append(neighbor)

                # Rule 1: If adjacent_mines equals the number of hidden neighbors,
                # then all hidden neighbors are mines. Flag them.
                if cell.adjacent_mines == len(hidden_neighbors) + len(flagged_neighbors):
                    for neighbor in hidden_neighbors:
                        moves.append(((neighbor.row, neighbor.col), 'flag'))

                # Rule 2: If adjacent_mines equals the number of flagged neighbors,
                # then all remaining hidden neighbors are safe. Reveal them.
                if cell.adjacent_mines == len(flagged_neighbors):
                    for neighbor in hidden_neighbors:
                        moves.append(((neighbor.row, neighbor.col), 'reveal'))
                        
    return moves
