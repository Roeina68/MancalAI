from typing import Tuple, Optional
import numpy as np
from mancala_ai.game.board import Board
from mancala_ai.game.rules import GameRules
from mancala_ai.ai.evaluation import EvaluationFunctions

class MinimaxAI:
    """Implements the Minimax algorithm with Alpha-Beta pruning for Mancala."""
    
    def __init__(self, 
                 max_depth: int = 3,  # Reduced default depth
                 evaluation_func: callable = EvaluationFunctions.basic_evaluation):  # Using simpler evaluation
        """
        Initialize the AI.
        
        Args:
            max_depth: Maximum search depth
            evaluation_func: Function to evaluate board states
        """
        self.max_depth = max_depth
        self.evaluation_func = evaluation_func
        self.nodes_evaluated = 0
    
    def get_best_move(self, board: Board) -> int:
        """
        Get the best move for the current player using Minimax with Alpha-Beta pruning.
        """
        self.nodes_evaluated = 0
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        
        # Get valid moves
        valid_moves = GameRules.get_legal_moves(board)
        if not valid_moves:
            raise ValueError("No valid moves available")
            
        # Try each move
        for move in valid_moves:
            # Make move
            board_copy = board.clone()
            is_valid, gets_extra_turn = GameRules.make_move(board_copy, move)
            
            if not is_valid:
                continue
                
            # If player gets extra turn, it's still their turn
            current_player = board.current_player if gets_extra_turn else 1 - board.current_player
            
            # Evaluate move
            score = self._minimax(board_copy, 
                                self.max_depth - 1,
                                alpha,
                                beta,
                                current_player,
                                True)  # Always start with maximizing for current player
            
            if score > best_score:
                best_score = score
                best_move = move
                
            alpha = max(alpha, best_score)
            
        if best_move is None:
            # If no move was evaluated as better, pick the first valid move
            best_move = valid_moves[0]
            
        return best_move
    
    def _minimax(self,
                 board: Board,
                 depth: int,
                 alpha: float,
                 beta: float,
                 current_player: int,
                 is_maximizing: bool) -> float:
        """
        Recursive Minimax implementation with Alpha-Beta pruning.
        """
        self.nodes_evaluated += 1
        
        # Check terminal conditions
        is_game_over, winner = GameRules.get_game_result(board)
        if is_game_over:
            if winner == -1:  # Draw
                return 0
            return float('inf') if winner == board.current_player else float('-inf')
            
        if depth == 0:
            return self.evaluation_func(board, board.current_player)
            
        valid_moves = GameRules.get_legal_moves(board)
        if not valid_moves:
            return self.evaluation_func(board, board.current_player)
            
        if is_maximizing:
            max_eval = float('-inf')
            for move in valid_moves:
                board_copy = board.clone()
                is_valid, gets_extra_turn = GameRules.make_move(board_copy, move)
                
                if not is_valid:
                    continue
                    
                # If player gets extra turn, keep maximizing, otherwise minimize
                next_player = current_player if gets_extra_turn else 1 - current_player
                next_is_maximizing = gets_extra_turn
                
                eval_score = self._minimax(board_copy,
                                         depth - 1,
                                         alpha,
                                         beta,
                                         next_player,
                                         next_is_maximizing)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                board_copy = board.clone()
                is_valid, gets_extra_turn = GameRules.make_move(board_copy, move)
                
                if not is_valid:
                    continue
                    
                # If player gets extra turn, keep minimizing, otherwise maximize
                next_player = current_player if gets_extra_turn else 1 - current_player
                next_is_maximizing = not gets_extra_turn
                
                eval_score = self._minimax(board_copy,
                                         depth - 1,
                                         alpha,
                                         beta,
                                         next_player,
                                         next_is_maximizing)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval 