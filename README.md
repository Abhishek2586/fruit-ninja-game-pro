# Fruit Ninja Game

A Python implementation of the classic Fruit Ninja game using Pygame. Slice fruits, avoid bombs, and achieve high scores in this engaging arcade game!

## Features

- Multiple game modes (Classic, Arcade, Zen, Tutorial, Challenge)
- Special blade types (Normal, Fire, Ice, Lightning) with unique abilities
- Achievement system with unlockable rewards
- Power-up system (Slow Motion, Double Points, Mega Slice, Freeze)
- Particle effects and smooth animations
- High score system
- Dynamic backgrounds based on score
- Combo system with multipliers

## Requirements

- Python 3.x
- Pygame

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/fruit-ninja-game.git
   cd fruit-ninja-game
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   source .venv/bin/activate  # On Unix/MacOS
   ```

3. Install required packages:
   ```bash
   pip install pygame
   ```

## How to Play

1. Run the game:
   ```bash
   python fruit_ninja.py
   ```

2. Enter your name when prompted
3. Select fruits to include in the game
4. Use your mouse to slice fruits
5. Avoid bombs - they end the game when hit
6. Unlock achievements to get special blades and powers

## Game Controls

- Mouse movement: Control the blade
- Left mouse button: Slice fruits
- R: Restart game (when game over)
- Q: Quit game (when game over)

## Project Structure

```
├── fruit-ninja-game-python-code/
│   ├── images/         # Game images and sprites
│   ├── sounds/        # Game sound effects
│   ├── back.jpg       # Background images
│   ├── back1.jpg
│   └── comic.ttf      # Font file
├── fruit_ninja.py     # Main game file
├── highscores.json    # High scores data
└── README.md         # Project documentation
```

## Features in Detail

### Blade Types
- Normal: Standard slicing
- Fire: Burns nearby fruits for bonus points
- Ice: Slows down fruits
- Lightning: Chain reaction between nearby fruits

### Power-ups
- Slow Motion: Slows down game time
- Double Points: Doubles score for duration
- Mega Slice: Increased slice range
- Freeze: Freezes fruits in place

### Achievements
- Fruit Ninja Master: Score 100 points
- Combo King: Get a 10x combo
- Survivor: Play 5 games
- Perfect Slice: Hit 5 fruits in a row

## Contributing

Feel free to fork the project and submit pull requests with improvements or bug fixes.

## License

This project is open source and available under the MIT License.