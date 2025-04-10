<p align="center">
  <img src="Pokémon_Trading_Card_Game_logo.svg.png" alt="Pokemon TCG Logo" width="400"/>
</p>

# 🃏 Python Pokémon TCG (Trading Card Game)

Welcome to a fully interactive simulation of the **Pokémon Trading Card Game (TCG)** built entirely in **Python**! This project brings the core mechanics of the classic card game to your terminal, with player-vs-player logic, deck building, energy attachments, evolution, trainer cards, and combat turns.

---

## 🎮 What is Pokémon TCG?

The **Pokémon Trading Card Game (TCG)** is a turn-based card game where players assume the role of Pokémon Trainers. Each player builds a 60-card deck containing:

- **Basic Pokémon** to start battles
- **Stage 1 & Stage 2 Pokémon** to evolve them
- **Energy Cards** to power up attacks
- **Trainer Cards** to use one-time effects (draw, heal, etc.)

The goal is to **knock out your opponent’s Pokémon** and collect all 6 **Prize Cards** to win!

---

## 🔥 Features Implemented

### 🧠 Core Gameplay

- ✅ 60-card randomized decks per player  
- ✅ Draws a 5-card hand from shuffled deck  
- ✅ Choose 1 Active Pokémon + up to 3 Bench Pokémon  
- ✅ Draw 6 Prize Cards  
- ✅ Turn-based battle system

---

### ⚔️ Battle Logic

- 🎯 Attack system with energy requirements
- 🧮 Dynamic HP + damage tracking
- 💀 Knockout detection + Prize card rewards
- 🔁 Automatic promotion of Benched Pokémon on KO

---

### 🔋 Energy Mechanics

- 🔥 Fire, 💧 Water, and 🌿 Grass energy types
- 🛠️ Custom energy cost logic
- 🎯 Attack only when energy requirements are met
- 🎒 Attach one energy per turn

---

### 🧬 Evolution System

- 🧚‍♀️ Stage 1 and Stage 2 Pokémon
- 🔄 Evolves from correct lower stage only
- 🔒 Cannot evolve from the wrong Pokémon or stage
- ✅ Inherits HP and energy from previous evolution

---

### 💼 Trainer Cards (NEW!)

- 🧙‍♂️ Playable Trainer cards with randomized effects:
  - 🃏 Draw 2 cards  
  - 💊 Heal 20 damage from Active Pokémon  
  - 🔄 Discard and redraw entire hand (draw 5)  
- ⚠️ Cannot place Trainer cards as Active or Benched Pokémon  
- ✅ Played directly from hand with immediate effect

---

### 👟 Retreat Mechanic

- 🔄 Swap Active Pokémon with one from Bench
- 🎒 Energy cost system can be added (planned)
- ♻️ Preserves energy and damage

---

## 🗂️ Project Structure

```
pokemon_tcg_game/
│
├── main.py                  # Game launcher, deck setup
├── game.py                  # Core game logic and turn system
├── player.py                # Player class: hand, bench, active, prize logic
├── card.py                  # Base Card class
├── energy_card.py           # Fire, Water, Grass energy support
├── trainer_card.py          # Trainer card logic and effect binding
├── pokemon_card.py          # HP, attacks, evolution logic
│
├── cards/                   # All Pokémon definitions
│   ├── charmander.py        # and other Pokémon like squirtle, bulbasaur, etc.
│
├── README.md                # 💡 You're reading it!
```

---

## 🚀 How to Run

### 1. Clone the Repo / Download Code

```bash
git clone https://github.com/yourname/pokemon-tcg-python.git
cd pokemon-tcg-python
```

Or simply download the `.zip` and extract.

---

### 2. Run the Game

Use Python 3:

```bash
python3 main.py
```

Follow the interactive prompts:
- Choose your Active Pokémon
- Place up to 3 Pokémon on your Bench
- Play Trainer cards
- Attach Energy
- Choose Attacks

---

## 🔮 Future Enhancements

| Feature | Status | Notes |
|--------|--------|-------|
| Retreat energy cost | ⏳ In progress | Deduct attached energy |
| Full Bench management | ✅ Basic | UI cleanup, status effects coming |
| AI player (vs CPU) | 🧠 Planned | Simple rule-based enemy logic |
| Trainer card discard pile | 🗑️ Planned | Currently just removed from hand |
| Win/Loss logging | 📜 Planned | Save game summary to a file |
| GUI version | 💻 Dream feature | Tkinter or Pygame port

---

## 🤝 Credits & Contributions

Created by **Taszid Chowdhury**.  
Built as a personal learning project to understand **object-oriented design**, **turn-based game logic**, and **event-driven gameplay** using Python.

Feel free to fork, clone, remix, and contribute!

---

## 📜 License

MIT License – open-source, free to use, modify, and share.

Gotta code 'em all! 🧠🔥💧🌿
