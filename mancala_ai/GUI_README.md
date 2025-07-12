# Mancala GUI

A graphical user interface for the Mancala game with AI opponent.

## Features

- **Visual Board**: Clear representation of the Mancala board with numbered pits
- **AI Opponent**: Play against a Minimax AI with configurable depth
- **Game Log**: Real-time logging of all moves and game events
- **Score Display**: Live score tracking for both players
- **Turn Indicators**: Clear indication of whose turn it is
- **Game Over Detection**: Automatic detection and display of game results
- **New Game**: Easy restart functionality
- **Input Validation**: Prevents invalid moves

## How to Play

1. **Setup**: You are Player 1 (bottom row), the AI is Player 2 (top row)
2. **Objective**: Collect more stones in your store than your opponent
3. **Moves**: Click on any pit in your row (bottom row) that contains stones
4. **Distribution**: Stones are distributed counter-clockwise, one per pit
5. **Extra Turns**: If your last stone lands in your store, you get another turn
6. **Captures**: If your last stone lands in an empty pit on your side, you capture stones from the opposite pit
7. **Game End**: Game ends when one player has no stones left in their pits

## Running the GUI

```bash
# From the mancala_ai directory
python gui.py
```

## Testing

Before running the GUI, you can test that all components work correctly:

```bash
python test_gui_components.py
```

## GUI Layout

- **Top Row**: AI pits (read-only display)
- **Bottom Row**: Player pits (clickable buttons)
- **Left Store**: Player's store (green)
- **Right Store**: AI's store (blue)
- **Game Log**: Scrollable text area showing move history
- **Controls**: New Game button and turn/score indicators

## Technical Details

- **AI Algorithm**: Minimax with Alpha-Beta pruning
- **AI Depth**: Configurable (default: 3)
- **Evaluation**: Basic evaluation function considering store difference and available stones
- **Threading**: AI moves are executed asynchronously to prevent GUI freezing

## Troubleshooting

If you encounter issues:

1. **Import Errors**: Make sure you're running from the `mancala_ai` directory
2. **GUI Not Responding**: The AI might be thinking - wait a moment
3. **Invalid Moves**: Empty pits are automatically disabled
4. **Game Crashes**: Check the console for error messages

## Customization

You can modify the AI behavior by changing:
- `max_depth` in the `MinimaxAI` constructor
- Evaluation function in `ai/evaluation.py`
- Board layout in the `build_board()` method 