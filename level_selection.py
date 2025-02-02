import tkinter as tk
import json
import os
import sys

def select_level(frame, callback, logged_in_username):
    # Clear the existing frame
    if frame:
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
        (0, 0), window=scrollable_frame, anchor="nw"
    )

    # Configure the Canvas scroll region
    def configure_canvas(event=None):
        if canvas:
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(scrollable_frame_id, width=canvas.winfo_width())

    scrollable_frame.bind("<Configure>", configure_canvas)
    canvas.bind("<Configure>", configure_canvas)

    # Enable mousewheel scrolling
    def on_mousewheel(event):
        try:
            canvas.yview_scroll(-1 * int(event.delta / 120), "units")
        except (tk.TclError, AttributeError):
            pass  # Ignore errors when scrolling

    canvas.bind_all("<MouseWheel>", on_mousewheel)

    # Add title
    title = tk.Label(
        scrollable_frame,
        text="Select Level",
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
            command=lambda level=level: callback(level) if callback else None,
        )
        level_button.pack(pady=5)

    # Add back to menu button at the bottom
    back_button = tk.Button(
        scrollable_frame,
        text="Back to Menu",
        font=("Arial", 14),
        bg="#16213e",
        fg="#ffffff",
        activebackground="#0f3460",
        activeforeground="#ffffff",
        command=lambda: callback("back_to_menu") if callback else None,
    )
    back_button.pack(pady=20)

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

    if not level_file:
        return []

    level_path = get_resource_path(f"levels/{level_file}")

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

if __name__ == "__main__":
    def dummy_callback(level):
        if level:
            try:
                print(f"Selected: {level}")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            print("No level selected.")

    root = tk.Tk()
    root.geometry("400x600")
    root.title("Level Selector")
    root.configure(bg="#1a1a2e")

    main_frame = tk.Frame(root, bg="#1a1a2e")
    main_frame.pack(fill="both", expand=True)

    select_level(main_frame, dummy_callback)

    root.mainloop()
