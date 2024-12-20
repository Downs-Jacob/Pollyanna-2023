import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox
)
from PyQt5.QtCore import Qt
from kidList import kidList
from adultList import adultList
import pygame  # For playing audio


class PollyannaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pollyanna 2024")
        self.setGeometry(100, 100, 800, 500)
        self.kid_pairings = []
        self.adult_pairings = []
        self.current_pairings = []
        self.index = 0
        self.reveal_state = False  # Tracks if reveal button has been clicked once

        # Initialize the music
        self.init_music()

        # Layout Setup
        self.layout = QVBoxLayout()

        # Title Label
        self.title_label = QLabel("🎁 Welcome to Pollyanna 2024 🎁", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(
            "font-size: 32px; color: #4CAF50; font-weight: bold; margin: 20px;"
        )
        self.layout.addWidget(self.title_label)

        # Subtitle
        self.subtitle_label = QLabel("Choose a group to start the Pollyanna pairing!", self)
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setStyleSheet("font-size: 16px; color: #555; margin-bottom: 20px;")
        self.layout.addWidget(self.subtitle_label)

        # Buttons for Kid and Adult Lists (Centered)
        button_layout = QHBoxLayout()  # Horizontal layout for buttons
        button_layout.setAlignment(Qt.AlignCenter)

        self.kid_button = QPushButton("🎈 Start Kid Pollyanna")
        self.kid_button.setStyleSheet(self.button_style())
        self.kid_button.setFixedWidth(200)  # Set fixed width
        self.kid_button.clicked.connect(self.start_kid_pollyanna)
        button_layout.addWidget(self.kid_button)

        self.adult_button = QPushButton("🎉 Start Adult Pollyanna")
        self.adult_button.setStyleSheet(self.button_style())
        self.adult_button.setFixedWidth(200)  # Set fixed width
        self.adult_button.clicked.connect(self.start_adult_pollyanna)
        button_layout.addWidget(self.adult_button)

        self.layout.addLayout(button_layout)  # Add the button layout to the main layout

        # Container widget
        container = QWidget()
        container.setLayout(self.layout)
        container.setStyleSheet("background-color: white;")  # Set the background to white
        self.setCentralWidget(container)

    def init_music(self):
        """Initialize and play background music."""
        pygame.mixer.init()
        music_path = os.path.join(os.path.dirname(__file__), "songs", "lookLikeChristmas.mp3")
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)  # Loop indefinitely
        else:
            print(f"Music file not found: {music_path}")

    def button_style(self):
        """Styling for buttons."""
        return (
            "background-color: #2196F3; color: white; font-size: 16px; font-weight: bold;"
            "border: none; border-radius: 8px; padding: 10px; margin: 10px;"
            "hover: { background-color: #1976D2; }"
        )

    def start_kid_pollyanna(self):
        self.kid_pairings = list(kidList().items())
        if not self.kid_pairings:
            QMessageBox.critical(self, "Error", "No valid kid Pollyanna pairings could be generated.")
        else:
            self.current_pairings = self.kid_pairings
            self.index = 0
            self.open_reveal_window("Kid Pollyanna Reveal")

    def start_adult_pollyanna(self):
        self.adult_pairings = list(adultList().items())
        if not self.adult_pairings:
            QMessageBox.critical(self, "Error", "No valid adult Pollyanna pairings could be generated.")
        else:
            self.current_pairings = self.adult_pairings
            self.index = 0
            self.open_reveal_window("Adult Pollyanna Reveal")

    def open_reveal_window(self, title):
        """Open a new window for reveals."""
        self.reveal_window = QWidget()
        self.reveal_window.setWindowTitle(title)
        self.reveal_window.setGeometry(200, 200, 600, 300)

        self.reveal_layout = QVBoxLayout()

        # Reveal label
        self.reveal_label = QLabel("", self.reveal_window)
        self.reveal_label.setAlignment(Qt.AlignCenter)
        self.reveal_label.setStyleSheet("font-size: 18px; margin-bottom: 20px; color: #333;")
        self.reveal_layout.addWidget(self.reveal_label)

        # Reveal button
        self.reveal_button = QPushButton("🔍 Click to Reveal Pollyanna", self.reveal_window)
        self.reveal_button.setStyleSheet(self.button_style())
        self.reveal_button.setFixedWidth(200)  # Set fixed width for consistency
        self.reveal_button.clicked.connect(self.handle_reveal_click)
        self.reveal_layout.addWidget(self.reveal_button, alignment=Qt.AlignCenter)

        self.reveal_window.setLayout(self.reveal_layout)
        self.reveal_window.setStyleSheet("background-color: white;")  # Set the background to white
        self.reveal_state = False  # Reset reveal state
        self.show_current_giver()

        self.reveal_window.show()

    def show_current_giver(self):
        """Display the current giver."""
        if self.index < len(self.current_pairings):
            giver, _ = self.current_pairings[self.index]
            self.reveal_label.setText(f"{giver}, click below to reveal your Pollyanna!")
        else:
            self.reveal_label.setText("🎉 All Pollyanna pairings have been revealed!")
            self.reveal_button.setEnabled(False)

    def handle_reveal_click(self):
        """Handle button click for reveal and next."""
        if not self.reveal_state:  # First click reveals the Pollyanna
            giver, receiver = self.current_pairings[self.index]
            self.reveal_label.setText(f"{giver}, your Pollyanna is: 🎁 <span style='color: green;'>{receiver}</span> 🎁")
            self.reveal_button.setText("➡️ Next")
            self.reveal_state = True
        else:  # Second click moves to the next participant
            self.index += 1
            self.reveal_state = False
            self.reveal_button.setText("🔍 Click to Reveal Pollyanna")
            self.show_current_giver()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PollyannaApp()
    window.show()
    sys.exit(app.exec_())
