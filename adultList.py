import random
import json
from datetime import date
import os
from emailLogic import send_email
import threading  # For threading email sending

def adultList():
    """Generate Pollyanna pairings for adults."""
    givers = ['Hannah', 'Jacob', 'Joshua', 'Mary', 'Noah', 'Jason', 'Olivia', 'Mike']
    receivers = [
        ['Jacob', 'Joshua', 'Mary', 'Noah', 'Jason', 'Olivia', 'Mike'],   # Hannah
        ['Hannah', 'Joshua', 'Noah', 'Mary', 'Jason', 'Olivia', 'Mike'],  # Jacob
        ['Hannah', 'Jacob', 'Mary', 'Noah', 'Jason', 'Olivia', 'Mike'],   # Josh
        ['Hannah', 'Jacob', 'Joshua', 'Jason', 'Olivia', 'Mike'],         # Mary
        ['Hannah', 'Jacob', 'Joshua', 'Jason', 'Olivia', 'Mike'],         # Noah
        ['Hannah', 'Jacob', 'Joshua', 'Mary', 'Noah', 'Olivia', 'Mike'],  # Jason
        ['Hannah', 'Jacob', 'Joshua', 'Mary', 'Noah', 'Jason'],           # Olivia
        ['Hannah', 'Jacob', 'Joshua', 'Mary', 'Noah', 'Jason'],           # Mike
    ]

    attempts = 0
    while True:
        attempts += 1
        pairings = {}
        taken = set()

        valid = True
        for i, giver in enumerate(givers):
            # Find a match not already taken
            available = [r for r in random.sample(receivers[i], len(receivers[i])) if r not in taken]
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
    filename = f'adultPollyanna_{current_date}.json'
    file_path = os.path.join(os.getcwd(), filename)

    with open(file_path, 'w') as f:
        json.dump(pairings, f, indent=4)

    print(f"Adult Pollyanna pairings saved to {filename}.")

    #######################################
    # Send email in a separate thread
    #######################################
    def send_email_in_thread():
        send_email(
            "Pollyanna 2024 - Adult List",
            "Attached is the adult list for the 2024 Pollyanna.",
            "tua04072@gmail.com",
            file_path
        )

    email_thread = threading.Thread(target=send_email_in_thread)
    email_thread.start()

    return pairings
