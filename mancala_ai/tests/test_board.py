import pytest
import numpy as np
from mancala_ai.game.board import Board
from mancala_ai.game.rules import GameRules

def test_board_initialization():
    """Test board initialization."""
    board = Board()
    assert board.pits.shape == (2, Board.PITS_PER_PLAYER)
    assert np.all(board.pits == Board.INITIAL_STONES)
    assert np.all(board.stores == 0)
    assert board.current_player == 0

def test_board_clone():
    """Test board cloning."""
    board = Board()
    board_copy = board.clone()
    
    # Test that it's a deep copy
    assert board_copy is not board
    assert board_copy.pits is not board.pits
    assert board_copy.stores is not board.stores
    
    # Test that values are copied correctly
    assert np.array_equal(board_copy.pits, board.pits)
    assert np.array_equal(board_copy.stores, board.stores)
    assert board_copy.current_player == board.current_player

def test_valid_moves():
    """Test getting valid moves."""
    board = Board()
    valid_moves = board.get_valid_moves()
    assert len(valid_moves) == Board.PITS_PER_PLAYER
    assert all(0 <= move < Board.PITS_PER_PLAYER for move in valid_moves)
    
    # Test with empty pits
    board.pits[0] = 0
    valid_moves = board.get_valid_moves()
    assert len(valid_moves) == 0

def test_apply_move():
    """Test applying moves."""
    board = Board()
    
    # Test valid move
    initial_stones = board.pits[0][0]
    gets_extra_turn = board.apply_move(0)
    assert board.pits[0][0] == 0
    
    # Test invalid move
    with pytest.raises(ValueError):
        board.apply_move(-1)
    with pytest.raises(ValueError):
        board.apply_move(Board.PITS_PER_PLAYER)
    with pytest.raises(ValueError):
        board.apply_move(0)  # Empty pit

def test_game_over():
    """Test game over conditions."""
    board = Board()
    assert not board.is_game_over()
    
    # Empty one side
    board.pits[0] = 0
    assert board.is_game_over()
    
    # Test winner determination
    board.pits[0] = 0
    board.pits[1] = 0
    board.stores[0] = 10
    board.stores[1] = 5
    assert board.get_winner() == 0
    
    board.stores[0] = 5
    board.stores[1] = 10
    assert board.get_winner() == 1
    
    board.stores[0] = 10
    board.stores[1] = 10
    assert board.get_winner() == -1  # Draw 