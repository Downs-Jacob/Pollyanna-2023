import tkinter as tk
from tkinter import messagebox
import os
# ... [other imports remain the same] ...

class RoundedButton(tk.Canvas):
    def __init__(self, parent, text="", command=None, **kwargs):
        tk.Canvas.__init__(self, parent, height=45, width=210, bg='white', bd=0, highlightthickness=0, relief='flat')
        self.command = command

        # Create a rounded rectangle for the border (larger)
        self.outer_rect = self.rounded_rectangle(2, 2, 208, 43, radius=20, outline='#007aff', fill='white', width=3)

        # Create a rounded rectangle for the center (smaller, white)
        self.inner_rect = self.rounded_rectangle(6, 6, 204, 39, radius=16, outline='', fill='white')

        # Add text to the button
        self.text_id = self.create_text(105, 22, text=text, fill='green', font=('Helvetica', 20))

        # Bind mouse events
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]
        return self.create_polygon(points, **kwargs, smooth=True)

    def on_press(self, event):
        self.itemconfig(self.outer_rect, fill='#0051a8')
        self.itemconfig(self.text_id, fill='white')

    def on_release(self, event):
        self.itemconfig(self.outer_rect, fill='white')
        self.itemconfig(self.text_id, fill='green')
        if self.command is not None:
            self.command()

    def on_enter(self, event):
        self.itemconfig(self.outer_rect, outline='#0051a8')

    def on_leave(self, event):
        self.itemconfig(self.outer_rect, outline='#007aff')