
import tkinter as tk
import json
import random

# Load the word pairs from a UTF-8 encoded JSON file
with open('words.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Extract the word pairs from the loaded data
words = data['words']

# Function to get a random subset of 4 words
def get_random_words(words, num=4):
    return random.sample(words, num)  # Randomly select 'num' words

# Get 4 random word pairs for the current round
current_round_words = get_random_words(words)

# Prepare the lists of English and Polish words from the current round
english_words = [word['english'] for word in current_round_words]
polish_words = [word['polish'] for word in current_round_words]

# Shuffle both the English and Polish words
random.shuffle(english_words)
random.shuffle(polish_words)

# Store the user's selected word pairs
selected_english = None
selected_polish = None
selected_english_button = None
selected_polish_button = None
correct_matches = 0

# Function to handle the matching logic
def check_match():
    global selected_english, selected_polish, selected_english_button, selected_polish_button, correct_matches
    # Find the correct pair (matching the selected words)
    correct_pair = next((pair for pair in current_round_words if pair['english'] == selected_english and pair['polish'] == selected_polish), None)
    
    if correct_pair:
        result_label.config(text="Correct!", fg="green")
        selected_english_button.config(state="disabled", bg="lightgreen")
        selected_polish_button.config(state="disabled", bg="lightgreen")
        correct_matches += 1
    else:
        result_label.config(text="Try again!", fg="red")
        root.after(1000, flip_back)  # Wait 1 second before flipping back
    
    if correct_matches == len(current_round_words):
        result_label.config(text="You won!", fg="blue")
        disable_buttons()
    
    # Reset selected words
    selected_english = None
    selected_polish = None
    selected_english_button = None
    selected_polish_button = None

# Function to update the buttons based on user interaction
def english_buttons():
    for widget in english_frame.winfo_children():
        widget.config(bg="lightblue", state="normal")
    
    for button in english_frame.winfo_children():
        button.config(command=lambda button=button: select_english(button))

def polish_buttons():
    for widget in polish_frame.winfo_children():
        widget.config(bg="lightgreen", state="normal")

    for button in polish_frame.winfo_children():
        button.config(command=lambda button=button: select_polish(button))

def select_english(button):
    global selected_english, selected_english_button
    selected_english = button.cget('text')
    selected_english_button = button
    button.config(bg="lightgray", state="disabled")  # Disable after selection
    polish_buttons()

def select_polish(button):
    global selected_polish, selected_polish_button
    selected_polish = button.cget('text')
    selected_polish_button = button
    button.config(bg="lightgray", state="disabled")  # Disable after selection
    check_match()

# Function to flip back the words if they do not match
def flip_back():
    selected_english_button.config(bg="lightblue", state="normal")
    selected_polish_button.config(bg="lightgreen", state="normal")
    
    # Reset the button states
    selected_english_button = None
    selected_polish_button = None

def disable_buttons():
    for widget in english_frame.winfo_children():
        widget.config(state="disabled")
    for widget in polish_frame.winfo_children():
        widget.config(state="disabled")

# Initialize the main window
root = tk.Tk()
root.title("Match the Words Game")

# Create the frames for the buttons
english_frame = tk.Frame(root)
english_frame.pack(side="left", padx=10)

polish_frame = tk.Frame(root)
polish_frame.pack(side="right", padx=10)

result_label = tk.Label(root, text="", font=("Helvetica", 14))
result_label.pack(pady=20)

# Add English word buttons (only the selected random 4 words)
for word in english_words:
    button = tk.Button(english_frame, text=word, font=("Arial", 14), width=15, height=2)
    button.pack(pady=5)

# Add Polish word buttons (only the selected random 4 words)
for word in polish_words:
    button = tk.Button(polish_frame, text=word, font=("Arial", 14), width=15, height=2)
    button.pack(pady=5)

# Start with the English buttons
english_buttons()


# Run the Tkinter main loop
root.mainloop()
