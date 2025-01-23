# LinguaPlay

A language learning application designed to help users master Polish-English vocabulary through engaging interactive games. Built with Python and Tkinter, this desktop application offers an intuitive interface and progress tracking.

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

**How to Play**:
- Select difficulty level (1-39) from scrollable menu
- Click word pairs to match them - system tracks two selections at a time
- Correct matches turn green and are disabled using button state management
- Earn 15 points per correct match - points stored in user profile
- Track progress across levels with persistent scoring system
- Visual feedback for correct/incorrect matches
- Option to return to main menu at any time

### Word Game (Spelling Game)
**Description**: Practice spelling English translations of Polish words with an intelligent scoring system.

**How to Play**:
- Choose difficulty level from 39 available options
- System displays Polish word from level's JSON data
- Type English translation in provided entry field
- Scoring system:
  - Points awarded for each correct letter
  - Bonus multiplier for perfect matches
  - Score updates in real-time
- Immediate feedback on answer accuracy
- Progress saved automatically to user profile

## Technical Information

### Data Management
- User profiles stored in `gamedata/data.txt`
  - Format: `username,password,points` (CSV structure)
  - File created automatically if not exists
  - Secure file operations with error handling
- Word pairs organized in JSON files under `levels/`
  - Each level file contains Polish-English word pairs
  - Structured format for easy maintenance
- Automatic point tracking and saving
  - Points updated after each game
  - Thread-safe file operations
  - Error handling for data corruption

### Game Features
- Multiple difficulty levels in both games (39 levels total)
- Visual feedback system using Tkinter widgets
- Progress tracking through persistent storage
- Points-based reward system with automatic updates
- Secure user authentication with validation
- Local data persistence with error handling
- Scrollable level selection interface
- Responsive GUI with consistent styling
- Error handling for all user interactions

## Development

### Contributing Guidelines
1. Fork the repository to your GitHub account
2. Create a feature branch with descriptive name
3. Make your changes following the existing code style
4. Test thoroughly and add documentation
5. Push changes to your branch
6. Submit a detailed Pull Request with change description

Your contributions to improve the game are welcome! Please ensure code quality and documentation.

## License

This project is licensed under the MIT License - see the LICENSE file for details. The MIT License allows for free use, modification, and distribution with proper attribution.
