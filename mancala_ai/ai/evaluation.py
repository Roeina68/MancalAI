from typing import List
import numpy as np
from mancala_ai.game.board import Board

class EvaluationFunctions:
    """Collection of evaluation functions for the Mancala game."""
    
    @staticmethod
    def basic_evaluation(board: Board, player: int) -> float:
        """
        Basic evaluation function that considers:
        - Difference in stores
        - Difference in available stones
        - Extra turn opportunities
        """
        # Get scores
        player_score = board.stores[player]
        opponent_score = board.stores[1 - player]
        
        # Get available stones
        player_stones = np.sum(board.pits[player])
        opponent_stones = np.sum(board.pits[1 - player])
        
        # Calculate score difference
        score_diff = player_score - opponent_score
        stones_diff = player_stones - opponent_stones
        
        # Weight the components
        return score_diff * 2.0 + stones_diff * 0.5
    
    @staticmethod
    def advanced_evaluation(board: Board, player: int) -> float:
        """
        Advanced evaluation function that considers:
        - Basic evaluation components
        - Position of stones (stones closer to store are more valuable)
        - Capture opportunities
        - Extra turn opportunities
        - Empty pits (can be good for capturing)
        """
        # Get basic evaluation
        basic_score = EvaluationFunctions.basic_evaluation(board, player)
        
        # Position-based evaluation
        position_score = 0
        for i in range(Board.PITS_PER_PLAYER):
            # Stones closer to store are more valuable
            position_weight = (i + 1) / Board.PITS_PER_PLAYER
            position_score += board.pits[player][i] * position_weight
            position_score -= board.pits[1 - player][i] * position_weight
        
        # Capture opportunity evaluation
        capture_score = 0
        for i in range(Board.PITS_PER_PLAYER):
            if board.pits[player][i] == 0:
                opposite_pit = Board.PITS_PER_PLAYER - 1 - i
                if board.pits[1 - player][opposite_pit] > 0:
                    capture_score += 1
        
        # Extra turn opportunity evaluation
        extra_turn_score = 0
        for i in range(Board.PITS_PER_PLAYER):
            stones = board.pits[player][i]
            if stones > 0:
                # Check if this move would end in player's store
                if (i + stones) % (Board.PITS_PER_PLAYER + 1) == Board.PITS_PER_PLAYER:
                    extra_turn_score += 1
        
        # Empty pits evaluation (can be good for capturing)
        empty_pits_score = 0
        for i in range(Board.PITS_PER_PLAYER):
            if board.pits[player][i] == 0:
                empty_pits_score += 0.5
        
        # Combine all components with weights
        return (basic_score * 1.0 + 
                position_score * 0.3 + 
                capture_score * 0.2 +
                extra_turn_score * 0.4 +
                empty_pits_score * 0.1)
    
    @staticmethod
    def get_evaluation_functions() -> List[callable]:
        """Get list of available evaluation functions."""
        return [
            EvaluationFunctions.basic_evaluation,
            EvaluationFunctions.advanced_evaluation
        ] 