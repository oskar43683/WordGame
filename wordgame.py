import tkinter as tk
import random
from PIL import Image, ImageTk  # To handle the background image

def start_word_game(frame, go_back_callback):
    # Clear the frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Load and set the background image
    bg_image = Image.open("game/ocean.png")  # Replace with your image path
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(frame, image=bg_photo)
    bg_label.image = bg_photo  # Keep a reference to avoid garbage collection
    bg_label.place(relwidth=1, relheight=1)  # Cover the entire frame

    # Game Variables
    word_list = ["word", "game", "code", "beat", "text"]
    target_word = random.choice(word_list)
    target_index = 0
    letters_correct = 0

    # UI Elements
    title_label = tk.Label(
        frame, text="Word Game", font=("Arial", 24), bg="#1a1a2e", fg="#ffffff"
    )
    title_label.pack(pady=20)

    instruction_label = tk.Label(
        frame, text="Type the letters of the word below correctly!", font=("Arial", 14), bg="#1a1a2e", fg="#ffffff"
    )
    instruction_label.pack(pady=10)

    word_label = tk.Label(
        frame, text="_ " * len(target_word), font=("Arial", 18), bg="#0f3460", fg="#ffffff"
    )
    word_label.pack(pady=20)

    feedback_label = tk.Label(
        frame, text="", font=("Arial", 14), bg="#1a1a2e", fg="#ffffff"
    )
    feedback_label.pack(pady=10)

    def update_word_label():
        display_word = ""
        for i, letter in enumerate(target_word):
            if i < target_index:
                display_word += letter + " "
            else:
                display_word += "_ "
        word_label.config(text=display_word.strip())

    def handle_keypress(event):
        nonlocal target_index, letters_correct, target_word
        key_pressed = event.char

        if target_index < len(target_word):
            if key_pressed == target_word[target_index]:
                target_index += 1
                letters_correct += 1
                feedback_label.config(text="Correct!", fg="#48c774")
            else:
                feedback_label.config(
                    text=f"Wrong! Expected '{target_word[target_index]}'", fg="#ff3860"
                )
            update_word_label()

        if target_index == len(target_word):
            feedback_label.config(
                text="Word completed! Generating a new word.", fg="#48c774"
            )
            target_index = 0
            target_word = random.choice(word_list)
            update_word_label()

    update_word_label()

    # Back to Menu Button
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

    # Bind Key Press
    frame.bind("<KeyPress>", handle_keypress)
    frame.focus_set()
