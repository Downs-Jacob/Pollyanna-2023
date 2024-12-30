import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox
)
from PyQt5.QtCore import Qt
from kidList import kidList
from adultList import adultList
import pygame

class PollyannaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_year = datetime.now().year
        self.setWindowTitle(f"Pollyanna {self.current_year}")
        self.setGeometry(100, 100, 800, 500)
        self.kid_pairings = []
        self.adult_pairings = []
        self.current_pairings = []
        self.index = 0
        self.reveal_state = False

        # Initialize the music
        try:
            self.init_music()
        except Exception as e:
            print(f"Error initializing music: {str(e)}")

        # Layout Setup
        self.layout = QVBoxLayout()

        # Title Label
        self.title_label = QLabel(f"🎁 Welcome to Pollyanna {self.current_year} 🎁", self)
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

        # Buttons Layout
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)

        self.kid_button = QPushButton("🎈 Start Kid Pollyanna")
        self.kid_button.setStyleSheet(self.button_style())
        self.kid_button.setFixedWidth(200)
        self.kid_button.clicked.connect(self.start_kid_pollyanna)
        button_layout.addWidget(self.kid_button)

        self.adult_button = QPushButton("🎉 Start Adult Pollyanna")
        self.adult_button.setStyleSheet(self.button_style())
        self.adult_button.setFixedWidth(200)
        self.adult_button.clicked.connect(self.start_adult_pollyanna)
        button_layout.addWidget(self.adult_button)

        self.layout.addLayout(button_layout)

        # Container widget
        container = QWidget()
        container.setLayout(self.layout)
        container.setStyleSheet("background-color: white;")
        self.setCentralWidget(container)

    def init_music(self):
        pygame.mixer.init()
        music_path = os.path.join(os.path.dirname(__file__), "songs", "lookLikeChristmas.mp3")
        if os.path.exists(music_path):
            try:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.play(-1)
            except pygame.error as e:
                print(f"Error playing music: {str(e)}")
        else:
            print(f"Music file not found: {music_path}")

    def button_style(self):
        return """
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                padding: 10px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #BDBDBD;
            }
        """

    def start_kid_pollyanna(self):
        try:
            pairings = kidList()
            if not pairings:
                QMessageBox.critical(self, "Error", "No valid kid Pollyanna pairings could be generated.")
                return
            
            self.kid_pairings = list(pairings.items())
            self.current_pairings = self.kid_pairings
            self.index = 0
            self.open_reveal_window("Kid Pollyanna Reveal")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error generating kid Pollyanna: {str(e)}")

    def start_adult_pollyanna(self):
        try:
            pairings = adultList()
            if not pairings:
                QMessageBox.critical(self, "Error", "No valid adult Pollyanna pairings could be generated.")
                return
            
            self.adult_pairings = list(pairings.items())
            self.current_pairings = self.adult_pairings
            self.index = 0
            self.open_reveal_window("Adult Pollyanna Reveal")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error generating adult Pollyanna: {str(e)}")

    def open_reveal_window(self, title):
        self.reveal_window = QWidget()
        self.reveal_window.setWindowTitle(title)
        self.reveal_window.setGeometry(200, 200, 600, 300)

        self.reveal_layout = QVBoxLayout()

        # Reveal label with improved styling
        self.reveal_label = QLabel("", self.reveal_window)
        self.reveal_label.setAlignment(Qt.AlignCenter)
        self.reveal_label.setStyleSheet("""
            font-size: 24px;
            margin: 20px;
            padding: 20px;
            color: #333;
            background-color: #f5f5f5;
            border-radius: 10px;
        """)
        self.reveal_layout.addWidget(self.reveal_label)

        # Progress indicator
        self.progress_label = QLabel("", self.reveal_window)
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.progress_label.setStyleSheet("font-size: 14px; color: #666;")
        self.reveal_layout.addWidget(self.progress_label)

        # Reveal button
        self.reveal_button = QPushButton("🔍 Click to Reveal Pollyanna", self.reveal_window)
        self.reveal_button.setStyleSheet(self.button_style())
        self.reveal_button.setFixedWidth(250)
        self.reveal_button.clicked.connect(self.handle_reveal_click)
        self.reveal_layout.addWidget(self.reveal_button, alignment=Qt.AlignCenter)

        self.reveal_window.setLayout(self.reveal_layout)
        self.reveal_window.setStyleSheet("background-color: white;")
        self.reveal_state = False
        self.show_current_giver()

        self.reveal_window.show()

    def show_current_giver(self):
        if self.index < len(self.current_pairings):
            giver, _ = self.current_pairings[self.index]
            self.reveal_label.setText(f"{giver}, click below to reveal your Pollyanna!")
            self.progress_label.setText(f"Pairing {self.index + 1} of {len(self.current_pairings)}")
        else:
            self.reveal_label.setText("🎉 All Pollyanna pairings have been revealed! 🎉")
            self.progress_label.setText("Complete!")
            self.reveal_button.setEnabled(False)

    def handle_reveal_click(self):
        if not self.reveal_state:
            giver, receiver = self.current_pairings[self.index]
            self.reveal_label.setText(
                f"{giver}, your Pollyanna is:\n"
                f"🎁 <span style='color: #4CAF50; font-size: 28px;'>{receiver}</span> 🎁"
            )
            self.reveal_button.setText("➡️ Next")
            self.reveal_state = True
        else:
            self.index += 1
            self.reveal_state = False
            self.reveal_button.setText("🔍 Click to Reveal Pollyanna")
            self.show_current_giver()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PollyannaApp()
    window.show()
    sys.exit(app.exec_())
