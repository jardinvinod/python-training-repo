# 2048 Game - Terminal Version


# Function to display the board
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


# Function to move and merge one row to the left
def merge_left(row):

    # Remove all empty spaces (0)
    numbers = []

    for number in row:
        if number != 0:
            numbers.append(number)

    # List for the merged row
    merged = []

    i = 0

    while i < len(numbers):

        # Check if the current number and next number are equal
        if i + 1 < len(numbers) and numbers[i] == numbers[i + 1]:

            # Merge the two equal numbers
            merged.append(numbers[i] * 2)

            # Skip the next number because it has already been merged
            i += 2

        else:
            # Keep the number without merging
            merged.append(numbers[i])

            i += 1

    # Add zeros until the row has 4 values
    while len(merged) < 4:
        merged.append(0)

    return merged


# Function to move all rows left
def move_left(board):

    new_board = []

    for row in board:
        new_board.append(merge_left(row))

    return new_board


# Function to move all rows right
def move_right(board):

    new_board = []

    for row in board:

        # Reverse the row
        reversed_row = row[::-1]

        # Merge as if moving left
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


# Function to move tiles upward
def move_up(board):

    # Convert columns into rows
    transposed = transpose(board)

    # Move those rows left
    moved = move_left(transposed)

    # Convert rows back into columns
    return transpose(moved)


# Function to move tiles downward
def move_down(board):

    # Convert columns into rows
    transposed = transpose(board)

    # Move those rows right
    moved = move_right(transposed)

    # Convert rows back into columns
    return transpose(moved)


# Function to check if 2048 has been reached
def check_win(board):

    for row in board:

        if 2048 in row:
            return True

    return False


# Function to check if there are any possible moves
def moves_available(board):

    # If there is an empty cell, a move is still possible
    for row in board:
        if 0 in row:
            return True

    # Check horizontal neighbouring tiles
    for row in range(4):

        for column in range(3):

            if board[row][column] == board[row][column + 1]:
                return True

    # Check vertical neighbouring tiles
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

                # Add a new tile with value 2
                board[row][column] = 2

                return


# Function to play the game
def play_2048():

    # Create an empty 4 x 4 board
    board = [
        [2, 2, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    print("2048 GAME")

    print("Controls:")
    print("W = Up")
    print("A = Left")
    print("S = Down")
    print("D = Right")
    print("Q = Quit")

    while True:

        # Display the board
        display_board(board)

        # Check if player has reached 2048
        if check_win(board):
            print("Congratulations! You reached 2048!")
            break

        # Check if there are no possible moves
        if not moves_available(board):
            print("Game Over! No more moves available.")
            break

        # Get movement from the user
        choice = input("Enter your move (W/A/S/D/Q): ").lower()

        # Store the old board
        old_board = [row[:] for row in board]

        # Process the player's choice
        if choice == "w":
            board = move_up(board)

        elif choice == "a":
            board = move_left(board)

        elif choice == "s":
            board = move_down(board)

        elif choice == "d":
            board = move_right(board)

        elif choice == "q":
            print("Game ended.")
            break

        else:
            print("Invalid input. Please use W, A, S, D or Q.")
            continue

        # Add a new tile only when the board has changed
        if board != old_board:
            add_new_tile(board)

        else:
            print("No tiles moved. Try another direction.")


# Start the game
play_2048()