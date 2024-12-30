from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore
from kivy.logger import Logger


#Per file is one view section (This code will follow hiercictal structure




#__________________Built In modules_________________________

import csv,os,glob

#--------Extra USer Modules-------------
import submaking



#Code for the view
import study
from study import Studies,CreateSetPopup

#code for creating flashcards
import making
from making import CreateFlashcard


class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)

        title = Label(
            text="STUDY PRO (BETA UI)", 
            font_size=32, 
            size_hint=(1, 0.2),
            halign='center',
            valign='middle'
        )
        title.bind(size=title.setter('text_size'))
        layout.add_widget(title)

        button_layout = BoxLayout(orientation='vertical', spacing=20, size_hint=(1, 0.5))

        play_button = Button(
            text="Play",
            font_size=24,
            size_hint=(1, None),
            height=60,
            background_normal='',
            background_color=(0, 0, 0, 1),
            color=(1, 1, 1, 1)
        )
        play_button.bind(on_release=lambda x: setattr(self.manager, 'current', 'play'))

        settings_button = Button(
            text="Settings",
            font_size=24,
            size_hint=(1, None),
            height=60,
            background_normal='',
            background_color=(0, 0, 0, 1),
            color=(1, 1, 1, 1)
        )
        settings_button.bind(on_release=lambda x: setattr(self.manager, 'current', 'settings'))

        exit_button = Button(
            text="Exit",
            font_size=24,
            size_hint=(1, None),
            height=60,
            background_normal='',
            background_color=(0, 0, 0, 1),
            color=(1, 1, 1, 1)
        )
        exit_button.bind(on_release=self.Closing)

        button_layout.add_widget(play_button)
        button_layout.add_widget(settings_button)
        button_layout.add_widget(exit_button)

        layout.add_widget(button_layout)
        self.add_widget(layout)

    def Closing(self, obj):
        App.get_running_app().stop()
        Window.close()
        


# COde for the play Screen
class PlayScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)

        title = Label(
            text="Play",
            font_size=32,
            size_hint=(1, 0.2),
            halign='center',
            valign='middle'
        )
        title.bind(size=title.setter('text_size'))
        layout.add_widget(title)

        button_grid = BoxLayout(orientation='horizontal', spacing=20, size_hint=(1, 0.6))

        # Import Button
        ImportButton = Button(
            text="Import Card",
            font_size=24,
            size_hint=(0.4, None),
            height=60,
            background_normal='',
            background_color=(0, 0, 0, 1),
            color=(1, 1, 1, 1)
        )
        ImportButton.bind(on_release=lambda x: print("Import Working"))

        # Use Button
        UseButton = Button(
            text="Use Card",
            font_size=24,
            size_hint=(0.4, None),
            height=60,
            background_normal='',
            background_color=(0, 0, 0, 1),
            color=(1, 1, 1, 1)
        )
        UseButton.bind(on_release=lambda x: print("Use Working"))

        # Create Button
        MakingButton = Button(
            text="Create Card",
            font_size=24,
            size_hint=(0.4, None),
            height=60,
            background_normal='',
            background_color=(0, 0, 0, 1),
            color=(1, 1, 1, 1)
        )
        MakingButton.bind(on_release=lambda x: setattr(self.manager, 'current', 'Studying'))
        

        # Podcast Button
        PodButton = Button(
            text="Podcasting",
            font_size=24,
            size_hint=(0.4, None),
            height=60,
            background_normal='',
            background_color=(0, 0, 0, 1),
            color=(1, 1, 1, 1)
        )
        PodButton.bind(on_release=lambda x: print("Podcast Working"))

        # Add buttons to the grid
        button_grid.add_widget(ImportButton)
        button_grid.add_widget(UseButton)
        button_grid.add_widget(MakingButton)
        button_grid.add_widget(PodButton)

        layout.add_widget(button_grid)

        # Back Button
        back_button = Button(
            text="Back",
            font_size=24,
            size_hint=(1, None),
            height=60,
            background_normal='',
            background_color=(0, 0, 0, 1),
            color=(1, 1, 1, 1)
        )
        back_button.bind(on_release=lambda x: setattr(self.manager, 'current', 'main'))

        layout.add_widget(back_button)
        self.add_widget(layout)
        
#----------------------------------------Code for the settings
class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)

        title = Label(
            text="Settings", 
            font_size=32, 
            size_hint=(1, 0.2),
            halign='center',
            valign='middle'
        )
        title.bind(size=title.setter('text_size'))
        layout.add_widget(title)

        back_button = Button(
            text="Back",
            font_size=24,
            size_hint=(1, None),
            height=60,
            background_normal='',
            background_color=(0, 0, 0, 1),
            color=(1, 1, 1, 1)
        )
        back_button.bind(on_release=lambda x: setattr(self.manager, 'current', 'main'))

        layout.add_widget(back_button)
        self.add_widget(layout)

class StudyProApp(App):
    def on_stop(self):
        Logger.critical("Good Bye")
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenuScreen(name='main'))
        sm.add_widget(PlayScreen(name='play'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(Studies(name="Studying"))
        sm.add_widget(CreateFlashcard(name="CreateFlash"))
        
        return sm

if __name__ == "__main__":
    StudyProApp().run()
