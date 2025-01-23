import tkinter as tk
import json
import os
from login import get_data_file_path

def get_level_words(level_file):
    """Load words from the selected level JSON file."""
    if not level_file:
        return []

    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Create the full path to the levels directory
    level_path = os.path.join(script_dir, "levels", level_file)
    
    try:
        with open(level_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data.get('words', [])
    except FileNotFoundError:
        print(f"Error loading level words: {level_file} not found")
        print(f"Attempted to load from: {level_path}")  # Added for debugging
        return []
    except json.JSONDecodeError as e:
        print(f"Error loading level words: {e}")
        return []

def update_score(username, points_earned):
    """
    Updates the user's score in the data file.

    :param username: The username to update
    :param points_earned: The points to add to the existing score
    :return: None
    """
    if not username:
        raise ValueError("Username is required")
    if points_earned is None or points_earned < 0:
        raise ValueError("Points earned must be a positive integer")
    
    try:
        file_path = get_data_file_path()
        if not file_path:
            raise ValueError("File path is empty")
        
        with open(file_path, "r") as file:
            lines = file.readlines()
            if not lines:
                raise ValueError("File is empty")
        
        with open(file_path, "w") as file:
            for line in lines:
                fields = line.strip().split(",")
                if len(fields) < 3:
                    raise ValueError("Malformed line in file")
                
                if fields[0] == username:
                    try:
                        current_points = int(fields[2])
                    except ValueError:
                        raise ValueError("Points are not a valid integer")
                    
                    # Update points by adding new points to existing points
                    fields[2] = str(current_points + points_earned)
                    line = ",".join(fields) + "\n"
                file.write(line)
    except Exception as e:
        print(f"Error updating points: {e}")

def start_word_game(frame, callback, level_file, username):
    # Clear the frame
    for widget in frame.winfo_children():
        widget.destroy()

    if not level_file or level_file == "back_to_menu":
        callback()
        return

    # Load words from the selected level
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
            command=callback
        ).pack(pady=20)
        return

    current_word_index = 0
    current_score = 0
    letter_entries = []  # Store references to letter entry widgets

    # Create UI elements
    title_label = tk.Label(
        frame,
        text="Spelling Game",
        font=("Arial", 24, "bold"),
        bg="#1a1a2e",
        fg="#ffffff"
    )
    title_label.pack(pady=20)

    # Display Polish word
    polish_word_label = tk.Label(
        frame,
        text=words[current_word_index]['polish'],
        font=("Arial", 18),
        bg="#1a1a2e",
        fg="#ffffff"
    )
    polish_word_label.pack(pady=10)

    # Create frame for letter entries
    letters_frame = tk.Frame(frame, bg="#1a1a2e")
    letters_frame.pack(pady=20)

    def create_letter_entries(word_length):
        nonlocal letter_entries
        # Clear existing entries
        for entry in letter_entries:
            entry.destroy()
        letter_entries.clear()
        
        # Create new entries
        current_column = 0
        word = words[current_word_index]['english']
        
        for i in range(len(word)):
            if word[i] == ' ':
                # Add a separator label between words
                separator = tk.Label(
                    letters_frame,
                    text="-",
                    font=("Arial", 16),
                    bg="#1a1a2e",
                    fg="#ffffff"
                )
                separator.grid(row=0, column=current_column, padx=5)
                current_column += 1
                continue
                
            entry = tk.Entry(
                letters_frame,
                font=("Arial", 16),
                width=2,
                justify='center'
            )
            entry.grid(row=0, column=current_column, padx=2)
            entry.bind('<Key>', lambda e, idx=i: handle_key_input(e, idx))
            letter_entries.append(entry)
            current_column += 1

    def handle_key_input(event, current_index):
        # Handle Enter key press to submit
        if event.keysym == 'Return':
            check_word()
            return "break"
            
        # Ignore other special key events
        if not event.char:
            return
        
        # Find the actual entry index (accounting for spaces)
        word = words[current_word_index]['english']
        entry_index = len([i for i in range(current_index) if word[i] != ' '])
        current_entry = letter_entries[entry_index]
        
        # Handle backspace
        if event.keysym == 'BackSpace':
            if entry_index > 0 and not current_entry.get():
                # If current box is empty, move to previous box
                letter_entries[entry_index - 1].focus()
                letter_entries[entry_index - 1].delete(0, tk.END)
            return
        
        # Handle letter input (now including _, ?, ,, and ')
        if event.char.isalpha() or event.char in ['_', '?', ',', "'"]:
            # Clear any existing content and insert the new character
            current_entry.delete(0, tk.END)
            current_entry.insert(0, event.char)
            
            # Find next non-space position
            next_char_index = current_index + 1
            while next_char_index < len(word) and word[next_char_index] == ' ':
                next_char_index += 1
                
            # Move to next box if available
            if next_char_index < len(word) and entry_index < len(letter_entries) - 1:
                letter_entries[entry_index + 1].focus()
        
        # Prevent default handling
        return "break"

    # Initialize letter entries for first word
    create_letter_entries(len(words[current_word_index]['english']))

    # Feedback label
    feedback_label = tk.Label(
        frame,
        text="",
        font=("Arial", 14),
        bg="#1a1a2e",
        fg="#ffffff"
    )
    feedback_label.pack(pady=10)

    # Score label
    score_label = tk.Label(
        frame,
        text=f"Score: {current_score}",
        font=("Arial", 16),
        bg="#1a1a2e",
        fg="#ffffff"
    )
    score_label.pack(pady=10)

    def check_word():
        nonlocal current_word_index, current_score
        correct_word = words[current_word_index]['english'].lower()
        
        # Reconstruct user input with spaces
        user_chars = []
        entry_index = 0
        for char in correct_word:
            if char == ' ':
                user_chars.append(' ')
            else:
                user_chars.append(letter_entries[entry_index].get().lower())
                entry_index += 1
        user_input = ''.join(user_chars)

        # Calculate score based on correct letters
        word_score = sum(1 for a, b in zip(user_input, correct_word) if a == b)

        if user_input == correct_word:
            word_score += 5  # Bonus for perfect match
            feedback_label.config(text="Correct! +5 bonus points!", fg="#48c774")
        else:
            feedback_label.config(text=f"The correct word was: {correct_word}", fg="#ff3860")

        current_score += word_score
        score_label.config(text=f"Score: {current_score}")
        
        update_score(username, word_score)

        # Move to next word or end game
        current_word_index += 1
        if current_word_index < len(words):
            polish_word_label.config(text=words[current_word_index]['polish'])
            # Create new letter entries for the next word
            create_letter_entries(len(words[current_word_index]['english']))
            letter_entries[0].focus()  # Focus first entry
        else:
            end_game()

    def end_game():
        for widget in frame.winfo_children():
            widget.destroy()

        tk.Label(
            frame,
            text="Game Over!",
            font=("Arial", 24, "bold"),
            bg="#1a1a2e",
            fg="#ffffff"
        ).pack(pady=20)

        tk.Label(
            frame,
            text=f"Final Score: {current_score}",
            font=("Arial", 18),
            bg="#1a1a2e",
            fg="#ffffff"
        ).pack(pady=20)

        tk.Button(
            frame,
            text="Back to Menu",
            font=("Arial", 14),
            bg="#16213e",
            fg="#ffffff",
            command=callback
        ).pack(pady=20)

    # Submit button
    submit_button = tk.Button(
        frame,
        text="Submit",
        font=("Arial", 14),
        bg="#16213e",
        fg="#ffffff",
        command=check_word
    )
    submit_button.pack(pady=10)

    # Back button
    back_button = tk.Button(
        frame,
        text="Back to Menu",
        font=("Arial", 14),
        bg="#16213e",
        fg="#ffffff",
        command=callback
    )
    back_button.pack(pady=10)

    # Focus first entry
    if letter_entries:
        letter_entries[0].focus()
#