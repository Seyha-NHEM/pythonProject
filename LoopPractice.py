''''
Initialize
    Set count = 0 to keep track of the score difference.
Create the UI:
    Create a Tkinter window with a title "Rock, Paper, Scissors Game".
    add a label prompting the user to enter their choice (0 for scissor, 1 for rock, 2 for paper).
    Add an entry widget for the user to input their choice.
    Add a button labeled "Play" that triggers the game logic when clicked.
    Add a label to display the result of the game.
Play Game:
    Retrieve User Input:
    Get the user's choice from the entry widget.
    Validate if the input is an integer and within the range [0, 2].
    Generate Computer Choice:
    Generate a random integer between 0 and 2 for the computer's choice.
Compare Choices:
    If the user's choice is equal to the computer's choice:
    Set the result to "It is a draw."
    If the user’s choice wins against the computer’s choice:
    Set the result to "You won!".
    Increment count by 1.
    If the computer's choice wins:
    Set the result to "Computer won!".
    Decrement count by 1.
    Check Game End Condition:
    If abs(count) >= 3:
    If count > 2, set the result to "Congratulations! You won more than two times continuously."
    Otherwise, set the result to "The computer won more than two times continuously."
    Reset count to 0.
Clear Input Field:
    Clear the user input entry widget.
Run the Application:
    Start the Tkinter main loop to display the UI and handle user interactions.
'''











import tkinter as tk
import random


def play_game():
    try:
        user_choice = int(user_input.get())
    except ValueError:
        result.set("Invalid input! Please enter an integer.")
        return

    if user_choice not in [0, 1, 2]:
        result.set("Invalid input! Please enter 0, 1, or 2.")
        return

    computer_choice = random.randint(0, 2)

    if computer_choice == user_choice:
        outcome = "It is a draw."
    elif (user_choice == 0 and computer_choice == 1) or \
         (user_choice == 1 and computer_choice == 2) or \
         (user_choice == 2 and computer_choice == 0):
        outcome = "You won!"
        global count
        count += 1
    else:
        outcome = "Computer won!"
        count -= 1

    if abs(count) >= 3:
        if count > 0:
            result.set("Congratulations! You won more than two times continuously.")
        else:
            result.set("The computer won more than two times continuously.")
        count = 0  # Reset count for new game
    else:
        result.set(outcome)

    user_input.delete(0, tk.END)  # Clear the input field


# Create UI window
window = tk.Tk()
window.title("Rock, Paper, Scissors Game")

# Initialize count
count = 0

# UI Elements
tk.Label(window, text="Enter your choice (0 for scissor, 1 for rock, 2 for paper):").pack()
user_input = tk.Entry(window)
user_input.pack()

tk.Button(window, text="Play", command=play_game).pack()

result = tk.StringVar()
tk.Label(window, textvariable=result).pack()

# Run the application
window.mainloop()

