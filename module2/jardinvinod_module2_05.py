# Function to display the game board
def display_board(board):
    print()
    print(board[0], "|", board[1], "|", board[2])
    print("--+---+--")
    print(board[3], "|", board[4], "|", board[5])
    print("--+---+--")
    print(board[6], "|", board[7], "|", board[8])
    print()


# Function to check if a player has won
def check_winner(board, player):

    # All possible winning combinations
    winning_combinations = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]

    # Check each winning combination
    for combination in winning_combinations:
        if (
            board[combination[0]] == player
            and board[combination[1]] == player
            and board[combination[2]] == player
        ):
            return True

    return False


# Function to play the X/O game
def play_game():

    # Board positions are shown as numbers from 1 to 9
    board = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

    # Player X starts first
    current_player = "X"

    # Maximum number of moves is 9
    for move in range(9):

        # Display current board
        display_board(board)

        # Ask the current player to choose a position
        try:
            choice = int(
                input(
                    "Player "
                    + current_player
                    + ", choose a position (1-9): "
                )
            )

            # Check if the number is between 1 and 9
            if choice < 1 or choice > 9:
                print("Invalid choice. Please enter a number from 1 to 9.")
                continue

            # Convert choice to list index
            position = choice - 1

            # Check if the position is already occupied
            if board[position] == "X" or board[position] == "O":
                print("That position is already taken.")
                continue

            # Place X or O on the board
            board[position] = current_player

            # Check if the current player has won
            if check_winner(board, current_player):
                display_board(board)
                print("Player", current_player, "wins!")
                return

            # Change player
            if current_player == "X":
                current_player = "O"
            else:
                current_player = "X"

        except ValueError:
            # Handle input that is not a number
            print("Invalid input. Please enter a number from 1 to 9.")

    # If all 9 moves are used and nobody wins
    display_board(board)
    print("Game is a draw!")


# Start the game
play_game()