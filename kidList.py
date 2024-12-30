import random
import json
from datetime import date
import os
from emailLogic import send_email
import threading

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

    MAX_ATTEMPTS = 1000
    attempts = 0
    
    while attempts < MAX_ATTEMPTS:
        attempts += 1
        pairings = {}
        taken = set()
        valid = True
        
        # Shuffle the givers to increase randomness
        giver_indices = list(range(len(givers)))
        random.shuffle(giver_indices)
        
        for i in giver_indices:
            giver = givers[i]
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
            print(f"Kid pairing succeeded after {attempts} attempt(s).")
            break
    
    if attempts >= MAX_ATTEMPTS:
        print("Failed to generate valid kid pairings after maximum attempts.")
        return {}

    try:
        # Save pairings to a file
        current_date = date.today().strftime("%Y-%m-%d")
        filename = f'kidPollyanna_{current_date}.json'
        file_path = os.path.join(os.getcwd(), filename)

        with open(file_path, 'w') as f:
            json.dump(pairings, f, indent=4)

        print(f"Kid Pollyanna pairings saved to {filename}.")

        # Send email in a separate thread
        def send_email_in_thread():
            try:
                send_email(
                    "Pollyanna 2024 - Kid List",
                    "Attached is the kid list for the 2024 Pollyanna.",
                    "tua04072@gmail.com",
                    file_path
                )
            except Exception as e:
                print(f"Error sending email: {str(e)}")

        email_thread = threading.Thread(target=send_email_in_thread)
        email_thread.start()

    except Exception as e:
        print(f"Error saving pairings: {str(e)}")

    return pairings
