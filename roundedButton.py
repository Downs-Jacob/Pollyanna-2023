import tkinter as tk

class RoundedButton(tk.Canvas):
    def __init__(self, parent, text="", command=None, **kwargs):
        tk.Canvas.__init__(self, parent, height=60, width=260, bg='white', bd=0, highlightthickness=0, relief='flat')
        self.command = command

        # Create a rounded rectangle for the button background
        self.outer_rect = self.rounded_rectangle(2, 2, 208, 43, radius=20, outline='#007aff', fill='white', width=3)
        self.inner_rect = self.rounded_rectangle(6, 6, 204, 39, radius=16, outline='', fill='white')
        self.text_id = self.create_text(105, 22, text=text, fill='green', font=('Helvetica', 20))

        # Bind events to the entire canvas
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
        # Check if the cursor is still within the bounds of the button
        x, y = event.x, event.y
        if 0 <= x <= self.winfo_width() and 0 <= y <= self.winfo_height():
            if self.command is not None:
                self.command()

        # Reset button color
        self.itemconfig(self.outer_rect, fill='white')
        self.itemconfig(self.text_id, fill='green')

    def on_enter(self, event):
        self.itemconfig(self.outer_rect, outline='#0051a8')

    def on_leave(self, event):
        self.itemconfig(self.outer_rect, outline='#007aff')
