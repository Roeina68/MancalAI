from typing import List, Tuple
import numpy as np

class Board:
    """Represents the Mancala game board state."""
    
    PITS_PER_PLAYER = 6
    INITIAL_STONES = 4
    TOTAL_STONES = PITS_PER_PLAYER * INITIAL_STONES * 2  # Total stones in the game
    
    def __init__(self):
        """Initialize a new Mancala board."""
        # Initialize pits with 4 stones each
        self.pits = np.full((2, self.PITS_PER_PLAYER), self.INITIAL_STONES)
        # Initialize stores (mancalas) with 0 stones
        self.stores = np.zeros(2, dtype=int)
        self.current_player = 0  # 0 for player 1, 1 for player 2
        
    def validate_stone_count(self) -> bool:
        """Validate that the total number of stones is correct."""
        total_stones = (np.sum(self.pits) + np.sum(self.stores))
        return total_stones == self.TOTAL_STONES
        
    def clone(self) -> 'Board':
        """Create a deep copy of the current board state."""
        new_board = Board()
        new_board.pits = self.pits.copy()
        new_board.stores = self.stores.copy()
        new_board.current_player = self.current_player
        return new_board
    
    def get_valid_moves(self) -> List[int]:
        """Get list of valid moves for current player."""
        return [i for i in range(self.PITS_PER_PLAYER) 
                if self.pits[self.current_player][i] > 0]
    
    def apply_move(self, pit_index: int) -> bool:
        """
        Apply a move starting from the specified pit.
        Returns True if the player gets an extra turn.
        """
        if not 0 <= pit_index < self.PITS_PER_PLAYER:
            raise ValueError("Invalid pit index")
            
        if self.pits[self.current_player][pit_index] == 0:
            raise ValueError("Selected pit is empty")
            
        # Get stones from selected pit
        stones = self.pits[self.current_player][pit_index]
        self.pits[self.current_player][pit_index] = 0
        
        # Distribute stones
        current_side = self.current_player
        current_pit = pit_index + 1
        
        while stones > 0:
            # If we're at the end of current side
            if current_pit >= self.PITS_PER_PLAYER:
                # If it's current player's store
                if current_side == self.current_player:
                    self.stores[current_side] += 1
                    stones -= 1
                    if stones == 0:
                        return True  # Extra turn
                current_side = 1 - current_side
                current_pit = 0
                continue
                
            # Place stone in pit
            self.pits[current_side][current_pit] += 1
            stones -= 1
            current_pit += 1
            
        # Check for capture
        if (current_side == self.current_player and 
            current_pit > 0 and 
            self.pits[current_side][current_pit - 1] == 1):
            opposite_pit = self.PITS_PER_PLAYER - current_pit
            if self.pits[1 - current_side][opposite_pit] > 0:
                # Capture stones
                captured = self.pits[1 - current_side][opposite_pit]
                self.pits[1 - current_side][opposite_pit] = 0
                self.pits[current_side][current_pit - 1] = 0
                self.stores[current_side] += captured + 1
                
        return False
    
    def is_game_over(self) -> bool:
        """Game is over when either side has all pits empty."""
        return np.sum(self.pits[0]) == 0 or np.sum(self.pits[1]) == 0

        
    def get_winner(self) -> int:
        """
        Get the winner of the game.
        Returns: 0 for player 1, 1 for player 2, -1 for draw
        """
        if not self.is_game_over():
            return -1
            
        # Add remaining stones to stores
        self.stores[0] += np.sum(self.pits[0])
        self.stores[1] += np.sum(self.pits[1])
        self.pits.fill(0)  # Clear all pits
        
        if self.stores[0] > self.stores[1]:
            return 0
        elif self.stores[1] > self.stores[0]:
            return 1
        return -1
    
    def switch_player(self):
        """Switch the current player."""
        self.current_player = 1 - self.current_player
    
    def get_state(self) -> Tuple[np.ndarray, np.ndarray, int]:
        """Get the current board state as a tuple of (pits, stores, current_player)."""
        return (self.pits.copy(), self.stores.copy(), self.current_player) 
    
    def clone_with_switched_player(self) -> 'Board':
        """Return a clone of the board with current_player switched."""
        new_board = self.clone()
        new_board.switch_player()
        return new_board
