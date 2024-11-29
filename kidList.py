import random
import json
from datetime import date
import os
from emailLogic import send_email
import threading  # For threading email sending

def kidList():
    givers = ['Evangeline', 'Caleb', 'Kate', 'Grace', 'Isabella', 'Sophia', 'Lana']
    receivers = [
        ['Caleb', 'Grace', 'Isabella', 'Kate', 'Sophia', 'Lana'],        # Evangeline
        ['Evangeline', 'Grace', 'Isabella', 'Sophia', 'Lana'],           # Caleb 
        ['Evangeline', 'Grace', 'Isabella', 'Sophia', 'Lana'],           # Kate
        ['Evangeline', 'Caleb', 'Isabella', 'Kate', 'Sophia', 'Lana'],   # Grace
        ['Evangeline', 'Caleb', 'Grace', 'Kate', 'Sophia', 'Lana'],      # Isabella
        ['Evangeline', 'Caleb', 'Grace', 'Isabella', 'Kate', 'Lana'],    # Sophia
        ['Evangeline', 'Caleb', 'Grace', 'Isabella', 'Kate', 'Sophia'],  # Lana
    ]

    attempts = 0
    while True:
        attempts += 1
        # Shuffle receivers for random pairing
        shuffled_receivers = [random.sample(receivers[i], len(receivers[i])) for i in range(len(receivers))]
        pairings = {}
        taken = set()

        valid = True
        for i, giver in enumerate(givers):
            # Find a valid match for the current giver
            match = next((r for r in shuffled_receivers[i] if r not in taken), None)
            if match:
                pairings[giver] = match
                taken.add(match)
            else:
                valid = False
                break

        if valid:
            print(f"Pairing succeeded after {attempts} attempt(s).")
            break

    # Save pairings to a file
    current_date = date.today().strftime("%d-%m-%Y")
    random_number = random.randint(1, 50000)
    filename = f'kidPollyanna_{current_date}_{random_number}.txt'
    file_path = os.path.join(os.getcwd(), filename)

    with open(file_path, 'w') as f:
        json.dump(pairings, f, indent=4)

    #######################################
    # emails in a separate thread
    #######################################

    def send_email_in_thread():
        send_email(
            "Pollyanna 2024 - Kid List",
            "Attached to this email is the kid list for the 2024 Pollyanna.",
            "moomama96@gmail.com",
            #moomama96@gmail.com
            file_path
        )

    email_thread = threading.Thread(target=send_email_in_thread)
    email_thread.start()

    print("Cousin List Generated")
    return pairings
