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
        - Capture opportunities (steals)
        - Extra turn opportunities
        - Empty pits (can be good for capturing)
        - Vulnerability to steals (avoid leaving stones in pits adjacent to empty pits)
        - Penalty rule considerations
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
        
        # Steal opportunity evaluation (capture opportunities)
        steal_score = 0
        for i in range(Board.PITS_PER_PLAYER):
            if board.pits[player][i] == 0:
                opposite_pit = Board.PITS_PER_PLAYER - 1 - i
                opposite_stones = board.pits[1 - player][opposite_pit]
                if opposite_stones > 0:
                    # More valuable if opponent has more stones to steal
                    steal_score += opposite_stones * 0.3
        
        # Vulnerability to steals evaluation
        vulnerability_score = 0
        for i in range(Board.PITS_PER_PLAYER):
            player_stones = board.pits[player][i]
            if player_stones > 0:
                # Check if opponent has an empty pit opposite to this one
                opposite_pit = Board.PITS_PER_PLAYER - 1 - i
                if board.pits[1 - player][opposite_pit] == 0:
                    # Penalize having stones in pits that can be stolen from
                    # More penalty for more stones
                    vulnerability_score -= player_stones * 0.4
        
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
        
        # Penalty rule evaluation
        penalty_score = 0
        # Check if current player would trigger penalty rule
        player_store = board.stores[player]
        player_closest_pit = board.pits[player][Board.PITS_PER_PLAYER - 1]
        if player_store == player_closest_pit and player_store > 0:
            # Penalize configurations that would trigger the penalty rule
            penalty_score -= 2.0
        
        # Check if opponent would trigger penalty rule (good for us)
        opponent_store = board.stores[1 - player]
        opponent_closest_pit = board.pits[1 - player][Board.PITS_PER_PLAYER - 1]
        if opponent_store == opponent_closest_pit and opponent_store > 0:
            # Reward configurations where opponent would trigger penalty
            penalty_score += 1.5
        
        # Combine all components with weights
        return (basic_score * 1.0 + 
                position_score * 0.3 + 
                steal_score * 0.5 +
                vulnerability_score * 0.6 +
                extra_turn_score * 0.4 +
                empty_pits_score * 0.1 +
                penalty_score * 0.8)
    
    @staticmethod
    def get_evaluation_functions() -> List[callable]:
        """Get list of available evaluation functions."""
        return [
            EvaluationFunctions.basic_evaluation,
            EvaluationFunctions.advanced_evaluation
        ] 