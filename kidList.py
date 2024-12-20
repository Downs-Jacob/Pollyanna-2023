import random
import json
from datetime import date
import os
from emailLogic import send_email
import threading  # For threading email sending


def kidList():
    """Generate Pollyanna pairings for kids."""
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
        pairings = {}
        taken = set()

        valid = True
        for i, giver in enumerate(givers):
            # Find a match not already taken
            available = [r for r in receivers[i] if r not in taken]
            if available:
                match = random.choice(available)
                pairings[giver] = match
                taken.add(match)
            else:
                valid = False
                break

        if valid:
            print(f"Pairing succeeded after {attempts} attempt(s).")
            break

    # Save pairings to a file
    current_date = date.today().strftime("%Y-%m-%d")
    filename = f'kidPollyanna_{current_date}.json'
    file_path = os.path.join(os.getcwd(), filename)

    with open(file_path, 'w') as f:
        json.dump(pairings, f, indent=4)

    print(f"Kid Pollyanna pairings saved to {filename}.")

    #######################################
    # Send email in a separate thread
    #######################################
    def send_email_in_thread():
        send_email(
            "Pollyanna 2024 - Kid List",
            "Attached is the kid list for the 2024 Pollyanna.",
            "tua04072@gmail.com",  # Replace with the recipient's email address
            file_path
        )

    email_thread = threading.Thread(target=send_email_in_thread)
    email_thread.start()

    return pairings
