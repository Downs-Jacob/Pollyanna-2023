# Pollyanna Generator 2023 🎁

A Python application that generates and manages Pollyanna (Secret Santa) pairings for both kids and adults, with a user-friendly GUI interface.

## Features

- **Separate Kid and Adult Pairings**: Manages two distinct Pollyanna groups
- **Smart Pairing Logic**: Ensures valid combinations based on predefined rules
- **Graphical User Interface**: Easy-to-use PyQt5-based interface
- **Email Notifications**: Sends pairing information to participants
- **Sound Effects**: Adds festive audio feedback
- **Automatic File Generation**: Creates JSON files with date-stamped pairings

## Requirements

- Python 3.9+
- PyQt5
- pygame (for audio)
- Internet connection (for email functionality)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Downs-Jacob/Pollyanna-2023.git
cd Pollyanna-2023
```

2. Install required packages:
```bash
pip install PyQt5 pygame
```

## Usage

Run the main application:
```bash
python main.py
```

This will open the GUI where you can:
1. Click "Start Kid Pollyanna" to generate kid pairings
2. Click "Start Adult Pollyanna" to generate adult pairings

Generated pairings are saved in JSON files with the current date.

## Testing

Run the test suite:
```bash
python -m unittest test_pollyanna.py -v
```

The test suite includes:
- Validation of kid and adult pairing generation
- File creation verification
- UI component testing
- Combination analysis

## Pairing Rules

### Kids
- Valid receivers are predefined for each kid
- No one can get themselves
- Each kid must give and receive exactly one gift

### Adults
- Similar rules apply with different valid receiver combinations
- Family members have specific restrictions

## Technical Details

- Uses randomization with maximum attempts to prevent infinite loops
- Generates approximately 1,280 possible valid kid combinations
- Maintains fair distribution of pairings (e.g., 15% chance for any specific valid pairing)
- Includes comprehensive error handling and user feedback

## File Structure

- `main.py`: Main application and GUI
- `kidList.py`: Kid Pollyanna generation logic
- `adultList.py`: Adult Pollyanna generation logic
- `test_pollyanna.py`: Test suite
- Generated files: `kidPollyanna_YYYY-MM-DD.json`, `adultPollyanna_YYYY-MM-DD.json`

## Contributing

Feel free to submit issues and enhancement requests!
