import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import pygame
from kidList import kidList
from adultList import adultList
from roundedButton import RoundedButton

#######################################
# Helper Functions
#######################################

def center_window(win, width=200, height=150):
    """Center a window on the screen."""
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    win.geometry(f'{width}x{height}+{x}+{y}')

def show_next_reveal(pairings, index=0):
    """Iterate through pairings to display reveals."""
    if index < len(pairings):
        giver, receiver = list(pairings.items())[index]
        show_reveal_window(giver, receiver, pairings, index)

def show_reveal_window(giver, receiver, pairings, index):
    """Display a reveal window for a Pollyanna pairing."""
    reveal_window = tk.Toplevel()
    reveal_window.title("Pollyanna Reveal")
    center_window(reveal_window, 350, 150)

    tk.Label(reveal_window, text=f"{giver}, click to reveal your Pollyanna").pack(pady=10)

    def reveal():
        reveal_button.pack_forget()
        tk.Label(reveal_window, text=f"Your Pollyanna is: {receiver}", foreground="#58e089").pack(pady=10)
        next_button.pack(pady=10)

    reveal_button = tk.Button(reveal_window, text="Reveal Pollyanna", command=reveal)
    reveal_button.pack(pady=10)

    def close_and_next():
        reveal_window.destroy()
        show_next_reveal(pairings, index + 1)

    next_button = tk.Button(reveal_window, text="Next", command=close_and_next)

def call_kid_list():
    """Generate and show kid Pollyanna list."""
    pairings = kidList()
    if not pairings:
        messagebox.showerror("Error", "Could not generate a valid Pollyanna list.")
    else:
        show_next_reveal(pairings)

def call_adult_list():
    """Generate and show adult Pollyanna list."""
    pairings = adultList()
    if not pairings:
        messagebox.showerror("Error", "Could not generate a valid Pollyanna list.")
    else:
        show_next_reveal(pairings)

#######################################
# Song Playlist Handling
#######################################

def play_next_song():
    """Play the next song in the playlist."""
    global current_song
    if not pygame.mixer.music.get_busy() and playlist:
        try:
            pygame.mixer.music.load(os.path.join('songs', playlist[current_song]))
            pygame.mixer.music.play()
            current_song = (current_song + 1) % len(playlist)
        except pygame.error as e:
            print(f"Error playing song: {e}")
    root.after(1000, play_next_song)

#######################################
# Main UI Setup
#######################################

root = tk.Tk()
root.title("Pollyanna List")
center_window(root, 700, 700)
root.configure(bg='white')

# ASCII Art Label
ascii_art = "POLLYANNA 2024"
tk.Label(
    root, text=ascii_art, font=('Helvetica', 28, 'bold'), fg="#dd3024", bg='white', justify=tk.CENTER
).pack(pady=(30, 20))

# Button Frame
button_frame = tk.Frame(root, bg='#f7f7f7')
button_frame.pack(pady=20)

btn_kid_list = RoundedButton(button_frame, text="Start Kid Pollyanna", command=call_kid_list)
btn_kid_list.pack(side='left', padx=10)

btn_adult_list = RoundedButton(button_frame, text="Start Adult Pollyanna", command=call_adult_list)
btn_adult_list.pack(side='right', padx=10)

# Santa Image
try:
    santa_img = Image.open(os.path.join('images', 'santa.png'))
    small_santa_img = santa_img.resize((santa_img.width // 2, santa_img.height // 2))
    santa_photo = ImageTk.PhotoImage(small_santa_img)
    santa_label = tk.Label(root, image=santa_photo, bg='#f7f7f7')
    santa_label.pack(pady=(0, 20))
    root.santa_photo = santa_photo  # Prevent garbage collection
except FileNotFoundError:
    print("Santa image not found. Skipping image display.")

# Initialize Pygame Mixer
pygame.mixer.init()
playlist = ['lookLikeChristmas.mp3', 'march.mp3', 'white.mp3']
current_song = 0

#######################################
# Start the Application
#######################################

if __name__ == "__main__":
    play_next_song()
    root.mainloop()
