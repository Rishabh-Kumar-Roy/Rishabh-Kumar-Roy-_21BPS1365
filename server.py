from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room

# Initialize Flask app and SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Dictionary to keep track of games
games = {}

# Route for index page
@app.route('/')
def index():
    return render_template('index.html')

# Function to initialize game positions (newly added for setup)
def initialize_positions(room):
    games[room]['positions'] = [
        'P1-Pawn', 'P1-Pawn', 'P1-Pawn', 'P1-Pawn', 'P1-Pawn',
        None, None, None, None, None,
        None, None, None, None, None,
        None, None, None, None, None,
        'P2-Pawn', 'P2-Pawn', 'P2-Pawn', 'P2-Pawn', 'P2-Pawn'
    ]
    # Emit initial positions to all players in the room
    for index, character in enumerate(games[room]['positions']):
        if character:
            player, char = character.split('-')
            emit('update_board', {'cell': index, 'character': char, 'player': player}, room=room)

# Event handler for player joining the game
@socketio.on('join_game')
def on_join(data):
    room = data['room']
    username = data['username']
    join_room(room)

    if room not in games:
        games[room] = {
            'players': [],
            'positions': [None] * 25
        }
        initialize_positions(room)

    games[room]['players'].append(username)
    emit('status', {'msg': f"{username} has joined the game!"}, room=room)

# Event handler for making a move
@socketio.on('make_move')
def on_move(data):
    room = data['room']
    character = data['character']
    move = data['move']
    player = data['player']

    positions = games[room]['positions']
    current_pos = positions.index(f"{player}-{character}") if f"{player}-{character}" in positions else None

    if current_pos is not None:
        new_pos = None

        # Determine new position based on character and move
        if character.startswith('P') or character.startswith('H1'):
            if move == 'L':
                new_pos = current_pos - 1 if current_pos % 5 > 0 else None
            elif move == 'R':
                new_pos = current_pos + 1 if current_pos % 5 < 4 else None
            elif move == 'F':
                new_pos = current_pos - 5 if current_pos >= 5 else None
            elif move == 'B':
                new_pos = current_pos + 5 if current_pos < 20 else None

            if character.startswith('H1') and new_pos is not None:
                # Allow H1 to move 2 blocks straight
                if move in ['L', 'R', 'F', 'B']:
                    if move == 'L':
                        new_pos -= 1 if new_pos % 5 > 0 else 0
                    elif move == 'R':
                        new_pos += 1 if new_pos % 5 < 4 else 0
                    elif move == 'F':
                        new_pos -= 5 if new_pos >= 5 else 0
                    elif move == 'B':
                        new_pos += 5 if new_pos < 20 else 0

        elif character.startswith('H2'):
            if move == 'FL':
                new_pos = current_pos - 6 if current_pos >= 6 and current_pos % 5 > 0 else None
            elif move == 'FR':
                new_pos = current_pos - 4 if current_pos >= 4 and current_pos % 5 < 4 else None
            elif move == 'BL':
                new_pos = current_pos + 4 if current_pos < 21 and current_pos % 5 > 0 else None
            elif move == 'BR':
                new_pos = current_pos + 6 if current_pos < 19 and current_pos % 5 < 4 else None

        # Check for combat and move validation
        if new_pos is not None and (positions[new_pos] is None or positions[new_pos].split('-')[0] != player):
            positions[current_pos] = None
            positions[new_pos] = f"{player}-{character}"
            emit('update_board', {'cell': new_pos, 'character': character, 'player': player}, room=room)
        else:
            emit('status', {'msg': 'Invalid move!'}, room=player)
    else:
        emit('status', {'msg': 'Character not found!'}, room=player)

# Run the Flask app with SocketIO
if __name__ == '__main__':
    socketio.run(app, debug=True)
