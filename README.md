Chess-Like Game

Overview

This is a web-based chess-like game implemented using Flask and Socket.IO. The game features a 5x5 grid where two players control characters with specific movement rules. The goal is to eliminate all of the opponent's characters.

Features

- Grid-based board: 5x5 grid where players can place and move characters.
- Character types: Pawns and Heroes with different movement rules.
- Real-time play: Players take turns making moves with real-time updates via Socket.IO.
- Gameplay rules: Characters have specific movement rules and combat mechanics.

Setup

Prerequisites

- Python 3.x
- Flask
- Flask-SocketIO

Installation

1. Clone the Repository

   `git clone https://github.com/yourusername/repositoryname.git`
   `cd repositoryname`

2. Install Dependencies

   Create a virtual environment (optional but recommended) and install the required packages:

   `python -m venv venv`
   `source venv/bin/activate  # On Windows use venv\Scripts\activate`
   `pip install -r requirements.txt`

3. Run the Application

   Start the Flask server:

   `python app.py`

   The game will be accessible at `http://127.0.0.1:5000`.

Usage

1. Open the game in your web browser.
2. Enter your name and join the game room.
3. Arrange your characters on the board as per the initial setup.
4. Take turns with your opponent to move characters and eliminate each other’s pieces.

Game Rules

- Pawns: Move one block in any direction (left, right, forward, backward).
- Hero1: Moves two blocks straight in any direction.
- Hero2: Moves two blocks diagonally in any direction.
- Players alternate turns. A character can eliminate an opponent's character by moving to the same cell.
- The game ends when one player eliminates all of the opponent's characters.

Contributing

Contributions are welcome! If you have suggestions or improvements, please create a pull request or open an issue.
