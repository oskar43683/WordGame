# LinguaPlay

A comprehensive language learning application designed to help users master Polish-English vocabulary through engaging interactive games. Built with Python and Tkinter, this desktop application offers an intuitive interface and detailed progress tracking.

## Technical Architecture

### Core Components Overview

1. **Entry Point (`main.py`)**
   - Application initialization
   - Window configuration
   - Theme setup
   - Global state management
   - Error logging configuration

2. **Login System (`login.py`)**
   ```python
   class LoginSystem:
       def __init__(self, root):
           self.root = root
           self.frame = tk.Frame(root, bg="#1a1a2e")
           self.users = self.load_users()
   ```
   - User authentication management
   - Session handling
   - Password validation
   - Registration system
   - Data persistence
   - Key methods:
     - `validate_login(username, password)`
     - `register_user(username, password)`
     - `load_users()`
     - `save_user_data(username, password)`

3. **Game Menu (`menu.py`)**
   ```python
   class GameMenu:
       def __init__(self, root, username):
           self.username = username
           self.current_score = self.load_user_score()
           self.available_levels = self.scan_levels()
   ```
   - Game selection interface
   - Level selection system
   - Score display
   - User progress tracking
   - Navigation controls
   - Key features:
     - Dynamic level loading
     - Progress persistence
     - Score management
     - Game launching

4. **Match Game (`matchgame.py`)**
   ```python
   class MatchGame:
       def __init__(self, frame, callback, level_file, username):
           self.words = self.load_words(level_file)
           self.flipped_cards = []
           self.matches_found = 0
           self.current_score = 0
   ```
   - Memory card game implementation
   - Card flipping mechanics
   - Match validation
   - Score calculation
   - Technical features:
     - Card state management
     - Animation handling
     - Event binding
     - Score tracking
   - UI Components:
     - Card grid layout
     - Score display
     - Progress indicators
     - Feedback messages

