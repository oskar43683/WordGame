import tkinter as tk
import level_selection
import Match_Game
import wordgame
from PIL import Image, ImageTk  # To handle the background image


def VerifyLogin(username, password, file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                fields = line.strip().split(",")
                if len(fields) >= 2 and fields[0] == username and fields[1] == password:
                    return True
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
    except Exception as e:
        print(f"Error: {e}")
    return False

def VerifyUsername(username, filepath):
    try:
        with open(filepath, 'r') as file:
            lines = file.readlines()
            for line in lines:
                fields = line.split(",")
                if fields[0] == username:
                    return True
    except Exception as e:
        print(f"Error: {e}")
    return False

class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LinguaPlay")
        self.geometry("1200x700")
        self.configure(bg="#1a1a2e")

        # Create a main container frame
        self.container = tk.Frame(self, bg="#1a1a2e")
        self.container.pack(fill="both", expand=True)

        self.current_frame = None
        self.logged_in_username = None

        # Start with the login screen
        self.show_login()

    def show_login(self):
        self.clear_frame()

        title = tk.Label(
            self.container, 
            text="Language Learning Game", 
            font=("Arial", 18, "bold"), 
            bg="#1a1a2e", 
            fg="#ffffff"
        )
        title.pack(pady=20)

        bg_image = Image.open("game/ocean.png")
        bg_photo = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(self.container, image=bg_photo)
        bg_label.image = bg_photo  # Keep a reference to avoid garbage collection
        bg_label.place(relwidth=1, relheight=1)  # Cover the entire frame

        username_label = tk.Label(
            self.container,
            text="Username: ",
            font=("Arial", 14),
            bg="#1a1a2e", 
            fg="#ffffff"
        )
        username_label.pack(pady=10)
        username_entry = tk.Entry(
            self.container,
            font=("Arial", 14),
            width=30
        )
        username_entry.pack(pady=10, ipadx=5, ipady=5)

        password_label = tk.Label(
            self.container,
            text="Password: ",
            font=("Arial", 14),
            bg="#1a1a2e", 
            fg="#ffffff"
        )
        password_label.pack(pady=10)
        password_entry = tk.Entry(
            self.container, 
            font=("Arial", 14), 
            width=30, 
            show="*"
        )
        password_entry.pack(pady=10, ipadx=5, ipady=5)

        def check_login():
            username = username_entry.get()
            password = password_entry.get()
            if VerifyLogin(username, password, "data.txt"):
                self.logged_in_username = username  # Store the logged-in user
                self.show_menu()
            else:
                error_label = tk.Label(
                    self.container,
                    text="Invalid login credentials, please try again.",
                    font=("Arial", 12),
                    bg="#1a1a2e",
                    fg="#ff0000"
                )
                error_label.pack(pady=10)

        login_button = tk.Button(
            self.container, 
            text="Login", 
            font=("Arial", 14), 
            bg="#16213e", fg="#ffffff",
            activebackground="#0f3460", activeforeground="#ffffff",
            command=check_login
        )
        login_button.pack(pady=10, ipadx=10, ipady=5)

        register_button = tk.Button(
            self.container, 
            text="Register", 
            font=("Arial", 14), 
            bg="#16213e", fg="#ffffff",
            activebackground="#0f3460", activeforeground="#ffffff",
            command=self.show_registration
        )
        register_button.pack(pady=10, ipadx=10, ipady=5)

        # nolog_button = tk.Button(
        #     self.container, 
        #     text="Enter without login", 
        #     font=("Arial", 14), 
        #     bg="#16213e", fg="#ffffff",
        #     activebackground="#0f3460", activeforeground="#ffffff",
        #     command=self.show_menu
        # )
        # nolog_button.pack(pady=10, ipadx=10, ipady=5)

        exit_button = tk.Button(
            self.container, 
            text="Exit", 
            font=("Arial", 14), 
            bg="#900d0d", fg="#ffffff",
            activebackground="#ff0000", activeforeground="#ffffff",
            command=self.quit
        )
        exit_button.pack(pady=10, ipadx=10, ipady=5)

    def show_registration(self):
        self.clear_frame()

        title = tk.Label(
            self.container,
            text="Register New Account",
            font=("Arial", 18, "bold"),
            bg="#1a1a2e",
            fg="#ffffff"
        )
        title.pack(pady=20)

        username_label = tk.Label(
            self.container,
            text="Username: ",
            font=("Arial", 14),
            bg="#1a1a2e",
            fg="#ffffff"
        )
        username_label.pack(pady=10)
        username_entry = tk.Entry(
            self.container,
            font=("Arial", 14),
            width=30
        )
        username_entry.pack(pady=10, ipadx=5, ipady=5)

        password_label = tk.Label(
            self.container,
            text="Password: ",
            font=("Arial", 14),
            bg="#1a1a2e",
            fg="#ffffff"
        )
        password_label.pack(pady=10)
        password_entry = tk.Entry(
            self.container,
            font=("Arial", 14),
            width=30,
            show="*"
        )
        password_entry.pack(pady=10, ipadx=5, ipady=5)

        def register():
            username = username_entry.get()
            password = password_entry.get()
            if not VerifyUsername(username, "data.txt"):
                if username and password:
                    try:
                        with open("data.txt", "a") as file:
                            file.write(f"{username},{password},0\n")
                        self.show_login()
                    except Exception as e:
                        error_label = tk.Label(
                            self.container,
                            text=f"Error: {e}",
                            font=("Arial", 12),
                            bg="#1a1a2e",
                            fg="#ff0000"
                        )
                        error_label.pack(pady=10)
                else:
                    error_label = tk.Label(
                            self.container,
                            text="Please fill in all fields.",
                            font=("Arial", 12),
                            bg="#1a1a2e",
                            fg="#ff0000"
                        )
                    error_label.pack(pady=10)
            else:
                error_label = tk.Label(
                    self.container,
                    text="User already exists. Please try a different username.",
                    font=("Arial", 12),
                    bg="#1a1a2e",
                    fg="#ff0000"
                )
                error_label.pack(pady=10)

        register_button = tk.Button(
            self.container,
            text="Register",
            font=("Arial", 14),
            bg="#16213e",
            fg="#ffffff",
            activebackground="#0f3460",
            activeforeground="#ffffff",
            command=register
        )
        register_button.pack(pady=10, ipadx=10, ipady=5)

        back_button = tk.Button(
            self.container,
            text="Back to login",
            font=("Arial", 14),
            bg="#16213e",
            fg="#ffffff",
            activebackground="#0f3460",
            activeforeground="#ffffff",
            command=self.show_login
        )
        back_button.pack(pady=10, ipadx=10, ipady=5)

    def show_menu(self):
        self.clear_frame()

        title = tk.Label(
            self.container, 
            text="LinguaPlay", 
            font=("Arial", 18, "bold"), 
            bg="#1a1a2e", 
            fg="#ffffff"
        )
        title.pack(pady=20)

        if self.logged_in_username:
            points = self.get_points()
            points_label = tk.Label(
                self.container,
                text=f"Points: {points}",
                font=("Arial", 14),
                bg="#1a1a2e",
                fg="#ffffff"
            )
            points_label.pack(pady=10)

        word_game_button = tk.Button(
            self.container, 
            text="Play Word Game", 
            font=("Arial", 14), 
            bg="#16213e", fg="#ffffff",
            activebackground="#0f3460", activeforeground="#ffffff",
            command=lambda: wordgame.start_word_game(self.container, self.show_menu)
        )
        word_game_button.pack(pady=10, ipadx=10, ipady=5)

        match_game_button = tk.Button(
            self.container, 
            text="Play Match Game", 
            font=("Arial", 14), 
            bg="#16213e", fg="#ffffff",
            activebackground="#0f3460", activeforeground="#ffffff",
            command=lambda: level_selection.select_level(self.container, self.start_match_game, self.logged_in_username)
        )
        match_game_button.pack(pady=10, ipadx=10, ipady=5)

        exit_button = tk.Button(
            self.container, 
            text="Exit", 
            font=("Arial", 14), 
            bg="#900d0d", fg="#ffffff",
            activebackground="#ff0000", activeforeground="#ffffff",
            command=self.quit
        )
        exit_button.pack(pady=10, ipadx=10, ipady=5)

        exit_to_login_button = tk.Button(
            self.container, 
            text="Log out", 
            font=("Arial", 14), 
            bg="#900d0d", fg="#ffffff",
            activebackground="#ff0000", activeforeground="#ffffff",
            command=self.show_login
        )
        exit_to_login_button.pack(pady=10, ipadx=10, ipady=5)

        future_updates_label = tk.Label(
            self.container,
            text="We are also in the process of creating new game modes...",
            font=("Arial", 14),
            bg="#1a1a2e",
            fg="#ffffff"
        )
        future_updates_label.pack(pady=20)


    def get_points(self):
        try:
            with open("data.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    fields = line.strip().split(",")
                    if fields[0] == self.logged_in_username:
                        return int(fields[2])  # Return the points
        except Exception as e:
            print(f"Error: {e}")
        return 0  # Default to 0 if not found

    def clear_frame(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def start_match_game(self, selected_level_file):
        points = self.get_points()
        Match_Game.start_match_game(self.container, self.show_menu, selected_level_file, self.logged_in_username, points)

if __name__ == "__main__":
    app = GameApp()
    app.mainloop()
