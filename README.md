# 🕹️ Ultimate Pokémon RPG Adventure

A full-featured Pokémon-style RPG game built with Python and Pygame, supporting sprite-based map navigation, 1v1 and 3v3 tactical battles, animated skills, sound, dynamic popups, and rich player statistics tracking and visualization.

---

## 🛠️ Installation

1. **Clone the repository**  
```bash
git clone https://github.com/karnponpoochitkanon/Pokemon-game.git
cd Pokemon-game
```

2. **Install dependencies**  
```bash
pip3 install pygame
pip3 install pandas
pip3 install matplotlib
pip3 install seaborn
> Note: `os` is a built-in module in Python, so no need to install it separately.
```

3. **Run the game**  
```bash
python3 main.py
```

---

## 🎮 Controls

### 🌍 Global
- `Arrow Keys` → Move / Navigate
- `Enter` → Confirm / Attack / Select
- `Esc` → Cancel popup
- `1` → Run from battle / cancel selection
- `Shift (L/R)` → View Pokémon team

### ✅ Start Menu
- `Click` input → Type name (max 10 chars)
- `Enter` → Confirm name

### 👤 Character Selection
- `Up / Down` → Navigate characters
- `Enter` → Select

### 🗺️ On Map
- `Arrow Keys` → Move
- `Shift` → View team popup
- `A` → Show debug grass zones

### ⚔️ Wild Battle (1v1)
- `Space` → Attack
- `1` → Run

### ⚔️ Final Boss Battle (3v3)
- `Space` → Select/unselect Pokémon (max 3)
- `Left / Right` → Choose enemy
- `Enter` → Attack
- `1` → Cancel and return

---

## 🔊 Sound

- `overworld.ogg` – background map music  
- `battle.ogg` – battle music for 1v1 and 3v3

---

## 📊 Data Logging

All data is saved in `game_stats.csv`:

- Player name
- Time played (seconds)
- Final boss battles
- Distance walked
- Total Pokémon
- Heal tree usage
- Character chosen

---

## 📈 Visualization GUI

Run the GUI via:

```bash
python3 GUI.py
```

Includes graphs and summary stats such as:

- Distance histogram
- Playtime chart
- Character selection pie chart
- Pokémon team count
- Heal usage
- Final boss battle stats
- Summary table

---

## 🖼️ Screenshots

- Gameplay: `/screenshots/gameplay/`  
- Graphs: `/screenshots/visualization/`

---

## 🎥 Demo

[Watch the Game Demo on YouTube](https://youtu.be/0PVEW_bYXD8)

---

Let the journey begin! 🚀

⚔️ In the 3v3 Final Boss Battle, if players press keys too rapidly (especially Enter to attack), the game may crash due to an IndexError.
This is related to a rare timing issue with the internal turn counter.
