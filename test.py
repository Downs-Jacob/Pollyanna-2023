import random
import json
from datetime import date
import os

def get_participants():
    number_of_participants = int(input("How many participants are there? "))
    participants = []

    for _ in range(number_of_participants):
        while True:
            name = input("Enter the participant's name: ").strip()
            if name not in participants:
                participants.append(name)
                break
            else:
                print("Each participant must have a unique name. Please try again.")
    
    return participants

def generate_pairings(participants):
    # Shuffle the list to randomize the pairings
    shuffled_participants = participants[:]
    random.shuffle(shuffled_participants)

    # Create a pairing such that no participant is paired with themselves
    pairings = {}
    for i in range(len(participants)):
        receiver = shuffled_participants[i]
        if receiver == participants[i]:
            # If the last participant is paired with themselves, swap with the previous
            if i == len(participants) - 1:
                pairings[participants[i - 1]], receiver = receiver, pairings[participants[i - 1]]
            # Otherwise, swap with the next participant
            else:
                shuffled_participants[i], shuffled_participants[i + 1] = shuffled_participants[i + 1], shuffled_participants[i]
                receiver = shuffled_participants[i]

        pairings[participants[i]] = receiver

    return pairings

def save_pairings(pairings):
    current_date = date.today().strftime("%d-%m-%Y")
    random_number = random.randint(1, 50000)
    filename = f'kidPollyanna_{current_date}_{random_number}.json'
    file_path = os.path.join(os.getcwd(), filename)
    with open(file_path, 'w') as f:
        json.dump(pairings, f, indent=4)
    print(f"Pairings saved to {filename}")

# Main function to run the Secret Santa generator
def run_secret_santa():
    participants = get_participants()
    try:
        pairings = generate_pairings(participants)
        print("Pairings generated successfully:")
        for giver, receiver in pairings.items():
            print(f"{giver} -> {receiver}")
        save_pairings(pairings)
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    run_secret_santa()
