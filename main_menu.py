import tkinter as tk
import wordgame
import Match_Game

class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Game App")
        self.geometry("800x600")
        self.configure(bg="#1a1a2e")

        # Create a main container frame
        self.container = tk.Frame(self, bg="#1a1a2e")
        self.container.pack(fill="both", expand=True)

        self.current_frame = None

        # Start with the menu
        self.show_menu()

    def show_menu(self):
        self.clear_frame()

        title = tk.Label(
            self.container, text="Welcome to the Game Menu!", font=("Arial", 18, "bold"), bg="#1a1a2e", fg="#ffffff"
        )
        title.pack(pady=20)

        word_game_button = tk.Button(
            self.container, text="Play Word Game", font=("Arial", 14), bg="#16213e", fg="#ffffff",
            activebackground="#0f3460", activeforeground="#ffffff",
            command=lambda: wordgame.start_word_game(self.container, self.show_menu)
        )
        word_game_button.pack(pady=10, ipadx=10, ipady=5)

        match_game_button = tk.Button(
            self.container, text="Play Match Game", font=("Arial", 14), bg="#16213e", fg="#ffffff",
            activebackground="#0f3460", activeforeground="#ffffff",
            command=lambda: Match_Game.start_match_game(self.container, self.show_menu)
        )
        match_game_button.pack(pady=10, ipadx=10, ipady=5)

        exit_button = tk.Button(
            self.container, text="Exit", font=("Arial", 14), bg="#900d0d", fg="#ffffff",
            activebackground="#ff0000", activeforeground="#ffffff",
            command=self.quit
        )
        exit_button.pack(pady=10, ipadx=10, ipady=5)

    def clear_frame(self):
        for widget in self.container.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = GameApp()
    app.mainloop()
