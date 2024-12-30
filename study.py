from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
import csv
import os
import glob
from kivy.storage.jsonstore import JsonStore

from functools import partial

# User Modules
import submaking
import making

fc = submaking.Flashcard()

class CreateSetPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Create Set"
        self.size_hint = (0.8, 0.4)
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.set_name_input = TextInput(hint_text="Enter Name of the Set", multiline=False)
        layout.add_widget(self.set_name_input)

        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        confirm_button = Button(text="Confirm", background_color=(0, 1, 0, 1))
        confirm_button.bind(on_release=self.confirm)
        cancel_button = Button(text="Cancel", background_color=(1, 0, 0, 1))
        cancel_button.bind(on_release=self.dismiss)

        button_layout.add_widget(confirm_button)
        button_layout.add_widget(cancel_button)
        layout.add_widget(button_layout)
        self.content = layout

    def confirm(self, instance):
        set_name = self.set_name_input.text.strip()
        if set_name:
            try:
                current_directory = os.path.dirname(os.path.abspath(__file__))
                flashcard_directory = os.path.join(current_directory, "Flashcards")
                os.makedirs(flashcard_directory, exist_ok=True)

                title_store = JsonStore(os.path.join(current_directory, "Title.json"))
                title_store.put("title", name=set_name)

                csv_path = os.path.join(flashcard_directory, f"{set_name}.csv")

                with open(csv_path, "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["Term", "Description"])
                    writer.writerows(fc.flashcards or [["Sample Term", "Sample Description"]])

                print(f"Set '{set_name}' created successfully!")
            except Exception as e:
                print(f"Error creating set: {e}")
        else:
            print("Set name cannot be empty.")
        self.dismiss()

class Studies(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        self.search_bar = TextInput(hint_text="Search", size_hint=(1, 0.1), multiline=False)
        self.search_bar.bind(text=self.update_flashcard_grid)

        self.top_bar = BoxLayout(size_hint=(1, 0.1), spacing=10)
        sync_button = Button(text="SYNC WITH MOBILE", size_hint=(0.5, 1), background_color=(0, 0, 1, 1))
        back_button = Button(text="Back to Main", size_hint=(0.5, 1), background_color=(0, 0, 1, 1))

        back_button.bind(on_release=lambda x: (self.refresh_flashcard_grid(), setattr(self.manager, 'current', 'play')))

        
        self.top_bar.add_widget(sync_button)
        self.top_bar.add_widget(back_button)

        self.flashcard_grid = GridLayout(cols=3, spacing=10, size_hint_y=None)
        self.flashcard_scroll = ScrollView(size_hint=(1, 0.7))
        self.flashcard_scroll.add_widget(self.flashcard_grid)

        self.create_set_button = Button(text="CREATE SET", size_hint=(1, 0.1), background_color=(0, 0, 1, 1))
        self.create_set_button.bind(on_release=self.open_create_set_popup)

        self.main_layout.add_widget(self.top_bar)
        self.main_layout.add_widget(self.search_bar)
        self.main_layout.add_widget(self.flashcard_scroll)
        self.main_layout.add_widget(self.create_set_button)

        self.add_widget(self.main_layout)
        self.load_flashcard_grid()

    def open_create_set_popup(self, instance):
        popup = CreateSetPopup()
        popup.open()

    def load_flashcard_grid(self):
        self.flashcard_grid.clear_widgets()
        sets = self.get_files_csv()
        for set_name in sets:
            card = BoxLayout(orientation="vertical", padding=5, spacing=5, size_hint=(None, None), size=(200, 100))
            card_label = Label(text=set_name, halign="center", valign="middle")
            card_label.bind(size=card_label.setter('text_size'))

            open_button = Button(text="Open", size_hint=(1, 0.3), background_color=(0, 0, 1, 1))
            open_button.bind(on_release=lambda instance, name=set_name: self.open_set(name))

            card.add_widget(card_label)
            card.add_widget(open_button)
            self.flashcard_grid.add_widget(card)

    def update_flashcard_grid(self, instance, value):
        self.flashcard_grid.clear_widgets()
        sets = [s for s in self.get_files_csv() if value.lower() in s.lower()]
        for set_name in sets:
            card = BoxLayout(orientation="vertical", padding=5, spacing=5, size_hint=(None, None), size=(200, 100))
            card_label = Label(text=set_name, halign="center", valign="middle")
            card_label.bind(size=card_label.setter('text_size'))

            open_button = Button(text="Open", size_hint=(1, 0.3), background_color=(0, 0, 1, 1))
            open_button.bind(on_release=lambda instance, name=set_name: self.open_set(name))

            card.add_widget(card_label)
            card.add_widget(open_button)
            self.flashcard_grid.add_widget(card)


    def open_set(self, set_name):
        try:
            title_store = JsonStore(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Title.json"))
            title_store.put("title", name=set_name)  # Update Title.json with the new set name
            print(f"Saved {set_name} to Title.json")
            
            # Explicitly reload the flashcards after updating Title.json
            if hasattr(fc, "load_flashcards"):
                fc.load_flashcards()
            else:
                print("Error: Flashcard object does not support 'load_flashcards'.")
            
            # Change the screen after ensuring data is reloaded
            self.manager.current = "CreateFlash"
            return set_name
        except Exception as e:
            print(f"Error opening set: {e}")
            return None


    def get_files_csv(self):
        try:
            directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Flashcards")
            os.makedirs(directory, exist_ok=True)
            csv_files = glob.glob(os.path.join(directory, "*.csv"))
            return [os.path.splitext(os.path.basename(file))[0] for file in csv_files]
        except Exception as e:
            import traceback
            print(f"Error retrieving files: {e}\n{traceback.format_exc()}")
            return []

    def refresh_flashcard_grid(self):
        self.clear_widgets()  # Remove all existing widgets
        self.__init__()       # Reinitialize the screen

    

    

