# 🚀 Astral Rush

**Astral Rush** is a fullscreen 2D arcade-style space shooter game built using Python and Pygame. Featuring fast-paced gameplay, dynamic menus, two-player support, and a retro aesthetic, it's an exciting journey through the stars!


## 🎮 Features

- Single-player & two-player modes
- Bullet dodging and shooting mechanics
- Progressive difficulty with increasing levels
- Dynamic enemy spawns and attacks
- Pause menu and settings
- Volume control and mute option
- High score tracking
- Retro-styled pixel assets and music


## 🕹 Controls

### Player 1:
- **Move**: W / A / S / D or Arrow Keys
- **Shoot**: SPACE
- **Pause**: P

### Player 2:
- **Move**: Arrow Keys
- **Shoot**: ENTER
- **Pause**: P


## 📁 Project Structure

```

Astral_Rush/
├── Assets/
│   ├── Audio/
│   │   ├── DEAF KEV - Invincible.mp3
│   │   ├── Explosion.mp3
│   │   └── Laser.mp3
│   ├── Fonts/
│   │   ├── ARCADECLASSIC.TTF
│   │   └── ArcadeAlternate.ttf
│   └── Images/
│       ├── Background.png
│       ├── enemy.png
│       ├── explosion_animation#.png
│       ├── gas.png
│       ├── icon.png
│       ├── laser_blue.png
│       ├── laser_red.png
│       └── player.png
├── Astral_Rush.py
└── highscore.txt

````


## 🛠 Requirements

- Python 3.x
- Pygame (`pip install pygame`)



## 🚀 Running the Game

1. Clone or download the repository.
2. Ensure all dependencies and asset files are in place.
3. Run the game:

```bash
python Astral_Rush.py
````

**Note**: The game runs in fullscreen mode by default.


## 🧠 How It Works

* The main game loop handles events, updates game state, and renders the screen at 60 FPS.
* Different menus are drawn conditionally (main, settings, volume, controls).
* Enemy and player interactions include shooting, hit detection, and explosion animations.
* Two-player mode allows real-time PvP shooting.


## 🎵 Credits

* Music: *"Invincible"* by DEAF KEV via NCS
* Fonts: ARCADECLASSIC, ArcadeAlternate
* Assets: Custom and retro-style graphics


## 📝 License

This game is provided for educational and entertainment purposes. Be sure to replace or properly license the music and font assets if you intend to distribute the game publicly.


Enjoy the rush! 🌌
