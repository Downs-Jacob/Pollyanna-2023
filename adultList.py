import random
import json
from datetime import date
import os
from emailLogic import send_email


def adultList():
    givers = ['Hannah','Jacob','Joshua','Mary','Noah', 'Jason', 'Olivia', 'Mike']
    receivers = [
        ['Jacob','Joshua','Mary', 'Noah', 'Jason', 'Olivia', 'Mike'],###### Hannah
        ['Hannah','Joshua','Noah', 'Mary', 'Jason', 'Olivia', 'Mike'],##### Jacob
        ['Hannah','Jacob','Mary','Noah', 'Jason', 'Olivia', 'Mike'],##### Josh
        ['Hannah','Jacob','Joshua', 'Jason', 'Olivia', 'Mike'],############ Mary
        ['Hannah','Jacob','Joshua', 'Jason', 'Olivia', 'Mike'],############ Noah
        ['Hannah','Jacob','Joshua', 'Mary','Noah', 'Olivia', 'Mike'],###### Jason
        ['Hannah','Jacob','Joshua', 'Mary','Noah', 'Jason'],############### Olivia
        ['Hannah','Jacob','Joshua', 'Mary','Noah', 'Jason'],############### Mike
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

    send_email("Pollyanna 2024 - Adult List", "Attached is the adult list for the 2024 Pollyanna", "tua04072@gmail.com", file_path)
    #downs1973@comcast.net
    print("Adult List Generated")
    return pairings
import random
import json
from datetime import date
import os
from emailLogic import send_email
import threading  # For threading email sending


def adultList():
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

    # Save the pairings to a file
    current_date = date.today().strftime("%d-%m-%Y")
    random_number = random.randint(1, 50000)
    filename = f'adultPollyanna_{current_date}_{random_number}.txt'
    file_path = os.path.join(os.getcwd(), filename)

    with open(file_path, 'w') as f:
        json.dump(pairings, f, indent=4)

    #######################################
    # emails in a separate thread
    #######################################

    def send_email_in_thread():
        send_email(
            "Pollyanna 2024 - Adult List",
            "Attached is the adult list for the 2024 Pollyanna.",
            "downs1973@comcast.net",
            #downs1973@comcast.net
            file_path
        )

    email_thread = threading.Thread(target=send_email_in_thread)
    email_thread.start()

    print("Adult List Generated")
    return pairings
