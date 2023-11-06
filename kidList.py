import tkinter as tk
from tkinter import messagebox
import random
import json
import datetime
from datetime import date
import os
import tkinter as tk
from tkinter import messagebox, PhotoImage
from PIL import Image, ImageTk


def kidList():
    givers = ['Evangeline', 'Caleb', 'Kate', 'Grace', 'Isabella', 'Sophia', 'Lana']
    receivers = [
        ['Caleb', 'Grace', 'Isabella', 'Kate', 'Sophia', 'Lana'],
        ['Evangeline', 'Grace', 'Isabella', 'Sophia', 'Lana'],
        ['Evangeline', 'Grace', 'Isabella', 'Sophia', 'Lana'],
        ['Evangeline', 'Caleb', 'Isabella', 'Kate', 'Sophia', 'Lana'],
        ['Evangeline', 'Caleb', 'Grace', 'Kate', 'Sophia', 'Lana'],
        ['Evangeline', 'Caleb', 'Grace', 'Isabella', 'Kate', 'Lana'],
        ['Evangeline', 'Caleb', 'Grace', 'Isabella', 'Kate', 'Sophia'],
    ]

    taken = []
    pairings = {}

    while len(taken) < len(givers):
        for i in range(len(givers)):
            possible = [x for x in receivers[i] if x not in taken]
            if possible:
                chosen = random.choice(possible)
                taken.append(chosen)
                pairings[givers[i]] = chosen
            else:
                taken.clear()
                pairings.clear()
                break

    # Save pairings to a file
    current_date = date.today().strftime("%d-%m-%Y")
    random_number = random.randint(1, 50000)
    filename = f'kidPollyanna_{current_date}_{random_number}.txt'
    file_path = os.path.join(os.getcwd(), filename)
    with open(file_path, 'w') as f:
        json.dump(pairings, f, indent=4)

    return pairings
