import random
from typing import List, Tuple
from mancala_ai.game.board import Board
from mancala_ai.game.rules import GameRules
from mancala_ai.ai.minimax import MinimaxAI
from mancala_ai.ai.evaluation import EvaluationFunctions

class Agent:
    """Base class for all game agents."""
    
    def get_move(self, board: Board) -> int:
        """Get the next move for the current board state."""
        raise NotImplementedError

class RandomAgent(Agent):
    """Agent that makes random valid moves."""
    
    def get_move(self, board: Board) -> int:
        valid_moves = GameRules.get_legal_moves(board)
        if not valid_moves:
            raise ValueError("No valid moves available")
        return random.choice(valid_moves)

class GreedyAgent(Agent):
    """Agent that always picks the move that maximizes immediate score gain."""
    
    def get_move(self, board: Board) -> int:
        valid_moves = GameRules.get_legal_moves(board)
        if not valid_moves:
            raise ValueError("No valid moves available")
            
        best_score = float('-inf')
        best_move = None
        
        for move in valid_moves:
            board_copy = board.clone()
            is_valid, gets_extra_turn = GameRules.make_move(board_copy, move)
            
            if not is_valid:
                continue
                
            # Calculate score difference
            score_diff = (board_copy.stores[board.current_player] - 
                         board.stores[board.current_player])
            
            if score_diff > best_score:
                best_score = score_diff
                best_move = move
                
        return best_move if best_move is not None else valid_moves[0]

class MinimaxAgent(Agent):
    """Agent that uses Minimax algorithm."""

    def __init__(self, depth: int = 3):
        self.ai = MinimaxAI(max_depth=depth, evaluation_func=EvaluationFunctions.advanced_evaluation)

    def get_move(self, board: Board) -> int:
        return self.ai.get_best_move(board)


class IterativeDeepeningAgent(Agent):
    """Agent that uses Iterative Deepening with time limit."""

    def __init__(self, time_limit: float = 5.0):
        from mancala_ai.ai.iterative import IterativeDeepeningAI
        from mancala_ai.ai.evaluation import EvaluationFunctions
        self.ai = IterativeDeepeningAI(
            time_limit=time_limit,
            max_depth=10,
            evaluation_func=EvaluationFunctions.advanced_evaluation
        )

    def get_move(self, board: Board) -> int:
        move, _ = self.ai.get_best_move(board)
        return move

def get_available_agents() -> List[Tuple[str, type]]:
    """Get list of available agents."""
    return [
        ("Random", RandomAgent),
        ("Greedy", GreedyAgent),
        ("Minimax", MinimaxAgent),
        ("IterativeDeepening", IterativeDeepeningAgent)
    ] 