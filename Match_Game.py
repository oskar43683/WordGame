import tkinter as tk
import random
import json
import level_selection
import sys
import os
from login import GameApp

def update_points_in_file(username, new_points, file_path="data.txt"):
    """Update the user's points in the data file."""
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
        
        with open(file_path, "w") as file:
            for line in lines:
                fields = line.strip().split(",")
                if fields[0] == username:
                    # Update the points for the logged-in user
                    fields[2] = str(new_points)
                    line = ",".join(fields) + "\n"
                file.write(line)
    except Exception as e:
        print(f"Error updating points: {e}")

def start_match_game(frame, go_back_callback, level_file, username, points):
    for widget in frame.winfo_children():
        widget.destroy()

    words = get_level_words(level_file)

    def get_random_words(words, num=5):
        return random.sample(words, num)

    current_round_words = get_random_words(words)

    english_words = [word['english'] for word in current_round_words]
    polish_words = [word['polish'] for word in current_round_words]

    # Shuffle both the English and Polish words
    random.shuffle(english_words)
    random.shuffle(polish_words)

    # Variables to track the game state
    selected_english = None
    selected_polish = None
    selected_english_button = None
    selected_polish_button = None
    correct_matches = 0
    temp_points = 0

    def check_match():
        nonlocal selected_english, selected_polish, selected_english_button, selected_polish_button, correct_matches, points, temp_points

        # Check if the selected pair matches
        correct_pair = next(
            (pair for pair in current_round_words 
                if pair['english'] == selected_english and pair['polish'] == selected_polish),
            None,
        )

        if correct_pair:
            result_label.config(text="Correct!", fg="green")
            selected_english_button.config(state="disabled", bg="lime")
            selected_polish_button.config(state="disabled", bg="lime")
            correct_matches += 1
            points += 15
            temp_points += 15
            temp_points_label.config(text=f"Points: {temp_points}")
            update_points_in_file(username, points)
        else:
            result_label.config(text="Try again!", fg="red")
            selected_english_button.config(state="normal", bg="lightblue")
            selected_polish_button.config(state="normal", bg="lightgreen")
            #frame.after(1000, flip_back)

        if correct_matches == len(current_round_words):
            result_label.config(text="You won!", fg="blue")
            disable_buttons()

        # Reset selections
        selected_english = None
        selected_polish = None
        selected_english_button = None
        selected_polish_button = None

    # Disable all buttons when the game ends
    def disable_buttons():
        for widget in english_frame.winfo_children():
            widget.config(state="disabled")
        for widget in polish_frame.winfo_children():
            widget.config(state="disabled")

    def select_english(button):
        nonlocal selected_english, selected_english_button
        selected_english = button.cget("text")
        selected_english_button = button
        if selected_polish:
            check_match()

    def select_polish(button):
        nonlocal selected_polish, selected_polish_button
        selected_polish = button.cget("text")
        selected_polish_button = button
        if selected_english:
            check_match()
        # else:
        #     result_label.config(text="Select an English word first!", fg="orange")
        #     button.config(bg="lightgreen", state="normal")

    # Add UI components to the frame
    label = tk.Label(
        frame, 
        text="Match the Words Game", 
        font=("Arial", 18), 
        bg="#1a1a2e", 
        fg="#ffffff"
    )
    label.pack(pady=10)

    temp_points_label = tk.Label(
        frame,
        text=f"Points: {temp_points}",
        font=("Helvetica", 14),
        bg="#1a1a2e",
        fg="#ffffff"
    )
    temp_points_label.pack(pady=10)

    result_label = tk.Label(
        frame,
        text="",
        font=("Helvetica", 14), 
        bg="#1a1a2e", 
        fg="#ffffff"
    )
    result_label.pack(pady=10)

    # Create frames for English and Polish words
    english_frame = tk.Frame(frame, bg="#1a1a2e")
    english_frame.pack(side="left", padx=20)

    polish_frame = tk.Frame(frame, bg="#1a1a2e")
    polish_frame.pack(side="right", padx=20)

    # Add English word buttons
    for word in english_words:
        button = tk.Button(
            english_frame, 
            text=word, 
            font=("Arial", 14), 
            bg="lightblue", 
            width=30, 
            height=2
            )
        button.config(command=lambda button=button: select_english(button))
        button.pack(pady=5)

    # Add Polish word buttons
    for word in polish_words:
        button = tk.Button(
            polish_frame, 
            text=word, 
            font=("Arial", 14), 
            bg="lightgreen", 
            width=30, 
            height=2)
        button.config(command=lambda button=button: select_polish(button))
        button.pack(pady=5)

    # Back to menu button
    back_button = tk.Button(
        frame,
        text="Back to Menu",
        font=("Arial", 14),
        bg="#16213e",
        fg="#ffffff",
        activebackground="#0f3460",
        activeforeground="#ffffff",
        command=go_back_callback,
    )
    back_button.pack(pady=10, ipadx=10, ipady=5)

def get_resource_path(relative_path):
    """Get the absolute path to a resource, considering PyInstaller's bundle."""
    if getattr(sys, 'frozen', False):  # Running as a PyInstaller executable
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

def get_level_words(level_file):
    """Load words from the selected level JSON file."""
    level_path = get_resource_path(f"levels/{level_file}")
    with open(level_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['words']