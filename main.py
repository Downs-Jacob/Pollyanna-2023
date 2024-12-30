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
            
            self.current_pairings = pairings
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
            
            self.current_pairings = pairings
            self.index = 0
            self.open_reveal_window("Adult Pollyanna Reveal")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error generating adult Pollyanna: {str(e)}")

    def open_reveal_window(self, title):
        self.reveal_window = RevealWindow(self.current_pairings, title)
        self.reveal_window.show()

class RevealWindow(QWidget):
    def __init__(self, pairings, title="Pollyanna Reveal"):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(200, 200, 600, 400)
        self.setStyleSheet("background-color: #333333;")
        
        # Create layout
        self.reveal_layout = QVBoxLayout()
        self.reveal_layout.setAlignment(Qt.AlignCenter)
        
        # Name at the top
        self.name_label = QLabel("", self)
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setStyleSheet("""
            font-size: 32px;
            margin: 10px;
            padding: 10px;
            color: white;
        """)
        
        # Create labels
        self.giver_label = QLabel("Click Next to start revealing Pollyannas", self)
        self.giver_label.setAlignment(Qt.AlignCenter)
        self.giver_label.setStyleSheet("""
            font-size: 24px;
            margin: 20px;
            padding: 20px;
            color: white;
        """)
        
        self.receiver_label = QLabel("", self)
        self.receiver_label.setAlignment(Qt.AlignCenter)
        self.receiver_label.setStyleSheet("""
            font-size: 48px;
            margin: 20px;
            padding: 20px;
            color: #4CAF50;
        """)
        
        # Create button
        self.reveal_button = QPushButton("Start", self)
        self.reveal_button.clicked.connect(self.reveal_next)
        self.reveal_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 15px 30px;
                font-size: 18px;
                border: none;
                border-radius: 5px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        # Add widgets to layout
        self.reveal_layout.addWidget(self.name_label)
        self.reveal_layout.addStretch()
        self.reveal_layout.addWidget(self.giver_label)
        self.reveal_layout.addWidget(self.receiver_label)
        self.reveal_layout.addStretch()
        self.reveal_layout.addWidget(self.reveal_button)
        self.setLayout(self.reveal_layout)
        
        # Initialize state
        self.current_pairings = pairings
        # Get the ordered list of givers
        if "Evangeline" in pairings:  # Kid list
            self.givers = ['Evangeline', 'Caleb', 'Kate', 'Grace', 'Isabella', 'Sophia', 'Lana']
        else:  # Adult list
            self.givers = ['Hannah', 'Jacob', 'Joshua', 'Mary', 'Noah', 'Jason', 'Olivia', 'Mike']
        self.index = 0
        self.reveal_state = False
        
        # Set initial name
        self.name_label.setText(self.givers[0])
        
        # Play sound
        try:
            pygame.mixer.init()
            pygame.mixer.music.load("jingle.mp3")
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Could not play sound: {str(e)}")
    
    def reveal_next(self):
        """Show the next Pollyanna pairing"""
        if not self.reveal_state:
            # Show next pairing
            giver = self.givers[self.index]
            receiver = self.current_pairings[giver]
            
            self.giver_label.setText("Your Pollyanna is:")
            self.receiver_label.setText(f"🎁 {receiver} 🎁")
            
            self.reveal_button.setText("➡️ Next")
            self.reveal_state = True
        else:
            self.index += 1
            if self.index >= len(self.givers):
                self.name_label.setText("")
                self.giver_label.setText("All Pollyannas have been revealed!")
                self.receiver_label.setText("🎉")
                self.reveal_button.setText("Close")
                self.reveal_button.clicked.disconnect()
                self.reveal_button.clicked.connect(self.close)
            else:
                self.reveal_state = False
                self.name_label.setText(self.givers[self.index])
                self.giver_label.setText("Click Next to reveal your Pollyanna")
                self.receiver_label.setText("")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PollyannaApp()
    window.show()
    sys.exit(app.exec_())
