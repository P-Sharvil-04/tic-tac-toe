from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

board = [" "] * 9
current_player = "X"

WIN_COMBOS = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
]

def check_winner(player):
    for combo in WIN_COMBOS:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == player:
            return True
    return False

def is_draw():
    return " " not in board

@app.route("/")
def home():
    return render_template("index.html", board=board, player=current_player)

@app.route("/move/<int:pos>")
def move(pos):
    global current_player

    if board[pos] == " ":
        board[pos] = current_player

        if check_winner(current_player):
            return render_template("index.html", board=board, player=f"{current_player} Wins!")

        if is_draw():
            return render_template("index.html", board=board, player="Draw!")

        current_player = "O" if current_player == "X" else "X"

    return redirect(url_for("home"))

@app.route("/reset")
def reset():
    global board, current_player
    board = [" "] * 9
    current_player = "X"
    return redirect(url_for("home"))

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)