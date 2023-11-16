import tkinter as tk
from tkinter import messagebox
import os
from kidList import kidList
from roundedButton import RoundedButton
from adultList import adultList
from PIL import Image, ImageTk
import pygame

#######################################
# functions
#######################################

def center_window(win, width=200, height=150):
    # Get the screen width and height
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    # Calculate position x, y
    x = (screen_width // 6) - (width // 6)
    y = (screen_height // 6) - (height // 6)
    win.geometry(f'{width}x{height}+{x}+{y}')

def show_next_reveal(pairings, index=0):
    if index < len(pairings):
        giver, receiver = list(pairings.items())[index]
        show_reveal_window(giver, receiver, pairings, index)

def show_reveal_window(giver, receiver, pairings, index):
    # The function body remains the same as before
    pass

def call_kid_list():
    pairings = kidList()
    if not pairings:
        messagebox.showerror("Error", "Could not generate a valid Pollyanna list.")
        return
    show_next_reveal(pairings)

def call_adult_list():
    pairings = adultList()
    if not pairings:
        messagebox.showerror("Error", "Could not generate a valid Pollyanna list.")
        return
    show_next_reveal(pairings)

def show_reveal_window(giver, receiver, pairings, index):
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

#######################################
# Build and manage UI
#######################################

root = tk.Tk()
root.title("Pollyanna List")

# Center the main window before showing it
center_window(root, 700, 700)

# Set a background color
root.configure(bg='white')

# ASCII art label for "POLLYANNA 2023"
ascii_art = "POLLYANNA 2023"

# Display ASCII art in a label with larger, bold font and more styling
lbl_art = tk.Label(root, text=ascii_art, font=('Helvetica', 28, 'bold'), fg="#dd3024", bg='white', justify=tk.CENTER)
lbl_art.pack(pady=(30, 20))

button_style = {
    'font': ('Helvetica', 20),
    'bg': '#007aff',  
    'fg': 'green',
    'activebackground': '#0051a8',
    'activeforeground': 'white',
    'borderwidth': '1',
    'highlightthickness': '1',
    'highlightcolor': '#0051a8',
    'highlightbackground': '#007aff',
    'padx': 10,
    'pady': 10
}
# Frame for buttons
button_frame = tk.Frame(root, bg='#f7f7f7')
button_frame.pack(pady=20)

btn_kid_list = RoundedButton(button_frame, text="Start Kid Pollyanna", command=call_kid_list)
btn_kid_list.pack(side='left', padx=10)

adult_button = RoundedButton(button_frame, text='Start Adult Pollyanna', command=call_adult_list)
adult_button.pack(side='right', padx=10)

# Load Santa image with Pillow
santa_image_path = os.path.join('images', 'santa.png')  
santa_img = Image.open(santa_image_path)
width, height = santa_img.size
new_size = (int(width * 0.5), int(height * 0.5))

# Resize the image
small_santa_img = santa_img.resize(new_size)

# Convert to a format Tkinter can use
santa_photo = ImageTk.PhotoImage(small_santa_img)

# Keep a reference to the image object to prevent garbage collection
root.santa_photo = santa_photo  # This line retains a reference to the image

# Label that displays the image
santa_label = tk.Label(root, image=root.santa_photo, bg='#f7f7f7')
santa_label.pack(pady=(0, 20))

# Initialize the pygame mixer
pygame.mixer.init()

# Define a list of songs
playlist = [
    'lookLikeChristmas.mp3',
    'march.mp3',
    'white.mp3'
]
current_song = 0

# Function to play the next song
def play_next_song():
    global current_song
    if not pygame.mixer.music.get_busy():
        if current_song < len(playlist):
            pygame.mixer.music.load(os.path.join('songs', playlist[current_song]))
            pygame.mixer.music.play()
            current_song += 1
        else:
            print("No more songs in the playlist.")
    root.after(1000, play_next_song)  # Check every 1000ms (1 second)


# Run the main loop
if __name__ == "__main__":
    play_next_song()
    root.mainloop()
