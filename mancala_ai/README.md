# Mancala AI

A Python implementation of the Mancala board game with an AI opponent using the Minimax algorithm with Alpha-Beta pruning.

## Features

- Complete Mancala game implementation
- AI opponent using Minimax with Alpha-Beta pruning
- Multiple evaluation strategies
- Simulation framework for testing different AI agents
- Comprehensive test suite

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

To play against the AI:
```bash
python main.py
```

To run simulations:
```bash
python simulate/run_simulation.py
```

To run tests:
```bash
pytest tests/
```

## Project Structure

- `game/`: Core game logic and board representation
- `ai/`: AI implementation with Minimax and evaluation functions
- `tests/`: Unit tests
- `simulate/`: Simulation framework for testing AI agents

## Requirements

- Python 3.9+
- See requirements.txt for dependencies 