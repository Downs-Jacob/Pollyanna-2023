import unittest
import os
from datetime import date
from kidList import kidList
from adultList import adultList
import json
from PyQt5.QtWidgets import QApplication
from main import PollyannaApp
import sys
from itertools import permutations

def has_two_person_loop(pairings):
    """Check if there are any two-person loops (A->B->A) in the pairings"""
    for person, receiver in pairings.items():
        # If the receiver gives back to the original person, it's a two-person loop
        if receiver in pairings and pairings[receiver] == person:
            return True
    return False

def has_closed_loop(pairings):
    """Check if there are any closed loops in the pairings"""
    for start in pairings:
        # Follow the chain starting from each person
        visited = set()
        current = start
        while True:
            if current in visited:
                # If we see someone again, we found a loop
                # Only report it if it starts with the person we began with
                return current == start
            visited.add(current)
            if current not in pairings:
                break
            current = pairings[current]
    return False

def find_loops(pairings):
    """Find and return all loops in the pairings"""
    loops = []
    visited = set()
    
    for start in pairings:
        if start in visited:
            continue
            
        # Follow the chain starting from this person
        current_path = []
        current = start
        path_set = set()
        
        while True:
            if current in path_set:
                # Found a loop - extract it
                loop_start_idx = current_path.index(current)
                loop = current_path[loop_start_idx:]
                if loop not in loops:
                    loops.append(loop)
                break
                
            if current not in pairings:
                break
                
            current_path.append(current)
            path_set.add(current)
            visited.add(current)
            current = pairings[current]
            
    return loops

def count_valid_kid_combinations():
    """Count all possible valid Pollyanna combinations for kids"""
    givers = ['Evangeline', 'Caleb', 'Kate', 'Grace', 'Isabella', 'Sophia', 'Lana']
    valid_receivers = {
        'Evangeline': {'Caleb', 'Grace', 'Isabella', 'Kate', 'Sophia', 'Lana'},
        'Caleb': {'Evangeline', 'Grace', 'Isabella', 'Sophia', 'Lana'},
        'Kate': {'Evangeline', 'Grace', 'Isabella', 'Sophia', 'Lana'},
        'Grace': {'Evangeline', 'Caleb', 'Isabella', 'Kate', 'Sophia', 'Lana'},
        'Isabella': {'Evangeline', 'Caleb', 'Grace', 'Kate', 'Sophia', 'Lana'},
        'Sophia': {'Evangeline', 'Caleb', 'Grace', 'Isabella', 'Kate', 'Lana'},
        'Lana': {'Evangeline', 'Caleb', 'Grace', 'Isabella', 'Kate', 'Sophia'}
    }
    
    total_count = 0
    valid_count = 0  # combinations without 2-person loops
    sophia_gets_lana = 0
    sophia_gets_lana_valid = 0
    loop_sizes = {}
    example_with_sophia_lana = None
    
    # Try all possible permutations
    for perm in permutations(givers):
        valid = True
        # Check if each giver-receiver pair is valid
        pairings = {}
        for i, giver in enumerate(givers):
            receiver = perm[i]
            if receiver == giver or receiver not in valid_receivers[giver]:
                valid = False
                break
            pairings[giver] = receiver
            
        if valid:
            total_count += 1
            
            # Check for two-person loops
            if not has_two_person_loop(pairings):
                valid_count += 1
                # Find loops in this valid combination
                loops = find_loops(pairings)
                for loop in loops:
                    size = len(loop)
                    loop_sizes[size] = loop_sizes.get(size, 0) + 1
                
                # Check if Sophia gets Lana in this valid combination
                if pairings['Sophia'] == 'Lana':
                    sophia_gets_lana_valid += 1
                    if example_with_sophia_lana is None:
                        example_with_sophia_lana = pairings.copy()
            
            # Track total Sophia->Lana count for comparison
            if pairings['Sophia'] == 'Lana':
                sophia_gets_lana += 1
    
    print(f"\nResults with two-person loops allowed:")
    print(f"Total valid combinations: {total_count}")
    print(f"Times Sophia gets Lana: {sophia_gets_lana}")
    print(f"Percentage of times Sophia gets Lana: {(sophia_gets_lana/total_count)*100:.2f}%")
    
    print(f"\nResults without two-person loops:")
    print(f"Valid combinations: {valid_count}")
    print(f"Times Sophia gets Lana: {sophia_gets_lana_valid}")
    print(f"Percentage of times Sophia gets Lana: {(sophia_gets_lana_valid/valid_count)*100:.2f}%")
    
    print("\nLoop size distribution (in valid combinations):")
    for size in sorted(loop_sizes.keys()):
        print(f"Size {size} loops: {loop_sizes[size]/valid_count*100:.2f}%")
    
    if example_with_sophia_lana:
        print("\nExample valid combination where Sophia gets Lana:")
        current = 'Sophia'
        chain = []
        seen = set()
        while current not in seen:
            chain.append(current)
            seen.add(current)
            current = example_with_sophia_lana[current]
        chain.append(current)  # Add the loop closer
        print(" -> ".join(chain))
    
    return total_count, sophia_gets_lana, valid_count, sophia_gets_lana_valid

