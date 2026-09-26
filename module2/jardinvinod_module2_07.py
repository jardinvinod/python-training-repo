# Import json to save and load the game session
import json


# Function to display the board neatly
def display_board(board):

    print("\n+------+------+------+------+")
    
    for row in board:
        for value in row:

            # Show "." for empty cells
            if value == 0:
                display_value = "."
            else:
                display_value = str(value)

            # Print each value inside a fixed-width cell
            print(f"|{display_value:^6}", end="")

        print("|")
        print("+------+------+------+------+")


# Function to merge one row to the left
def merge_left(row):

    # Remove all zeros
    numbers = []

    for number in row:
        if number != 0:
            numbers.append(number)

    # List to store merged numbers
    merged = []

    i = 0

    while i < len(numbers):

        # Merge equal adjacent numbers
        if i + 1 < len(numbers) and numbers[i] == numbers[i + 1]:

            merged.append(numbers[i] * 2)

            # Skip both numbers
            i += 2

        else:

            merged.append(numbers[i])

            i += 1

    # Add zeros until the row has 4 values
    while len(merged) < 4:
        merged.append(0)

    return merged


# Function to move board left
def move_left(board):

    new_board = []

    for row in board:
        new_board.append(merge_left(row))

    return new_board


# Function to move board right
def move_right(board):

    new_board = []

    for row in board:

        # Reverse the row
        reversed_row = row[::-1]

        # Merge it to the left
        merged_row = merge_left(reversed_row)

        # Reverse it back
        merged_row = merged_row[::-1]

        new_board.append(merged_row)

    return new_board


# Function to transpose rows and columns
def transpose(board):

    new_board = []

    for column in range(4):

        new_row = []

        for row in range(4):
            new_row.append(board[row][column])

        new_board.append(new_row)

    return new_board


# Function to move board up
def move_up(board):

    transposed = transpose(board)

    moved = move_left(transposed)

    return transpose(moved)


# Function to move board down
def move_down(board):

    transposed = transpose(board)

    moved = move_right(transposed)

    return transpose(moved)


# Function to check if player reached 2048
def check_win(board):

    for row in board:

        if 2048 in row:
            return True

    return False


# Function to check if any moves are still possible
def moves_available(board):

    # Check for empty cells
    for row in board:
        if 0 in row:
            return True

    # Check horizontal neighbours
    for row in range(4):

        for column in range(3):

            if board[row][column] == board[row][column + 1]:
                return True

    # Check vertical neighbours
    for column in range(4):

        for row in range(3):

            if board[row][column] == board[row + 1][column]:
                return True

    return False


# Function to add a new tile
def add_new_tile(board):

    # Find the first empty cell
    for row in range(4):

        for column in range(4):

            if board[row][column] == 0:

                # Add a new tile
                board[row][column] = 2

                return


# Function to save the current game session
def save_game(board):

    # Store game information in dictionary format
    game_data = {
        "board": board
    }

    # Save dictionary into JSON file
    with open("2048_game_session.json", "w") as file:

        json.dump(game_data, file, indent=4)

    print("Game saved successfully.")


# Function to load the previous game session
def load_game():

    try:
        # Open the saved JSON file
        with open("2048_game_session.json", "r") as file:

            game_data = json.load(file)

        print("Previous game loaded successfully.")

        # Return the saved board
        return game_data["board"]

    except FileNotFoundError:

        # If the file does not exist, return None
        print("No saved game found.")

        return None


# Function to start a new game
def new_game():

    return [
        [2, 2, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]


# Main function to play the game
def play_2048():

    print("2048 ADVANCED GAME")

    print("\n1 - Start New Game")
    print("2 - Continue Saved Game")

    choice = input("Choose an option: ")

    # Start a new game
    if choice == "1":

        board = new_game()

    # Load saved game
    elif choice == "2":

        board = load_game()

        # If there is no saved game, start a new one
        if board is None:

            print("Starting a new game instead.")

            board = new_game()

    else:

        print("Invalid choice. Starting a new game.")

        board = new_game()


    print("\nControls:")
    print("W = Up")
    print("A = Left")
    print("S = Down")
    print("D = Right")
    print("P = Save Game")
    print("Q = Quit")


    while True:

        # Display current board
        display_board(board)

        # Check if player reached 2048
        if check_win(board):

            print("Congratulations! You reached 2048!")

            # Save final game state
            save_game(board)

            break

        # Check if no moves are possible
        if not moves_available(board):

            print("Game Over!")

            # Save final game state
            save_game(board)

            break

        # Ask the player for a move
        move = input(
            "Enter your move (W/A/S/D/P/Q): "
        ).lower()


        # Save game
        if move == "p":

            save_game(board)

            continue


        # Quit game
        elif move == "q":

            # Save automatically before quitting
            save_game(board)

            print("Game saved. You can continue later.")

            break


        # Store current board before making the move
        old_board = [row[:] for row in board]


        # Move up
        if move == "w":

            board = move_up(board)


        # Move left
        elif move == "a":

            board = move_left(board)


        # Move down
        elif move == "s":

            board = move_down(board)


        # Move right
        elif move == "d":

            board = move_right(board)


        else:

            print("Invalid input. Use W, A, S, D, P or Q.")

            continue


        # Add a new tile only if something moved
        if board != old_board:

            add_new_tile(board)

            # Automatically save after each valid move
            save_game(board)

        else:

            print("No tiles moved. Try another direction.")


# Start the game
play_2048()