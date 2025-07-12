import sys
from mancala_ai.game.board import Board
from mancala_ai.game.rules import GameRules
from mancala_ai.ai.minimax import MinimaxAI
from mancala_ai.ai.evaluation import EvaluationFunctions

def print_board(board: Board):
    """Print the current board state."""
    # Print opponent's pits
    print("\nOpponent's pits:")
    print("  ", end="")
    for i in range(Board.PITS_PER_PLAYER - 1, -1, -1):
        print(f"{board.pits[1][i]:2d} ", end="")
    print(f"\n{board.stores[1]:2d} {'  ' * Board.PITS_PER_PLAYER} {board.stores[0]:2d}")
    print("  ", end="")
    for i in range(Board.PITS_PER_PLAYER):
        print(f"{board.pits[0][i]:2d} ", end="")
    print("\nYour pits:")

def get_human_move(board: Board) -> int:
    """Get move from human player."""
    while True:
        try:
            move = int(input("Enter pit number (0-5): "))
            if not GameRules.is_valid_move(board, move):
                print("Invalid move. Try again.")
                continue
            return move
        except ValueError:
            print("Please enter a number between 0 and 5.")

def main():
    """Run the main game loop."""
    print("Welcome to Mancala!")
    print("You are Player 1 (bottom row)")
    
    # Initialize game
    board = Board()
    ai = MinimaxAI(max_depth=3)
    
    while True:
        print_board(board)
        
        # Check if game is over
        is_game_over, winner = GameRules.get_game_result(board)
        if is_game_over:
            if winner == 0:
                print("You win!")
            elif winner == 1:
                print("AI wins!")
            else:
                print("It's a draw!")
            break
            
        if board.current_player == 0:
            # Human's turn
            move = get_human_move(board)
        else:
            # AI's turn
            print("\nAI is thinking...")
            move = ai.get_best_move(board)
            print(f"AI chooses pit {move}")
            
        # Make move
        is_valid, gets_extra_turn = GameRules.make_move(board, move)
        if not is_valid:
            print("Invalid move!")
            continue
            
        # Switch player if no extra turn
        if not gets_extra_turn:
            board.switch_player()
            
        print("\n" + "=" * 30)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame terminated by user.")
        sys.exit(0) 