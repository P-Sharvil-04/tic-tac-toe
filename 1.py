# Tic Tac Toe Game in Python

board = [" " for _ in range(9)]

def print_board():
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")

def check_winner(player):
    win_conditions = [
        [0,1,2], [3,4,5], [6,7,8],  # rows
        [0,3,6], [1,4,7], [2,5,8],  # columns
        [0,4,8], [2,4,6]            # diagonals
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True
    return False

def is_draw():
    return " " not in board

def play_game():
    current_player = "X"

    while True:
        print_board()
        try:
            move = int(input(f"Player {current_player}, choose position (1-9): ")) - 1
        except ValueError:
            print("Invalid input! Enter number 1-9.")
            continue

        if move < 0 or move > 8:
            print("Position out of range! Choose 1-9.")
            continue

        if board[move] != " ":
            print("Position already taken! Try again.")
            continue

        board[move] = current_player

        if check_winner(current_player):
            print_board()
            print(f"🎉 Player {current_player} wins!")
            break

        if is_draw():
            print_board()
            print("🤝 It's a draw!")
            break

        current_player = "O" if current_player == "X" else "X"

# Run the game
play_game()