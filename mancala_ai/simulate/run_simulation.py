import time
from typing import List, Tuple, Dict
import numpy as np
from mancala_ai.game.board import Board
from mancala_ai.game.rules import GameRules
from mancala_ai.simulate.agents import Agent, get_available_agents

class Simulation:
    """Runs simulations between different agents."""
    
    def __init__(self, num_games: int = 100, max_moves_per_game: int = 200):
        self.num_games = num_games
        self.max_moves_per_game = max_moves_per_game
        self.results: Dict[str, Dict[str, int]] = {}
        
    def run_match(self, agent1: Agent, agent2: Agent, 
                 agent1_name: str, agent2_name: str) -> Tuple[int, int, int]:
        """
        Run a single match between two agents.
        Returns: (agent1_wins, agent2_wins, draws)
        """
        board = Board()
        agent1_wins = 0
        agent2_wins = 0
        draws = 0
        
        for game_num in range(self.num_games):
            board = Board()  # Reset board
            moves_count = 0
            
            while moves_count < self.max_moves_per_game:
                # Validate stone count
                if not board.validate_stone_count():
                    print(f"Warning: Invalid stone count detected in game {game_num}")
                    break
                
                # If current player has no legal moves, end the game
                if not board.get_valid_moves():
                    print(f"Game {game_num}: Player {board.current_player} has no valid moves. Ending game.")
                    is_game_over, winner = GameRules.get_game_result(board)
                    if winner == 0:
                        agent1_wins += 1
                    elif winner == 1:
                        agent2_wins += 1
                    else:
                        draws += 1
                    break

                # Get current agent
                current_agent = agent1 if board.current_player == 0 else agent2
                
                try:
                    # Get move from current agent
                    move = current_agent.get_move(board)
                    
                    # Make move
                    is_valid, gets_extra_turn = GameRules.make_move(board, move)
                    if not is_valid:
                        print(f"Warning: Invalid move detected in game {game_num}")
                        break
                        
                    moves_count += 1
                        
                    # Check if game is over
                    is_game_over, winner = GameRules.get_game_result(board)
                    if is_game_over:
                        if winner == 0:
                            agent1_wins += 1
                        elif winner == 1:
                            agent2_wins += 1
                        else:
                            draws += 1
                        break
                        
                    # Switch player if no extra turn
                    if not gets_extra_turn:
                        board.switch_player()
                        
                except ValueError as e:
                    print(f"Error in game {game_num}: {e}")
                    break
            
            if moves_count >= self.max_moves_per_game:
                print(f"Warning: Game {game_num} exceeded maximum move limit")
                # Count as a draw if we hit the move limit
                draws += 1
                continue  
                    
        return agent1_wins, agent2_wins, draws
    
    def run_tournament(self, agents: List[Tuple[str, Agent]]):
        """Run a tournament between all agents."""
        n = len(agents)
        
        # Initialize results
        for name, _ in agents:
            self.results[name] = {"wins": 0, "losses": 0, "draws": 0}
            
        # Run all pairwise matches
        for i in range(n):
            for j in range(i + 1, n):
                name1, agent1 = agents[i]
                name2, agent2 = agents[j]
                
                print(f"\nRunning match: {name1} vs {name2}")
                wins1, wins2, draws = self.run_match(agent1, agent2, name1, name2)
                
                # Update results
                self.results[name1]["wins"] += wins1
                self.results[name1]["losses"] += wins2
                self.results[name1]["draws"] += draws
                
                self.results[name2]["wins"] += wins2
                self.results[name2]["losses"] += wins1
                self.results[name2]["draws"] += draws
                
    def print_results(self):
        """Print tournament results."""
        print("\nTournament Results:")
        print("-" * 50)
        print(f"{'Agent':<20} {'Wins':<10} {'Losses':<10} {'Draws':<10} {'Win Rate':<10}")
        print("-" * 50)
        
        for name, stats in self.results.items():
            total = stats["wins"] + stats["losses"] + stats["draws"]
            win_rate = stats["wins"] / total if total > 0 else 0
            print(f"{name:<20} {stats['wins']:<10} {stats['losses']:<10} "
                  f"{stats['draws']:<10} {win_rate:.2%}")

def main():
    """Run a tournament between all available agents."""
    # Get available agents
    agent_classes = get_available_agents()
    
    # Create agent instances
    agents = []
    for name, agent_class in agent_classes:
        if name == "Minimax":
            agent = agent_class(depth=3)
        elif name == "IterativeDeepening":
            agent = agent_class(time_limit=2.0)
        else:
            agent = agent_class()
        agents.append((name, agent))
    
    # Run tournament
    sim = Simulation(num_games=50)
    sim.run_tournament(agents)
    sim.print_results()

if __name__ == "__main__":
    main() 