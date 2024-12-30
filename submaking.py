import csv
import os
from kivy.storage.jsonstore import JsonStore


class Flashcard:
    def __init__(self):
        self.flashcards = []
        self.current_set = self.get_current_set()
        if self.current_set:
            self.flashcards = self.load_flashcards()

    def get_file_location(self):
        # Get the Flashcards directory path
        current_directory = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_directory, "Flashcards")

    def get_title_store(self):
        # Initialize and return the JsonStore for Title.json
        current_directory = os.path.dirname(os.path.abspath(__file__))
        return JsonStore(os.path.join(current_directory, "Title.json"))

    def get_current_set(self):
        # Load the current set name from Title.json
        try:
            title_store = self.get_title_store()
            if title_store.exists("title"):
                return title_store.get("title")["name"]
            return None
        except Exception as e:
            print(f"Error loading current set: {e}")
            return None

    def set_current_set(self, set_name):
        # Save the current set name to Title.json
        try:
            title_store = self.get_title_store()
            title_store.put("title", name=set_name)
            self.current_set = set_name
        except Exception as e:
            print(f"Error saving current set: {e}")

    def load_flashcards(self):
        # Load flashcards from the CSV corresponding to the current set
        if not self.current_set:
            return []

        csv_path = os.path.join(self.get_file_location(), f"{self.current_set}.csv")
        try:
            with open(csv_path, 'r') as file:
                reader = csv.reader(file)
                return [tuple(row) for row in reader if row]  # Convert rows to tuples
        except FileNotFoundError:
            return []

    def save_flashcards(self):
        # Save flashcards to the CSV corresponding to the current set
        if not self.current_set:
            return

        csv_path = os.path.join(self.get_file_location(), f"{self.current_set}.csv")
        os.makedirs(self.get_file_location(), exist_ok=True)  # Ensure directory exists
        with open(csv_path, 'w', newline='') as file:
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
            return f"{title}, {activity}"
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

    def clear_flashcards(self):
        self.flashcards = []  # Clear the flashcards list
