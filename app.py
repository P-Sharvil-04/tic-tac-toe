from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, emit
import random, string, os

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

# ✅ REMOVE threading (auto-selects best async mode like gevent)
socketio = SocketIO(app, cors_allowed_origins="*")

rooms = {}

WIN_COMBOS = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
]

def generate_room():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def check_winner(board):
    for combo in WIN_COMBOS:
        if board[combo[0]] != " " and board[combo[0]] == board[combo[1]] == board[combo[2]]:
            return board[combo[0]], combo
    return None, []

def is_draw(board):
    return " " not in board

@app.route("/")
def home():
    return render_template("index.html")

# ✅ CREATE ROOM
@socketio.on("create_room")
def create_room_event():
    room = generate_room()

    rooms[room] = {
        "board": [" "] * 9,
        "players": {},
        "turn": "X",
        "status": "Waiting for Player O...",
        "winning_combo": []
    }

    join_room(room)
    rooms[room]["players"][request.sid] = "X"

    emit("room_created", {
        "room": room,
        "symbol": "X",
        "game": rooms[room]
    })

# ✅ JOIN ROOM
@socketio.on("join_room")
def join_room_event(data):
    room = data.get("room", "").upper()

    if room not in rooms:
        emit("error", {"msg": "Room not found"})
        return

    game = rooms[room]

    if len(game["players"]) >= 2:
        emit("error", {"msg": "Room full"})
        return

    symbol = "O"
    game["players"][request.sid] = symbol
    join_room(room)

    game["status"] = "Turn: X"

    emit("joined", {"room": room, "symbol": symbol})
    emit("update", game, to=room)

# ✅ HANDLE MOVE
@socketio.on("move")
def move(data):
    room = data.get("room")
    index = data.get("index")
    player = data.get("player")

    game = rooms.get(room)
    if not game:
        return

    if player != game["turn"]:
        return

    if game["board"][index] != " ":
        return

    game["board"][index] = player

    winner, combo = check_winner(game["board"])

    if winner:
        game["status"] = f"Player {winner} Wins!"
        game["winning_combo"] = combo
    elif is_draw(game["board"]):
        game["status"] = "Draw!"
    else:
        game["turn"] = "O" if game["turn"] == "X" else "X"
        game["status"] = f"Turn: {game['turn']}"

    emit("update", game, to=room)

# ✅ RESET GAME
@socketio.on("reset")
def reset(data):
    room = data.get("room")
    game = rooms.get(room)

    if game:
        game["board"] = [" "] * 9
        game["turn"] = "X"
        game["status"] = "Turn: X"
        game["winning_combo"] = []

        emit("update", game, to=room)

# ✅ REMOVE PLAYER WHEN DISCONNECTED
@socketio.on("disconnect")
def handle_disconnect():
    for room, game in list(rooms.items()):
        if request.sid in game["players"]:
            del game["players"][request.sid]

            # Remove empty rooms
            if len(game["players"]) == 0:
                del rooms[room]
            else:
                game["status"] = "Player disconnected"

            emit("update", game, to=room)

# ✅ RUN (LOCAL ONLY)
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)