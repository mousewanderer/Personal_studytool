import csv
import os
from kivy.storage.jsonstore import JsonStore

class Flashcard:
    def __init__(self, default_set=None):
        """
        Initializes the Flashcard instance. Loads the current set from Title.json or uses the default set.
        """
        self.flashcards = []
        self.current_set = self.get_current_set() or default_set
        if self.current_set:
            self.flashcards = self.load_flashcards()

    def get_file_location(self):
        """
        Returns the path to the Flashcards directory.
        """
        current_directory = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_directory, "Flashcards")

    def get_title_store(self):
        """
        Returns a JsonStore instance for Title.json.
        """
        current_directory = os.path.dirname(os.path.abspath(__file__))
        return JsonStore(os.path.join(current_directory, "Title.json"))

    def get_current_set(self):
        """
        Loads the current set name from Title.json.
        """
        try:
            title_store = self.get_title_store()
            if title_store.exists("title"):
                return title_store.get("title")["name"]
            return None
        except Exception as e:
            print(f"Error loading current set: {e}")
            return None

    def set_current_set(self, set_name):
        """
        Saves the current set name to Title.json and updates the current set in memory.
        """
        if not set_name or not isinstance(set_name, str):
            print("Invalid set name. It must be a non-empty string.")
            return

        try:
            title_store = self.get_title_store()
            title_store.put("title", name=set_name)
            self.current_set = set_name
            print(f"Current set updated to: {set_name}")
        except Exception as e:
            print(f"Error saving current set: {e}")

    def load_flashcards(self):
        """
        Loads flashcards from the CSV file corresponding to the current set.
        """
        if not self.current_set:
            print("No current set to load flashcards from.")
            return []

        csv_path = os.path.join(self.get_file_location(), f"{self.current_set}.csv")
        try:
            with open(csv_path, 'r', newline='') as file:
                reader = csv.reader(file)
                return [tuple(row) for row in reader if row]  # Convert rows to tuples
        except FileNotFoundError:
            print(f"No file found for set: {self.current_set}. Starting with an empty set.")
            return []

    def save_flashcards(self):
        """
        Saves the flashcards to the CSV file corresponding to the current set.
        """
        if not self.current_set:
            print("No current set to save flashcards to.")
            return

        csv_path = os.path.join(self.get_file_location(), f"{self.current_set}.csv")
        os.makedirs(self.get_file_location(), exist_ok=True)  # Ensure the directory exists
        try:
            with open(csv_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(self.flashcards)
                print(f"Flashcards saved to set: {self.current_set}")
        except Exception as e:
            print(f"Error saving flashcards: {e}")

    def display_flashcards(self):
        """
        Displays all flashcards in the current set.
        """
        if not self.flashcards:
            return "No flashcards found."
        result = "\n".join(
            f"{index + 1}. Term: {title}, Description: {activity}"
            for index, (title, activity) in enumerate(self.flashcards)
        )
        return result.strip()

    def display_flashcard_from_index(self, index):
        """
        Displays a specific flashcard by its index.
        """
        if 0 < index <= len(self.flashcards):
            title, activity = self.flashcards[index - 1]
            return f"Term: {title}, Description: {activity}"
        return "Invalid flashcard index."

    def add_flashcard(self, title, activity):
        """
        Adds a new flashcard to the current set.
        """
        if not title or not activity:
            return "Both term and description are required."
        self.flashcards.append((title.strip(), activity.strip()))
        self.save_flashcards()
        return "Flashcard added successfully."

    def update_flashcard(self, index, title, activity):
        """
        Updates an existing flashcard by its index.
        """
        if not (0 < index <= len(self.flashcards)):
            return "Invalid flashcard index."
        if not title or not activity:
            return "Both term and description are required."
        self.flashcards[index - 1] = (title.strip(), activity.strip())
        self.save_flashcards()
        return "Flashcard updated successfully."

    def delete_flashcard(self, index):
        """
        Deletes a flashcard by its index.
        """
        if not (0 < index <= len(self.flashcards)):
            return "Invalid flashcard index."
        del self.flashcards[index - 1]
        self.save_flashcards()
        return "Flashcard deleted successfully."
