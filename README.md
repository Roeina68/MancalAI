# Mancala AI

A Python implementation of the Mancala board game with an AI opponent using the Minimax algorithm with Alpha-Beta pruning.

## Features

- Complete Mancala game implementation
- AI opponent using Minimax with Alpha-Beta pruning
- Multiple evaluation strategies
- Simulation framework for testing different AI agents
- Comprehensive test suite
- Playable via terminal or graphical interface (GUI)

## Installation

1. Clone the repository
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Play Against the AI

#### Terminal Mode (default)
To play in the terminal:
```bash
python -m mancala_ai.main
```

#### GUI Mode
To play with the graphical interface:
```bash
python -m mancala_ai.main --gui
# or
python -m mancala_ai.main -g
```

#### Help
To see all available options:
```bash
python -m mancala_ai.main --help
```

### Default Parameters

- **AI Agent:** The default AI is `MinimaxAI` with a search depth of 3.
- **Evaluation Function:** The default evaluation function is `advanced_evaluation`, which considers:
  - Store and pit stone differences
  - Stone positions (closer to store is better)
  - Capture (steal) opportunities
  - Extra turn opportunities
  - Empty pits and vulnerability to steals
  - Penalty and blocking rules

### Run Simulations

To run AI-vs-AI simulations:
```bash
python -m mancala_ai.simulate.run_simulation
```

### Run Tests

To run the test suite:
```bash
pytest mancala_ai/tests/
```

## Project Structure

- `game/`: Core game logic and board representation
- `ai/`: AI implementation with Minimax and evaluation functions
- `tests/`: Unit tests
- `simulate/`: Simulation framework for testing AI agents

## Requirements

- Python 3.9+
- See requirements.txt for dependencies 