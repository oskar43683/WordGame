
import tkinter as tk
import json
import random

# Load the word pairs from the JSON file
with open('words.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Extract the word pairs
words = data['words']

def get_random_words(words, num=4):
    return random.sample(words, num)

current_round_words = get_random_words(words)

# Prepare the lists of English and Polish words
english_words = [word['english'] for word in current_round_words]
polish_words = [word['polish'] for word in current_round_words]

random.shuffle(english_words)
random.shuffle(polish_words)

# Store the user's selected word pairs
selected_english = None
selected_polish = None

# Function to handle the matching logic
def check_match():
    global selected_english, selected_polish
    # Find the correct pair
    correct_pair = next((pair for pair in words if pair['english'] == selected_english and pair['polish'] == selected_polish), None)
    
    if correct_pair:
        result_label.config(text="Correct!", fg="green")
    else:
        result_label.config(text="Try again!", fg="red")

    # Reset selected words
    selected_english = None
    selected_polish = None
    english_buttons()

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
    global selected_english
    selected_english = button.cget('text')
    button.config(bg="lightgray", state="disabled")  # Disable after selection
    polish_buttons()

def select_polish(button):
    global selected_polish
    selected_polish = button.cget('text')
    button.config(bg="lightgray", state="disabled")  # Disable after selection
    check_match()

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

# Add English word buttons
for word in english_words:
    button = tk.Button(english_frame, text=word, font = ("Arial", 12), width=15, height=2)
    button.pack(pady=5)

# Add Polish word buttons

for word in polish_words:
    button = tk.Button(polish_frame, text=word, font = ("Arial", 12), width=15, height=2)
    button.pack(pady=5)

# Start with the English buttons
english_buttons()

# Run the Tkinter main loop
root.mainloop()