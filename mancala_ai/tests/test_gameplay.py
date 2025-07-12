import pytest
import numpy as np
from mancala_ai.game.board import Board
from mancala_ai.game.rules import GameRules
from mancala_ai.simulate.agents import RandomAgent, GreedyAgent, MinimaxAgent

def test_random_agent():
    """Test random agent behavior."""
    board = Board()
    agent = RandomAgent()
    
    # Test multiple moves
    for _ in range(10):
        move = agent.get_move(board)
        assert 0 <= move < Board.PITS_PER_PLAYER
        assert board.pits[board.current_player][move] > 0
        
        # Make move
        is_valid, _ = GameRules.make_move(board, move)
        assert is_valid
        
        # Switch player
        board.switch_player()
    
    # Test with no valid moves
    board.pits[board.current_player] = 0
    with pytest.raises(ValueError):
        agent.get_move(board)

def test_greedy_agent():
    """Test greedy agent behavior."""
    board = Board()
    agent = GreedyAgent()
    
    # Test multiple moves
    for _ in range(10):
        move = agent.get_move(board)
        assert 0 <= move < Board.PITS_PER_PLAYER
        assert board.pits[board.current_player][move] > 0
        
        # Make move
        is_valid, _ = GameRules.make_move(board, move)
        assert is_valid
        
        # Switch player
        board.switch_player()
    
    # Test with no valid moves
    board.pits[board.current_player] = 0
    with pytest.raises(ValueError):
        agent.get_move(board)

def test_minimax_agent():
    """Test minimax agent behavior."""
    board = Board()
    agent = MinimaxAgent(depth=2)
    
    # Test multiple moves
    for _ in range(5):  # Fewer moves due to computational cost
        move = agent.get_move(board)
        assert 0 <= move < Board.PITS_PER_PLAYER
        assert board.pits[board.current_player][move] > 0
        
        # Make move
        is_valid, _ = GameRules.make_move(board, move)
        assert is_valid
        
        # Switch player
        board.switch_player()
    
    # Test with no valid moves
    board.pits[board.current_player] = 0
    with pytest.raises(ValueError):
        agent.get_move(board)

def test_game_rules():
    """Test game rules and move validation."""
    board = Board()
    
    # Test valid moves
    for i in range(Board.PITS_PER_PLAYER):
        assert GameRules.is_valid_move(board, i)
    
    # Test invalid moves
    assert not GameRules.is_valid_move(board, -1)
    assert not GameRules.is_valid_move(board, Board.PITS_PER_PLAYER)
    
    # Test empty pit
    board.pits[board.current_player][0] = 0
    assert not GameRules.is_valid_move(board, 0)
    
    # Test move application
    board.pits[board.current_player][0] = 4
    move = 0
    is_valid, gets_extra_turn = GameRules.make_move(board, move)
    assert is_valid
    assert board.pits[board.current_player][move] == 0
    
    # Test game result
    is_game_over, winner = GameRules.get_game_result(board)
    assert not is_game_over
    assert winner == -1
    
    # Test score
    score = GameRules.get_score(board)
    assert len(score) == 2
    assert all(isinstance(s, (int, np.integer)) for s in score)
    
    # Test available stones
    stones = GameRules.get_available_stones(board)
    assert len(stones) == 2
    assert all(isinstance(s, (int, np.integer)) for s in stones)
