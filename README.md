# Click Game Ver.1.0.0

[日本語版README](README-ja.md)

A fast-paced clicking game built with Python and Pygame. Test your reflexes by clicking on randomly appearing targets within the time limit!

## 🎮 Features

- **Multiple Difficulty Levels**
  - Easy: 3×3 grid
  - Normal: 6×6 grid  
  - Hard: 9×9 grid

- **Customizable Time Limits**
  - 10 seconds
  - 20 seconds
  - 30 seconds

- **High Score System**
  - Individual records for each difficulty/time combination
  - Persistent storage using JSON
  - New high score notifications

- **Enhanced Visual Effects**
  - Gradient backgrounds
  - Pulsing target animations
  - Shadow effects on buttons
  - Professional UI design

## 🚀 Getting Started

### Prerequisites

- Python 3.6 or higher
- Pygame library

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/click-game.git
cd click-game
```

2. Install required dependencies:
```bash
pip install pygame
```

### Running the Game

```bash
python click_game.py
```

## 🎯 How to Play

1. **Start the Game**: Click "START GAME" from the main menu
2. **Select Difficulty**: Choose from Easy (3×3), Normal (6×6), or Hard (9×9)
3. **Select Time**: Choose your preferred time limit (10s, 20s, or 30s)
4. **Play**: Click on the black/red pulsing squares as quickly as possible
5. **Score**: Earn points for each correct click
6. **Restart**: Press 'R' to restart or 'ESC' to return to menu

## 🏆 Scoring System

- **1 point** per correct click
- **High scores** are saved automatically
- **New records** are highlighted when achieved
- **Individual leaderboards** for each difficulty/time combination

## 🎨 Game Modes

### Difficulty Levels
- **Easy (3×3)**: Perfect for beginners, larger targets
- **Normal (6×6)**: Balanced challenge for regular players
- **Hard (9×9)**: Ultimate test for expert players

### Time Challenges
- **10 seconds**: Quick reflexes test
- **20 seconds**: Balanced gameplay
- **30 seconds**: Endurance challenge

## 📁 Project Structure

```
click-game/
│
├── click_game.py          # Main game file
├── high_scores.json       # High scores storage (auto-generated)
├── README.md             # This file
└── screenshot.png        # Game screenshot
```

## 🛠️ Technical Details

- **Language**: Python 3
- **Framework**: Pygame
- **Data Storage**: JSON for high scores
- **Resolution**: 800x600 pixels
- **FPS**: 60 frames per second

## 🎵 Controls

- **Mouse**: Click on targets and navigate menus
- **R Key**: Restart game (during game over screen)
- **ESC Key**: Return to main menu (during game over screen)

## 🔧 Development

### Code Structure

The game follows an object-oriented design with the main `ClickGame` class handling:
- Game state management
- UI rendering
- Event handling
- Score tracking
- High score persistence

### Key Components

- **State Management**: Title screen, difficulty selection, gameplay, game over
- **Dynamic Grid System**: Adjustable grid sizes for different difficulties
- **Animation System**: Pulsing effects and visual feedback
- **Data Persistence**: JSON-based high score storage

## 🚀 Future Enhancements

Potential features for future versions:
- Sound effects and background music
- Combo system for consecutive hits
- Power-ups and special effects
- Multiplayer support
- Online leaderboards
- Custom themes and colors

## 🙏 Acknowledgments

- Built with [Pygame](https://www.pygame.org/)
- Inspired by classic reaction time games
- Thanks to the Python gaming community

---

**Enjoy the game and challenge your friends to beat your high scores!** 🎯
