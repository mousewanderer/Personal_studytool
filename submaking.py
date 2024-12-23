import json
import csv
import os


count = 0
# Get the current directory (same folder as the Python file)
current_directory = os.path.dirname(os.path.abspath(__file__))
current_directory = current_directory + "\\Flashcards\\"



class Flashcard:
    def __init__(self):
        self.flashcards = self.load_flashcards()

    def load_flashcards(self):
        # Load the filename from the JSON file
        try:
            with open('Title.json', 'r') as file:
                name = json.load(file)  # Assuming it returns a string containing the f
                name = current_directory + name
        except FileNotFoundError:
            return []

        # Use the name from the JSON file to load the corresponding CSV
        try:
            with open(f'{name}.csv', 'r') as file:
                reader = csv.reader(file)
                return [tuple(row) for row in reader if row]  # Convert rows to tuples (Title, Activity)
        except FileNotFoundError:
            return []

    def save_flashcards(self):
        # Load the filename from the JSON file
        try:
            with open('Title.json', 'r') as file:
                name = json.load(file)
                name = current_directory + name
        except FileNotFoundError:
            return

        # Save the flashcards to the corresponding CSV
        with open(f'{name}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.flashcards)

    def display_flashcards(self):
        if not self.flashcards:
            return "No flashcards found."
        else:
            result = ""
            for index, (title, activity) in enumerate(self.flashcards, start=1):
                result += f"{index}. Term: {title}, Description: {activity}\n"
            return result.strip()

    def display_flashcard_from_index(self, index):
        if 0 < index <= len(self.flashcards):
            title, activity = self.flashcards[index - 1]
            return f"{title},{activity}"
        else:
            return "Invalid flashcard index."

    def add_flashcard(self, title, activity):
        self.flashcards.append((title, activity))
        self.save_flashcards()
        return "Flashcard added successfully."

    def update_flashcard(self, index, title, activity):
        if 0 < index <= len(self.flashcards):
            self.flashcards[index - 1] = (title, activity)
            self.save_flashcards()
            return "Flashcard updated successfully."
        else:
            return "Invalid flashcard index."

    def delete_flashcard(self, index):
        if 0 < index <= len(self.flashcards):
            del self.flashcards[index - 1]
            self.save_flashcards()
            return "Flashcard deleted successfully."
        else:
            return "Invalid flashcard index."
