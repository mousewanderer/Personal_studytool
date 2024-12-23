import submaking
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import csv
from kivy.uix.screenmanager import Screen, ScreenManager

import json,os
fc = submaking.Flashcard()  # Flashcard functionality from your imported OOP module


try:
    with open('Title.json', 'r') as file:
        name = json.load(file)  # Assuming it returns a string containing the f
except FileNotFoundError:
    print("Not found")
    name =""

class CreateFlashcard(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Main layout setup
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Title label (Top-Left Style)
        title_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        self.title_label = Label(
            text=str(name),
            font_size=18,
            size_hint=(None, None),
            size=(200, 40),
            color=(1, 1, 1, 1),
            halign='left',
            valign='middle'
        )
        title_layout.add_widget(self.title_label)
        self.layout.add_widget(title_layout)

        # Search bar
        self.search_input = TextInput(hint_text="Search", size_hint_y=None, height=40)
        self.layout.add_widget(self.search_input)

        # Scrollable flashcard display
        self.scroll_view = ScrollView(size_hint=(1, None), height=200)
        self.scroll_content = GridLayout(cols=1, size_hint_y=None)
        self.scroll_content.bind(minimum_height=self.scroll_content.setter('height'))
        self.scroll_view.add_widget(self.scroll_content)
        self.layout.add_widget(self.scroll_view)

        # Input fields for adding/editing flashcards
        self.term_input = TextInput(hint_text="Enter Term", size_hint_y=None, height=40)
        self.description_input = TextInput(hint_text="Enter Description", size_hint_y=None, height=40)
        self.layout.add_widget(self.term_input)
        self.layout.add_widget(self.description_input)

        # Add action buttons
        self.add_action_buttons()

        # Add footer buttons
        self.add_footer_buttons()

        self.add_widget(self.layout)

    def add_action_buttons(self):
        action_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)

        share_button = Button(text="Share", background_color=(0, 0, 0.5, 1))
        download_button = Button(text="Download CSV", background_color=(0, 0, 0.5, 1))
        sync_button = Button(text="Sync", background_color=(0, 0, 0.5, 1))

        action_layout.add_widget(share_button)
        action_layout.add_widget(download_button)
        action_layout.add_widget(sync_button)

        self.layout.add_widget(action_layout)

    def add_footer_buttons(self):
        footer_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)

        self.add_button = Button(text="Add Card", background_color=(0, 0, 0.5, 1))
        self.edit_button = Button(text="Edit Card", background_color=(0, 0, 0.5, 1))
        self.view_button = Button(text="View Flashcards", background_color=(0, 0, 0.5, 1))
        self.delete_button = Button(text="Delete Card", background_color=(0.5, 0, 0, 1))

        #return to the selection 
        self.back_button = Button(text="BACK", background_color=(0, 0, 0.5, 1))
        self.back_button.bind(on_release=lambda x: setattr(self.manager, 'current', 'Studying'))

        # Button bindings
        self.add_button.bind(on_press=self.add_flashcard)
        self.edit_button.bind(on_press=self.update_flashcard)
        self.view_button.bind(on_press=self.view_flashcards)
        self.delete_button.bind(on_press=self.delete_flashcard)

        footer_layout.add_widget(self.add_button)
        footer_layout.add_widget(self.edit_button)
        footer_layout.add_widget(self.view_button)
        footer_layout.add_widget(self.delete_button)
        footer_layout.add_widget(self.back_button)

        self.layout.add_widget(footer_layout)

    def add_flashcard(self, instance):
        term = self.term_input.text.strip()
        description = self.description_input.text.strip()
        if term and description:
            message = fc.add_flashcard(term, description)
        else:
            message = "Both Term and Description are required."
        self.display_message(message)

    def view_flashcards(self, instance):
        self.scroll_content.clear_widgets()
        flashcards_data = fc.display_flashcards()

        if isinstance(flashcards_data, str):
            from io import StringIO
            csv_reader = csv.reader(StringIO(flashcards_data))
            flashcards = list(csv_reader)
        else:
            flashcards = flashcards_data

        for flashcard in flashcards:
            if len(flashcard) == 2:
                term, description = flashcard
                card_label = Label(text=f"{term}: {description}", size_hint_y=None, height=40)
                self.scroll_content.add_widget(card_label)

        self.scroll_view.scroll_y = 1

    def update_flashcard(self, instance):
        try:
            index = int(self.term_input.text.strip())
            new_term = self.description_input.text.strip()
            new_description = self.search_input.text.strip()
            if new_term and new_description:
                message = fc.update_flashcard(index, new_term, new_description)
            else:
                message = "Both new Term and new Description are required."
        except ValueError:
            message = "Invalid index. Enter a valid number in the Term field."
        self.display_message(message)

    def delete_flashcard(self, instance):
        try:
            index = int(self.term_input.text.strip())
            message = fc.delete_flashcard(index)
        except ValueError:
            message = "Invalid index. Enter a valid number in the Term field."
        self.display_message(message)

    def display_message(self, message):
        self.search_input.text = message
        self.clear_inputs()

    def clear_inputs(self):
        self.term_input.text = ""
        self.description_input.text = ""


