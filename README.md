# 🎮 Bouncy Maze 2D

**Bouncy Maze 2D** is a lightweight arcade-style 2D platformer developed using **Python and OpenGL**, where players control a bouncing ball to navigate through tricky mazes, avoid enemies, and collect treasures. All visuals are rendered using only `GL_POINTS` for a pixelated retro aesthetic.

---

## 🚀 Gameplay Overview

- Navigate a **bouncy ball** through 2 maze levels.
- **Avoid enemies**, traps, and moving obstacles.
- Collect **hidden treasures** for bonus interaction.
- Use **jump physics** and precise timing to cross challenges.
- Game status (score, health, pause, game over) is displayed via the **terminal**, not in-game UI.

---

## 🎮 Controls

| Action            | Key/Button         |
|-------------------|--------------------|
| Move Left         | `A` key            |
| Move Right        | `D` key            |
| Jump (Double Jump)| `Space`            |
| Pause/Resume      | Top-center click   |
| Restart Game      | Top-left click     |
| Exit Game         | Top-right click    |

---

## 🧱 Features

- 🔘 Only uses **`GL_POINTS`** for all drawing (ball, walls, UI, etc.).
- 💥 Collision detection with **obstacles, enemies, and lasers**.
- 🧠 Basic **physics simulation** with gravity and jump mechanics.
- 🛑 **Laser traps** with animated vertical motion.
- 💎 **Treasure collectibles** to pause traps and reset laser timers.
- ❤️ Life system: 3 lives per game, shown using symbols.
- 🖱️ Mouse-based game controls.
- 🧪 Game state feedback via **terminal logs** (score, pause, game over).

---

## 🖼️ Screenshots

> You can add screenshots here using:
> ```markdown
> ![Gameplay](screenshots/gameplay.png)
> ```

---

## 📦 Requirements

- Python 3.x
- OpenGL bindings for Python:
  ```bash
  pip install PyOpenGL PyOpenGL_accelerate
