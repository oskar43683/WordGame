#login.py file
#...
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
#...
class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Game App")
        self.geometry("1200x700")
        self.configure(bg="#1a1a2e")

        # Create a main container frame
        self.container = tk.Frame(self, bg="#1a1a2e")
        self.container.pack(fill="both", expand=True)

        self.current_frame = None
        self.logged_in_username = None

        # Start with the login screen
        self.show_login()
#...
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
#...
    def show_login(self):
        self.clear_frame()
        #...
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
        #...
    #...
    def show_menu(self):
        self.clear_frame()
        #...
        match_game_button = tk.Button(
            self.container, 
            text="Play Match Game", 
            font=("Arial", 14), 
            bg="#16213e", fg="#ffffff",
            activebackground="#0f3460", activeforeground="#ffffff",
            command=lambda: level_selection.select_level(self.container, self.start_match_game, self.logged_in_username)
        )
        match_game_button.pack(pady=10, ipadx=10, ipady=5)
        #...
    #...
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
    #...
    def start_match_game(self, selected_level_file):
        points = self.get_points()
        Match_Game.start_match_game(self.container, self.show_menu, selected_level_file, self.logged_in_username, points)
    #...
#another file where i need to transfer points from logged in username - Match_Game.py
def start_match_game(frame, go_back_callback, level_file, username, points):

#level_selection.py file

def select_level(frame, callback, logged_in_username):
    # Clear the existing frame
    for widget in frame.winfo_children():
        widget.destroy()

    #...
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
        #...
    back_button = tk.Button(
    frame,
    text="Back",
    font=("Arial", 14),
    bg="#16213e",
    fg="#ffffff",
    activebackground="#0f3460",
    activeforeground="#ffffff",
    command=go_back_callback
    )
    back_button.pack(pady=10)
#...









#part 2

#Match_Game.py
def start_match_game(frame, go_back_callback, level_file, username, points):
    for widget in frame.winfo_children():
        widget.destroy()
        