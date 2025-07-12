import pytest
import numpy as np
from mancala_ai.game.board import Board
from mancala_ai.game.rules import GameRules
from mancala_ai.ai.minimax import MinimaxAI
from mancala_ai.ai.evaluation import EvaluationFunctions
from mancala_ai.ai.iterative import IterativeDeepeningAI

def test_minimax_initialization():
    """Test MinimaxAI initialization."""
    ai = MinimaxAI(max_depth=3)
    assert ai.max_depth == 3
    assert ai.evaluation_func == EvaluationFunctions.basic_evaluation
    
    # Test with custom evaluation function
    ai = MinimaxAI(max_depth=4, 
                   evaluation_func=EvaluationFunctions.basic_evaluation)
    assert ai.max_depth == 4
    assert ai.evaluation_func == EvaluationFunctions.basic_evaluation

def test_minimax_get_best_move():
    """Test getting best move from MinimaxAI."""
    board = Board()
    ai = MinimaxAI(max_depth=2)
    
    # Test with valid board state
    move = ai.get_best_move(board)
    assert 0 <= move < Board.PITS_PER_PLAYER
    assert board.pits[board.current_player][move] > 0
    
    # Test with no valid moves
    board.pits[board.current_player] = 0
    with pytest.raises(ValueError):
        ai.get_best_move(board)

def test_evaluation_functions():
    """Test evaluation functions."""
    board = Board()
    
    # Test basic evaluation
    score = EvaluationFunctions.basic_evaluation(board, 0)
    assert isinstance(score, float)
    
    # Test advanced evaluation
    score = EvaluationFunctions.advanced_evaluation(board, 0)
    assert isinstance(score, float)
    
    # Test with different board states
    board.stores[0] = 10
    board.stores[1] = 5
    score = EvaluationFunctions.advanced_evaluation(board, 0)
    assert score > 0  # Should be positive for winning position
    
    board.stores[0] = 5
    board.stores[1] = 10
    score = EvaluationFunctions.advanced_evaluation(board, 0)
    assert score < 0  # Should be negative for losing position

def test_iterative_deepening():
    """Test IterativeDeepeningAI."""
    board = Board()
    ai = IterativeDeepeningAI(
    max_depth=5,
    time_limit=1.0,
    evaluation_func=EvaluationFunctions.basic_evaluation
    )
    
    # Test getting best move
    move, depth = ai.get_best_move(board)
    assert 0 <= move < Board.PITS_PER_PLAYER
    assert 0 < depth <= 5
    
    # Test with no valid moves
    board.pits[board.current_player] = 0
    with pytest.raises(ValueError):
        ai.get_best_move(board)
    
    # Test search statistics
    depth, nodes = ai.get_last_search_stats()
    assert depth > 0
    assert nodes > 0 