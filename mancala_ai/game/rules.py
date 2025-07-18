from typing import List, Tuple
import numpy as np
from mancala_ai.game.board import Board

class GameRules:
    """Contains the core game rules and validation logic."""
    
    @staticmethod
    def is_valid_move(board: Board, pit_index: int) -> bool:
        """Check if a move is valid."""
        if not 0 <= pit_index < Board.PITS_PER_PLAYER:
            return False
        
        # Check if the pit is blocked
        if board.blocked_pits[board.current_player] == pit_index:
            return False
            
        return board.pits[board.current_player][pit_index] > 0
    
    @staticmethod
    def get_legal_moves(board: Board) -> List[int]:
        """Get all legal moves for the current player."""
        return [i for i in range(Board.PITS_PER_PLAYER) 
                if GameRules.is_valid_move(board, i)]

    @staticmethod
    def make_move(board: Board, pit_index: int) -> Tuple[bool, bool]:
        """
        Make a move starting from the specified pit.
        Returns (is_valid, gets_extra_turn).
        """
        if not GameRules.is_valid_move(board, pit_index):
            return False, False

        # Get stones from selected pit
        stones = board.pits[board.current_player][pit_index]
        board.pits[board.current_player][pit_index] = 0

        current_side = board.current_player
        current_pit = pit_index + 1
        last_pit = None
        last_side = None

        while stones > 0:
            if current_pit >= board.PITS_PER_PLAYER:
                if current_side == board.current_player:
                    board.stores[current_side] += 1
                    stones -= 1
                    if stones == 0:
                        return True, True
                current_side = 1 - current_side
                current_pit = 0
                continue

            board.pits[current_side][current_pit] += 1
            stones -= 1
            last_pit = current_pit
            last_side = current_side
            current_pit += 1

        # Check for capture
        if (last_side == board.current_player and
                last_pit is not None and
                board.pits[last_side][last_pit] == 1):
            opposite_pit = Board.PITS_PER_PLAYER - 1 - last_pit
            if board.pits[1 - last_side][opposite_pit] > 0:
                # Capture stones from opposite pit
                captured = board.pits[1 - last_side][opposite_pit]
                board.pits[1 - last_side][opposite_pit] = 0
                # Remove the capturing stone (and count it)
                board.pits[last_side][last_pit] = 0
                # Add both captured stones and the capturing stone
                board.stores[last_side] += captured + 1
        return True, False

    @staticmethod
    def get_game_result(board: Board) -> Tuple[bool, int]:
        """
        Get the game result.
        Returns: (is_game_over, winner)
        where winner is 0 for player 1, 1 for player 2, -1 for draw
        """
        # מקרה 1: כל צד ריק
        no_stones = np.sum(board.pits[0]) == 0 or np.sum(board.pits[1]) == 0
        
        # מקרה 2: אין מהלכים חוקיים לאף צד
        no_legal_moves = (
            len(GameRules.get_legal_moves(board)) == 0 and
            len(GameRules.get_legal_moves(board.clone_with_switched_player())) == 0
        )

        if not (no_stones or no_legal_moves):
            return False, -1

        # איסוף אבנים
        board.stores[0] += np.sum(board.pits[0])
        board.stores[1] += np.sum(board.pits[1])
        board.pits.fill(0)

        if board.stores[0] > board.stores[1]:
            return True, 0
        elif board.stores[1] > board.stores[0]:
            return True, 1
        return True, -1

    
    @staticmethod
    def get_score(board: Board) -> Tuple[int, int]:
        """Get the current score for both players."""
        return (board.stores[0], board.stores[1])
    
    @staticmethod
    def get_available_stones(board: Board) -> Tuple[int, int]:
        """Get the number of stones available to each player."""
        return (np.sum(board.pits[0]), np.sum(board.pits[1])) 
    
    @staticmethod
    def apply_penalty_rule(board: Board) -> bool:
        """
        Apply the penalty redistribution rule.
        
        If the number of stones in the player's store equals the number of stones
        in their closest pit (last pit on their side), remove 1 stone from the store
        and add it to that closest pit.
        
        Returns True if the penalty was applied, False otherwise.
        """
        current_player = board.current_player
        store_count = board.stores[current_player]
        closest_pit_index = Board.PITS_PER_PLAYER - 1  # Last pit on the player's side
        closest_pit_count = board.pits[current_player][closest_pit_index]
        
        # Check if the penalty condition is met
        if store_count == closest_pit_count and store_count > 0:
            # Apply penalty: remove 1 from store, add 1 to closest pit
            board.stores[current_player] -= 1
            board.pits[current_player][closest_pit_index] += 1
            return True
        
        return False

    @staticmethod
    def handle_blocking_after_move(board: Board, player: int) -> bool:
        """
        Handle blocking logic after a player's move.
        Returns True if a block was applied, False otherwise.
        """
        # Clear any existing block for the current player
        board.clear_block(player)
        
        # Check if the player can and should block
        if not board.can_block(player):
            return False
        
        # Get blockable pits
        blockable_pits = board.get_blockable_pits(player)
        if not blockable_pits:
            return False
        
        # For AI, automatically choose the best pit to block
        # For human players, this will be handled by the GUI
        if player == 1:  # AI player
            # Advanced strategy: consider multiple factors
            best_pit = None
            best_score = -1
            
            for pit in blockable_pits:
                score = 0
                opponent_stones = board.pits[1 - player][pit]
                
                # Base score: more stones = better block
                score += opponent_stones * 2.0
                
                # Bonus for blocking pits that could lead to steals
                # Check if this pit could be used for stealing from AI
                ai_opposite_pit = Board.PITS_PER_PLAYER - 1 - pit
                if board.pits[player][ai_opposite_pit] == 0:
                    score += opponent_stones * 1.5  # Extra bonus for preventing steals
                
                # Bonus for blocking pits that could lead to extra turns
                # (pits closer to opponent's store)
                position_bonus = (pit + 1) / Board.PITS_PER_PLAYER
                score += opponent_stones * position_bonus
                
                if score > best_score:
                    best_score = score
                    best_pit = pit
            
            if best_pit is not None:
                return board.apply_block(player, best_pit)
        
        return False  # Human player blocking will be handled by GUI