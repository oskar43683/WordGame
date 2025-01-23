import tkinter as tk
import json
import os
import sys

def select_word_level(frame, callback, logged_in_username):
    # Clear the existing frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Create a Canvas with a Scrollbar
    canvas = tk.Canvas(frame, bg="#1a1a2e", highlightthickness=0)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Create a Frame inside the Canvas
    scrollable_frame = tk.Frame(canvas, bg="#1a1a2e")
    scrollable_frame_id = canvas.create_window(
        (0, 0), window=scrollable_frame, anchor="nw"  # Keep top alignment
    )

    # Configure the Canvas scroll region
    def configure_canvas(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(scrollable_frame_id, width=canvas.winfo_width())

    scrollable_frame.bind("<Configure>", configure_canvas)
    canvas.bind("<Configure>", configure_canvas)

    # Enable mousewheel scrolling
    def on_mousewheel(event):
        try:
            canvas.yview_scroll(-1 * int(event.delta / 120), "units")
        except tk.TclError:
            pass  # Ignore the error when scrolling

    canvas.bind_all("<MouseWheel>", on_mousewheel)

    # Add title
    title = tk.Label(
        scrollable_frame,
        text="Select Word Game Level",
        font=("Arial", 18, "bold"),
        bg="#1a1a2e",
        fg="#ffffff"
    )
    title.pack(pady=20)

    # Add buttons for level selection
    levels = [f"{i}level.json" for i in range(1, 40)]
    for idx, level in enumerate(levels, start=1):
        level_button = tk.Button(
            scrollable_frame,
            text=f"Level {idx}",
            font=("Arial", 14),
            width=30,
            bg="#16213e",
            fg="#ffffff",
            activebackground="#0f3460",
            activeforeground="#ffffff",
            command=lambda level=level: callback(level),
        )
        level_button.pack(pady=5)

    # Add back to menu button
    back_button = tk.Button(
        scrollable_frame,
        text="Back to Menu",
        font=("Arial", 14),
        bg="#16213e",
        fg="#ffffff",
        activebackground="#0f3460",
        activeforeground="#ffffff",
        command=lambda: callback("back_to_menu"),
    )
    back_button.pack(pady=20) 