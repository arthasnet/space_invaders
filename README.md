# Space Invaders

![Space Invaders](https://img.shields.io/badge/Game-Space%20Invaders-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.6.1-red)

A classic Space Invaders arcade game clone implemented in Python using the Pygame library. Defend Earth from waves of invading aliens!

## Game Description

Space Invaders is a classic arcade game where you control a spaceship at the bottom of the screen and shoot at alien invaders moving down from the top. Your mission is to destroy all aliens before they reach the bottom of the screen or collide with your ship.

### Features

- Classic Space Invaders gameplay
- Different types of enemies with unique visual designs
- Player spaceship with shooting capabilities
- Visual effects (animated enemies, projectile trails, hit flashes)
- Sound effects for shooting, explosions, and game events
- High score tracking system
- Start screen with instructions
- Game over screen with score display
- Volume control

## Installation

1. Ensure you have Python 3.11 or newer installed on your system.
2. Install the Pygame library using pip:
   ```
   pip install pygame
   ```
3. Clone or download this repository:
   ```
   git clone <repository-url>
   ```
   or download and extract the ZIP file.
4. Navigate to the game directory:
   ```
   cd space_invaders
   ```
5. Run the game:
   ```
   python main.py
   ```

## How to Play

### Controls

- **Left/Right Arrow Keys**: Move your spaceship left or right
- **Space Bar**: Shoot
- **Escape**: Exit the game
- **+/- Keys**: Increase/decrease volume
- **R Key**: Restart the game after game over

### Objective

- Destroy all alien invaders before they reach the bottom of the screen
- Avoid getting hit by enemy projectiles
- Achieve the highest score possible

## Requirements

- Python 3.11 or newer
- Pygame 2.6.1 or newer

## Game Features and Mechanics

### Player Ship
- Triangular ship design with engine glow
- Moves left and right at bottom of screen
- Shoots green laser projectiles upward
- Has limited lives (3 by default)
- Visual flash effect when hit

### Enemies
- Three different types with unique designs based on row:
  - Top row: UFO-style enemies (red)
  - Middle rows: Crab-like enemies (blue)
  - Bottom rows: Octopus-like enemies (green)
- Move in formation side-to-side and downward
- Flash white before shooting
- Increase difficulty as game progresses

### Projectiles
- Player projectiles: Green laser beams with trailing effect
- Enemy projectiles: Red-orange plasma balls with rotation effect

### Scoring
- Each destroyed enemy awards points
- High score is saved between game sessions
- Score displayed during gameplay and on game over screen

### Game States
- Start Screen: Shows instructions and high score
- Gameplay: Main game action
- Game Over: Shows final score and high score

## Project Structure

- `main.py`: Main game loop and overall control
- `constants.py`: Game constants and configuration
- `player.py`: Player spaceship implementation
- `enemy.py`: Enemy aliens implementation
- `projectile.py`: Projectile system implementation
- `assets/`: Directory for game resources (created at runtime)
- `highscore.json`: High score storage file (created at runtime)

## Credits and Acknowledgments

This game was created as a Python learning project and is based on the classic Space Invaders arcade game originally developed by Tomohiro Nishikado and released in 1978 by Taito.

Special thanks to:
- Pygame development team for creating an easy-to-use game development library
- The original Space Invaders game for inspiration
- [Insert your name/team members here]

## License

This project is released under the MIT License - see the LICENSE file for details.

## Future Improvements

Potential features for future versions:
- Additional enemy types
- Power-ups and special weapons
- Multiple levels with increasing difficulty
- Background music
- Animated backgrounds
- Shields or barriers for player protection
- Mobile/touch screen support

