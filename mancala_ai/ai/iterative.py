import time
from typing import Tuple, Optional
from mancala_ai.game.board import Board
from mancala_ai.ai.minimax import MinimaxAI

class IterativeDeepeningAI:
    """Implements iterative deepening with time limit for the Minimax algorithm."""
    
    def __init__(self,
                 max_depth: int = 10,
                 time_limit: float = 5.0,
                 evaluation_func = None):
        """
        Initialize the AI.
        
        Args:
            max_depth: Maximum search depth
            time_limit: Time limit per move in seconds
            evaluation_func: Function to evaluate board states
        """
        self.max_depth = max_depth
        self.time_limit = time_limit
        self.evaluation_func = evaluation_func
        self.minimax_ai = MinimaxAI(max_depth=1, evaluation_func=evaluation_func)
        self.last_depth = 0
        self.last_nodes = 0
        
    def get_best_move(self, board: Board) -> Tuple[int, int]:
        """
        Get the best move using iterative deepening.
        Returns: (best_move, depth_reached)
        """
        start_time = time.time()
        best_move = None
        depth_reached = 0
        
        # Start with depth 1 and increase until time limit
        for depth in range(1, self.max_depth + 1):
            if time.time() - start_time >= self.time_limit:
                break
                
            self.minimax_ai.max_depth = depth
            try:
                move = self.minimax_ai.get_best_move(board)
                if move is not None:
                    best_move = move
                    depth_reached = depth
                    self.last_depth = depth
                    self.last_nodes = self.minimax_ai.nodes_evaluated
            except ValueError:
                break
                
        if best_move is None:
            raise ValueError("No valid moves found")
            
        return best_move, depth_reached
    
    def get_last_search_stats(self) -> Tuple[int, int]:
        """Get statistics about the last search."""
        return self.last_depth, self.last_nodes 