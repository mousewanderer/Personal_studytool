from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

#_______________________Built In modules_________________________

import csv,os,glob,json

#--------USer Modules-------------
import submaking
import making

count = 0
# Get the current directory (same folder as the Python file)
current_directory = os.path.dirname(os.path.abspath(__file__))


current_directory = current_directory + "\Flashcards"
# Use glob to find all CSV files in the current directory
csv_files = glob.glob(os.path.join(current_directory, '*.csv'))
# Extract just the file names from the full paths
csv_file_names = [os.path.basename(file) for file in csv_files]
#Removing .csv in the name
for t in csv_file_names:
    csv_file_names[count] = t.replace(".csv","")
    count+=1

#___________________________________________________________

fc = submaking.Flashcard()
#___________________________________________________________





#-------------------------------------------------------------Creator

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
            # Save the set name to Title.json
            title_data = set_name
            current_directory = os.path.dirname(os.path.abspath(__file__)) + "\\Flashcards"
            os.makedirs(current_directory, exist_ok=True)

            with open(os.path.join(current_directory, "Title.json"), "w") as json_file:
                json.dump(title_data, json_file)

            # Create an empty CSV file for the new set
            with open(os.path.join(current_directory, f"{set_name}.csv"), "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(fc.flashcards)

            print(f"Set '{set_name}' created successfully!")
        else:
            print("Set name cannot be empty.")

        self.dismiss()





class Studies(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Main layout
        main_layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        # Top bar with sync and pre-made sets buttons
        top_bar = BoxLayout(size_hint=(1, 0.1), spacing=10)
        sync_button = Button(text="SYNC WITH MOBILE", size_hint=(0.5, 1), background_color=(0, 0, 1, 1))




        #if back button press go back to play
        back_button = Button(text="Back to Main", size_hint=(0.5, 1), background_color=(0, 0, 1, 1))
        back_button.bind(on_release=lambda x: setattr(self.manager, 'current', 'play'))



        
        top_bar.add_widget(sync_button)
        top_bar.add_widget(back_button)
        main_layout.add_widget(top_bar)

        # Search bar
        search_bar = TextInput(hint_text="Search", size_hint=(1, 0.1), multiline=False)
        main_layout.add_widget(search_bar)

        # Flashcard grid
        flashcard_grid = GridLayout(cols=3, spacing=10, size_hint=(1, 0.7))

        # Example flashcard sets-------------------
        sets = csv_file_names
        for set_name in sets:
            card = BoxLayout(orientation="vertical", padding=5, spacing=5, size_hint=(None, None), size=(200, 100))
            card_label = Label(text=set_name, halign="center", valign="middle")
            card_label.bind(size=card_label.setter('text_size'))
            open_button = Button(text="Open", size_hint=(1, 0.3), background_color=(0, 0, 1, 1))
            open_button.bind(on_release=lambda instance, name=set_name: self.open_set(name))
            card.add_widget(card_label)
            card.add_widget(open_button)
            flashcard_grid.add_widget(card)

        main_layout.add_widget(flashcard_grid)

        # Create set button
        create_set_button = Button(text="CREATE SET", size_hint=(1, 0.1), background_color=(0, 0, 1, 1))
        create_set_button.bind(on_release=self.open_create_set_popup)
        main_layout.add_widget(create_set_button)

        self.add_widget(main_layout)

    def open_set(self, set_name):
        
        # Get just the name of the file without the extension
        set_name_without_extension = os.path.splitext(set_name)[0]

        # Save the name into Title.json
        self.save_to_json(set_name_without_extension)
        self.manager.current = "CreateFlash"
        self.manager.get_screen("CreateFlash")

        # Print the saved name to verify
        print(f"Saved {set_name_without_extension} to Title.json")

    def save_to_json(self, name):
        title_data = name


        # Check if Title.json exists, create it if not
        if not os.path.exists("Title.json"):
            with open("Title.json", "w") as json_file:
                json.dump(title_data, json_file)
        else:
            # Save the data to the existing Title.json
            with open("Title.json", "w") as json_file:
                json.dump(title_data, json_file)

    def open_create_set_popup(self, instance):
        popup = CreateSetPopup()
        popup.open()


    

#____
    

class CreatingSET(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        # Create set button
        create_set_button = Button(text="CREATE SET", size_hint=(1, 0.1), background_color=(0, 0, 1, 1))

        
        create_set_button.bind(on_release=self.open_create_set_popup)
        main_layout.add_widget(create_set_button)

        self.add_widget(main_layout)




 
