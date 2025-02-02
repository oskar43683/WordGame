import tkinter as tk
import random
import json
import level_selection
import sys
import os

def update_points_in_file(username, new_points, data_file_path):
    """Update the user's points in the data file."""
    if not username or not data_file_path:
        raise ValueError("Username and data file path are required")
    
    try:
        with open(data_file_path, "r") as file:
            lines = file.readlines()
        
        with open(data_file_path, "w") as file:
            for line in lines:
                fields = line.strip().split(",")
                if len(fields) != 3:
                    raise ValueError("Malformed line in file")
                if fields[0] == username:
                    # Update the points for the logged-in user
                    fields[2] = str(new_points)
                    line = ",".join(fields) + "\n"
                file.write(line)
    except FileNotFoundError:
        print(f"Error updating points: File '{data_file_path}' not found")
    except IOError as e:
        print(f"Error updating points: I/O error occurred when writing to '{data_file_path}': {e}")
    except Exception as e:
        print(f"Error updating points: {e}")

def start_match_game(frame, go_back_callback, level_file, username, points):
    for widget in frame.winfo_children():
        widget.destroy()

    words = get_level_words(level_file)
    if not words:
        tk.Label(
            frame,
            text="Error loading words. Please try a different level.",
            font=("Arial", 18),
            bg="#1a1a2e",
            fg="#ff3860"
        ).pack(pady=20)
        tk.Button(
            frame,
            text="Back to Menu",
            font=("Arial", 14),
            bg="#16213e",
            fg="#ffffff",
            command=go_back_callback
        ).pack(pady=20)
        return

    def get_random_words(words, num=5):
        return random.sample(words, num)

    current_round_words = get_random_words(words)

    english_words = [word['english'] for word in current_round_words]
    polish_words = [word['polish'] for word in current_round_words]

    random.shuffle(english_words)
    random.shuffle(polish_words)

    selected_english = None
    selected_polish = None
    selected_english_button = None
    selected_polish_button = None
    correct_matches = 0
    temp_points = 0

    def check_match():
        nonlocal selected_english, selected_polish, selected_english_button, selected_polish_button, correct_matches, points, temp_points

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
            data_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gamedata", "data.txt")
            try:
                update_points_in_file(username, points, data_file_path)
            except Exception as e:
                print(f"Error updating points: {e}")
        else:
            result_label.config(text="Try again!", fg="red")
            selected_english_button.config(state="normal", bg="lightblue")
            selected_polish_button.config(state="normal", bg="lightgreen")

        if correct_matches == len(current_round_words):
            result_label.config(text="You won!", fg="blue")
            disable_buttons()

        selected_english = None
        selected_polish = None
        selected_english_button = None
        selected_polish_button = None

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

    english_frame = tk.Frame(frame, bg="#1a1a2e")
    english_frame.pack(side="left", padx=20)

    polish_frame = tk.Frame(frame, bg="#1a1a2e")
    polish_frame.pack(side="right", padx=20)

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

    for word in polish_words:
        button = tk.Button(
            polish_frame, 
            text=word, 
            font=("Arial", 14), 
            bg="lightgreen", 
            width=30, 
            height=2
        )
        button.config(command=lambda button=button: select_polish(button))
        button.pack(pady=5)

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
        base_path = getattr(sys, '_MEIPASS', None)
        if base_path is None:
            raise ValueError("_MEIPASS is not set")
    else:
        base_path = os.path.dirname(__file__)
        if base_path is None:
            raise ValueError("__file__ is not set")
    return os.path.join(base_path, relative_path)

def get_level_words(level_file):
    """Load words from the selected level JSON file."""
    level_path = get_resource_path(f"levels/{level_file}")
    if level_path is None:
        raise ValueError("Level file path is not set")
    if not os.path.isfile(level_path):
        raise FileNotFoundError(f"Level file not found: {level_path}")
    with open(level_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON: {e}")
    if 'words' not in data:
        raise ValueError("Level file does not contain 'words' key")
    return data['words']