class TestPollyannaGeneration(unittest.TestCase):
    def setUp(self):
        # Initialize QApplication for UI tests
        self.app = QApplication(sys.argv)
        self.window = PollyannaApp()

    def test_kid_list_generation(self):
        """Test that kid Pollyanna pairings are valid"""
        pairings = kidList()
        
        # Test that pairings were generated
        self.assertTrue(pairings, "Kid pairings should not be empty")
        
        # Test that all kids are included
        expected_kids = {'Evangeline', 'Caleb', 'Kate', 'Grace', 'Isabella', 'Sophia', 'Lana'}
        self.assertEqual(set(pairings.keys()), expected_kids, "All kids should be givers")
        self.assertTrue(set(pairings.values()).issubset(expected_kids), 
                        "All receivers should be from the kid list")

        # Test that no one has themselves
        for giver, receiver in pairings.items():
            self.assertNotEqual(giver, receiver, f"{giver} should not have themselves as Pollyanna")

        # Test valid pairings
        valid_receivers = {
            'Evangeline': {'Caleb', 'Grace', 'Isabella', 'Kate', 'Sophia', 'Lana'},
            'Caleb': {'Evangeline', 'Grace', 'Isabella', 'Sophia', 'Lana'},
            'Kate': {'Evangeline', 'Grace', 'Isabella', 'Sophia', 'Lana'},
            'Grace': {'Evangeline', 'Caleb', 'Isabella', 'Kate', 'Sophia', 'Lana'},
            'Isabella': {'Evangeline', 'Caleb', 'Grace', 'Kate', 'Sophia', 'Lana'},
            'Sophia': {'Evangeline', 'Caleb', 'Grace', 'Isabella', 'Kate', 'Lana'},
            'Lana': {'Evangeline', 'Caleb', 'Grace', 'Isabella', 'Kate', 'Sophia'}
        }
        
        for giver, receiver in pairings.items():
            self.assertIn(receiver, valid_receivers[giver], 
                         f"{receiver} is not a valid Pollyanna for {giver}")

    def test_adult_list_generation(self):
        """Test that adult Pollyanna pairings are valid"""
        pairings = adultList()
        
        # Test that pairings were generated
        self.assertTrue(pairings, "Adult pairings should not be empty")
        
        # Test that all adults are included
        expected_adults = {'Hannah', 'Jacob', 'Joshua', 'Mary', 'Noah', 'Jason', 'Olivia', 'Mike'}
        self.assertEqual(set(pairings.keys()), expected_adults, "All adults should be givers")
        self.assertTrue(set(pairings.values()).issubset(expected_adults), 
                        "All receivers should be from the adult list")

        # Test that no one has themselves
        for giver, receiver in pairings.items():
            self.assertNotEqual(giver, receiver, f"{giver} should not have themselves as Pollyanna")

        # Test valid pairings
        valid_receivers = {
            'Hannah': {'Jacob', 'Joshua', 'Mary', 'Noah', 'Jason', 'Olivia', 'Mike'},
            'Jacob': {'Hannah', 'Joshua', 'Noah', 'Mary', 'Jason', 'Olivia', 'Mike'},
            'Joshua': {'Hannah', 'Jacob', 'Mary', 'Noah', 'Jason', 'Olivia', 'Mike'},
            'Mary': {'Hannah', 'Jacob', 'Joshua', 'Jason', 'Olivia', 'Mike'},
            'Noah': {'Hannah', 'Jacob', 'Joshua', 'Jason', 'Olivia', 'Mike'},
            'Jason': {'Hannah', 'Jacob', 'Joshua', 'Mary', 'Noah', 'Olivia', 'Mike'},
            'Olivia': {'Hannah', 'Jacob', 'Joshua', 'Mary', 'Noah', 'Jason'},
            'Mike': {'Hannah', 'Jacob', 'Joshua', 'Mary', 'Noah', 'Jason'}
        }
        
        for giver, receiver in pairings.items():
            self.assertIn(receiver, valid_receivers[giver], 
                         f"{receiver} is not a valid Pollyanna for {giver}")

    def test_file_generation(self):
        """Test that Pollyanna files are generated correctly"""
        # Run both generators
        kidList()
        adultList()
        
        # Check that files were created
        current_date = date.today().strftime("%Y-%m-%d")
        kid_filename = f'kidPollyanna_{current_date}.json'
        adult_filename = f'adultPollyanna_{current_date}.json'
        
        self.assertTrue(os.path.exists(kid_filename), "Kid Pollyanna file should be created")
        self.assertTrue(os.path.exists(adult_filename), "Adult Pollyanna file should be created")
        
        # Check that files contain valid JSON
        try:
            with open(kid_filename) as f:
                kid_data = json.load(f)
            with open(adult_filename) as f:
                adult_data = json.load(f)
                
            self.assertTrue(isinstance(kid_data, dict), "Kid file should contain a dictionary")
            self.assertTrue(isinstance(adult_data, dict), "Adult file should contain a dictionary")
        except json.JSONDecodeError:
            self.fail("Generated files should contain valid JSON")

    def test_ui_initialization(self):
        """Test that the UI initializes correctly"""
        # Test window properties
        self.assertEqual(self.window.windowTitle(), f"Pollyanna {self.window.current_year}")
        self.assertEqual(self.window.title_label.text(), 
                        f"🎁 Welcome to Pollyanna {self.window.current_year} 🎁")
        
        # Test that buttons exist and are enabled
        self.assertTrue(self.window.kid_button.isEnabled(), "Kid button should be enabled")
        self.assertTrue(self.window.adult_button.isEnabled(), "Adult button should be enabled")
        
        # Test button text
        self.assertEqual(self.window.kid_button.text(), "🎈 Start Kid Pollyanna")
        self.assertEqual(self.window.adult_button.text(), "🎉 Start Adult Pollyanna")

    def test_count_combinations(self):
        """Test to count all possible valid Pollyanna combinations"""
        total_count, sophia_gets_lana, valid_count, sophia_gets_lana_valid = count_valid_kid_combinations()
        self.assertGreater(total_count, 0, "There should be at least one valid combination")
        self.assertGreater(valid_count, 0, "There should be at least one valid combination without two-person loops")

    def tearDown(self):
        """Clean up after tests"""
        # Clean up any generated files
        current_date = date.today().strftime("%Y-%m-%d")
        files_to_remove = [
            f'kidPollyanna_{current_date}.json',
            f'adultPollyanna_{current_date}.json'
        ]
        
        for file in files_to_remove:
            if os.path.exists(file):
                try:
                    os.remove(file)
                except Exception as e:
                    print(f"Warning: Could not remove test file {file}: {str(e)}")

if __name__ == '__main__':
    # If you want to just run the combination counter:
    # print(f"Total valid combinations: {count_valid_kid_combinations()}")
    unittest.main()
