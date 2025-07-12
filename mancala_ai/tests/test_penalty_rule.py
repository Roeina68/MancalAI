import unittest
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from mancala_ai.game.board import Board
from mancala_ai.game.rules import GameRules

class TestPenaltyRule(unittest.TestCase):
    
    def setUp(self):
        """Set up a fresh board for each test."""
        self.board = Board()
    
    def test_penalty_rule_triggered(self):
        """Test that penalty rule is triggered when store equals closest pit."""
        # Set up a scenario where player 0's store has 5 stones and closest pit has 5 stones
        self.board.stores[0] = 5
        self.board.pits[0][5] = 5  # Closest pit (last pit on player's side)
        
        # Apply penalty rule
        penalty_applied = GameRules.apply_penalty_rule(self.board)
        
        # Check that penalty was applied
        self.assertTrue(penalty_applied)
        self.assertEqual(self.board.stores[0], 4)  # Store should have 4 stones
        self.assertEqual(self.board.pits[0][5], 6)  # Closest pit should have 6 stones
    
    def test_penalty_rule_not_triggered_different_numbers(self):
        """Test that penalty rule is not triggered when numbers are different."""
        # Set up a scenario where store has 5 stones but closest pit has 4 stones
        self.board.stores[0] = 5
        self.board.pits[0][5] = 4
        
        # Apply penalty rule
        penalty_applied = GameRules.apply_penalty_rule(self.board)
        
        # Check that penalty was not applied
        self.assertFalse(penalty_applied)
        self.assertEqual(self.board.stores[0], 5)  # Store should still have 5 stones
        self.assertEqual(self.board.pits[0][5], 4)  # Closest pit should still have 4 stones
    
    def test_penalty_rule_not_triggered_zero_stones(self):
        """Test that penalty rule is not triggered when both are zero."""
        # Set up a scenario where both store and closest pit have 0 stones
        self.board.stores[0] = 0
        self.board.pits[0][5] = 0
        
        # Apply penalty rule
        penalty_applied = GameRules.apply_penalty_rule(self.board)
        
        # Check that penalty was not applied
        self.assertFalse(penalty_applied)
        self.assertEqual(self.board.stores[0], 0)
        self.assertEqual(self.board.pits[0][5], 0)
    
    def test_penalty_rule_for_player_1(self):
        """Test penalty rule works for player 1 (AI)."""
        # Switch to player 1
        self.board.current_player = 1
        
        # Set up a scenario where player 1's store has 3 stones and closest pit has 3 stones
        self.board.stores[1] = 3
        self.board.pits[1][5] = 3
        
        # Apply penalty rule
        penalty_applied = GameRules.apply_penalty_rule(self.board)
        
        # Check that penalty was applied
        self.assertTrue(penalty_applied)
        self.assertEqual(self.board.stores[1], 2)  # Store should have 2 stones
        self.assertEqual(self.board.pits[1][5], 4)  # Closest pit should have 4 stones
    
    def test_penalty_rule_only_affects_current_player(self):
        """Test that penalty rule only affects the current player's side."""
        # Set up both players with equal store and closest pit
        self.board.stores[0] = 5
        self.board.pits[0][5] = 5
        self.board.stores[1] = 3
        self.board.pits[1][5] = 3
        
        # Current player is 0, so only player 0 should be affected
        penalty_applied = GameRules.apply_penalty_rule(self.board)
        
        # Check that penalty was applied only to player 0
        self.assertTrue(penalty_applied)
        self.assertEqual(self.board.stores[0], 4)  # Player 0 store affected
        self.assertEqual(self.board.pits[0][5], 6)  # Player 0 closest pit affected
        self.assertEqual(self.board.stores[1], 3)  # Player 1 store unchanged
        self.assertEqual(self.board.pits[1][5], 3)  # Player 1 closest pit unchanged

if __name__ == '__main__':
    unittest.main() 