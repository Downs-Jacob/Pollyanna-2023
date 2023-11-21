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
from emailLogic import send_email


def adultList():
    givers = ['Hannah','Jacob','Josh','Mary','Noah', 'Jason', 'Olivia', 'Mike']
    receivers = [
        ['Jacob','Josh','Mary', 'Noah', 'Jason', 'Olivia', 'Mike'],###### Hannah
        ['Hannah','Josh','Noah', 'Jason', 'Olivia', 'Mike'],############# Jacob
        ['Hannah','Jacob','Mary','Noah', 'Jason', 'Olivia', 'Mike'],##### Josh
        ['Hannah','Jacob','Josh', 'Jason', 'Olivia', 'Mike'],############ Mary
        ['Hannah','Jacob','Josh', 'Jason', 'Olivia', 'Mike'],############ Noah
        ['Hannah','Jacob','Josh', 'Mary','Noah', 'Olivia', 'Mike'],###### Jason
        ['Hannah','Jacob','Josh', 'Mary','Noah', 'Jason'],############### Olivia
        ['Hannah','Jacob','Josh', 'Mary','Noah', 'Jason'],############### Mike
    ]
    taken = []
    pairings = {}
    
    start = random.choice(receivers[0])
    taken.append(start)
    pairings[givers[0]] = start

    while len(taken) < len(givers):
        for i in range(1, len(givers)):
            possible = [x for x in receivers[i] if x not in taken]
            if possible:
                chosen = random.choice(possible)
                taken.append(chosen)
                pairings[givers[i]] = chosen
            else:
                taken = [start]
                pairings = {givers[0]: start}
                break

    # Save the pairings to a file
    current_date = date.today().strftime("%d-%m-%Y")
    random_number = random.randint(1, 50000)
    filename = f'adultPollyanna_{current_date}_{random_number}.txt'
    file_path = os.path.join(os.getcwd(), filename)
    with open(file_path, 'w') as f:
        json.dump(pairings, f, indent=4)

    send_email("Pollyanna 2023", "Attached is the adult list for the 2023 Pollyanna", "tua04072@gmail.com", file_path)
    #downs1973@comcast.net
    return pairings