5. **Word Game (`wordgame.py`)**
   ```python
   class WordGame:
       def __init__(self, frame, callback, level_file, username):
           self.letter_entries = []
           self.current_word_index = 0
           self.words = self.load_words(level_file)
           self.setup_ui()
   ```
   - Letter-by-letter input system
   - Word validation
   - Input handling
   - Score calculation
   - Key features:
     - Multi-character support (a-z, A-Z, _, ?, ', ,)
     - Auto-focus navigation
     - Word separation visualization
     - Real-time feedback
   - Input handling:
     ```python
     def handle_key_input(self, event, current_index):
         # Enter key submission
         if event.keysym == 'Return':
             self.check_word()
             return "break"
         
         # Character validation
         valid_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_?,\'')
         if event.char in valid_chars:
             # Process input
             self.process_character(event.char, current_index)
     ```
   - Word checking:
     ```python
     def check_word(self):
         user_input = self.get_user_input()
         correct_word = self.words[self.current_word_index]['english']
         
         # Score calculation
         score = self.calculate_score(user_input, correct_word)
         self.update_score(score)
         
         # Feedback and progression
         self.show_feedback(user_input == correct_word)
         self.advance_word()
     ```

### Data Structures

1. **User Data**
   ```python
   class UserData:
       def __init__(self, username):
           self.username = username
           self.scores = {}
           self.progress = {}
           self.settings = {}
   ```
   - Properties:
     - Username (str)
     - Password hash (str)
     - Total score (int)
     - Game progress (dict)
     - Settings (dict)
   - File format (CSV):
     ```
     username,password_hash,total_score,last_played
     john_doe,hash123,1500,2024-03-20
     ```

2. **Word Pairs**
   ```python
   class WordPair:
       def __init__(self, polish, english):
           self.polish = polish
           self.english = english
           self.difficulty = self.calculate_difficulty()
   ```
   - JSON structure:
     ```json
     {
       "level_id": "1",
       "difficulty": "beginner",
       "words": [
         {
           "polish": "kot",
           "english": "cat",
           "category": "animals"
         }
       ]
     }
     ```
   - Properties:
     - Polish word/phrase
     - English translation
     - Difficulty rating
     - Category/theme
     - Usage examples

3. **Game State**
   ```python
   class GameState:
       def __init__(self):
           self.current_game = None
           self.current_level = None
           self.score = 0
           self.time_elapsed = 0
   ```
   - Active game tracking
   - Current level info
   - Score management
   - Time tracking
   - State persistence

## Getting Started

### Installation Requirements
- Python 3.x - The core programming language used
- Tkinter (built-in Python GUI library) - Handles all graphical interface elements
- Standard Python libraries:
  - json: Manages level data and word pairs storage
  - os: Handles file/directory operations
  - sys: Provides system-specific parameters and functions

### Account Setup
1. **New Users**
   - Launch the application by running `login.py`
   - Click "Register" button to open registration form
   - Create account with unique username and secure password
   - Data is stored locally in `gamedata/data.txt`
   - System verifies username availability
   - Log in with new credentials

2. **Existing Users**
   - Enter registered username and password
   - System validates credentials against stored data
   - Click "Login" to access account and game menu
   - Failed login attempts show error message

## Available Games

### Match Game
**Description**: Test your vocabulary by matching Polish and English word pairs using a memory card game interface.

**Technical Implementation**:
- Uses Tkinter Button widgets for card representation
- Implements state management for card flipping:
  ```python
  def flip_card(button, word):
      if len(flipped_cards) < 2:  # Only allow two cards flipped at once
          button.config(text=word, state='disabled')
          flipped_cards.append((button, word))
  ```
- Score tracking system:
  - 15 points per correct match
  - Points stored in user profile
  - Real-time score updates

**How to Play**:
- Select difficulty level (1-39) from scrollable menu
- Click word pairs to match them - system tracks two selections at a time
- Correct matches turn green and are disabled using button state management
- Visual feedback for correct/incorrect matches
- Option to return to main menu at any time

### Word Game (Spelling Game)
**Description**: Practice spelling English translations of Polish words with an intelligent scoring system and letter-by-letter input interface.

**Technical Implementation**:
- Individual letter entry system:
  ```python
  def create_letter_entries(word_length):
      # Creates separate entry boxes for each letter
      for i in range(word_length):
          entry = tk.Entry(
              letters_frame,
              width=2,
              justify='center'
          )
          entry.bind('<Key>', handle_key_input)
  ```
- Smart input handling:
  - Auto-focus next box on letter input
  - Backspace navigation between boxes
  - Enter key submission
  - Support for special characters (_, ?, ', ,)
- Word separation visualization using dash symbols
- Real-time input validation and scoring

**Input Features**:
- Supported characters:
  - Letters (a-z, A-Z)
  - Special characters: underscore (_), question mark (?), comma (,), apostrophe (')
- Automatic focus advancement
- Backspace navigation
- Enter key submission
- Visual word separation

**Scoring System**:
- Points awarded for each correct letter
- Bonus multiplier for perfect matches
- Score calculation:
  ```python
  word_score = sum(1 for a, b in zip(user_input, correct_word) if a == b)
  if user_input == correct_word:
      word_score += 5  # Perfect match bonus
  ```

## Technical Information

### Data Management
1. **User Profile Storage**
   - Location: `gamedata/data.txt`
   - Format: CSV structure
     ```
     username,password,points
     ```
   - File operations:
     ```python
     def save_user_data(username, password):
         with open('gamedata/data.txt', 'a') as file:
             file.write(f"{username},{password},0\n")
     ```

2. **Word Pairs Storage**
   - Location: `levels/` directory
   - Format: JSON structure
     ```json
     {
       "words": [
         {
           "polish": "kot",
           "english": "cat"
         }
       ]
     }
     ```
   - Level organization:
     - 39 difficulty levels
     - Progressive complexity
     - Themed word groups

### Game Architecture

1. **Main Components**
   - Login System (`login.py`)
   - Game Menu (`menu.py`)
   - Match Game (`matchgame.py`)
   - Word Game (`wordgame.py`)

2. **State Management**
   - User session tracking
   - Score persistence
   - Game progress monitoring
   - Error handling and recovery

3. **UI Components**
   - Consistent styling across modules
   - Responsive layout management
   - Error feedback system
   - Progress indicators

4. **Event Handling**
   ```python
   def handle_key_input(event, current_index):
       # Handle Enter key submission
       if event.keysym == 'Return':
           check_word()
           return "break"
       
       # Handle character input
       if event.char.isalpha() or event.char in ['_', '?', ',', "'"]:
           # Process input and advance focus
   ```

### Security Features
1. **User Authentication**
   - Password validation
   - Unique username enforcement
   - Session management

2. **Data Protection**
   - Secure file operations
   - Error handling for data corruption
   - Atomic write operations

### Error Handling
1. **File Operations**
   ```python
   try:
       with open(filepath, 'r') as file:
           data = file.read()
   except FileNotFoundError:
       handle_missing_file()
   except PermissionError:
       handle_permission_error()
   ```

2. **User Input Validation**
   - Character validation
   - Length checks
   - Format verification

3. **Game State Recovery**
   - Automatic save points
   - Error recovery mechanisms
   - State restoration

## Development

### Contributing Guidelines
1. **Code Style**
   - Follow PEP 8 guidelines
   - Use meaningful variable names
   - Include docstrings and comments
   - Maintain consistent indentation

2. **Testing**
   - Unit tests for core functions
   - Integration tests for game flows
   - UI/UX testing
   - Error condition testing

3. **Documentation**
   - Update README.md
   - Document new features
   - Include code examples
   - Explain technical decisions

4. **Pull Request Process**
   - Fork repository
   - Create feature branch
   - Submit detailed PR
   - Respond to review feedback
