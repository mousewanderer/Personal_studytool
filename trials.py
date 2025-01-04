from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.progressbar import ProgressBar
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.animation import Animation
from kivy.lang import Builder
from random import choice

Builder.load_string("""
<GameScreen>:
    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            size_hint_y: 0.1
            Button:
                text: "Back to Menu"
                on_release: app.stop()

        FloatLayout:
            CardLayout:
                id: card
                pos_hint: {"center_x": 0.5, "center_y": 0.6}
                size_hint: 0.7, 0.4

        BoxLayout:
            size_hint_y: 0.2
            spacing: 10
            ProgressBar:
                id: new_progress
                max: root.total_cards
                value: root.new_count
            ProgressBar:
                id: learning_progress
                max: root.total_cards
                value: root.learning_count
            ProgressBar:
                id: reviewing_progress
                max: root.total_cards
                value: root.reviewing_count
            ProgressBar:
                id: mastered_progress
                max: root.total_cards
                value: root.mastered_count
<CardLayout>:
    Label:
        id: front_label
        text: root.front_text
        font_size: 32
        halign: 'center'
        valign: 'middle'
        size_hint: 1, 1
        on_touch_down: root.flip_card()
    Label:
        id: back_label
        text: root.back_text
        font_size: 24
        halign: 'center'
        valign: 'middle'
        size_hint: 1, 1
        opacity: 0
""")

class CardLayout(FloatLayout):
    front_text = StringProperty("Front of Card")
    back_text = StringProperty("Back of Card")

    def flip_card(self):
        anim_out = Animation(opacity=0, duration=0.2)
        anim_in = Animation(opacity=1, duration=0.2)
        if self.ids.front_label.opacity == 1:
            anim_out.bind(on_complete=lambda *args: anim_in.start(self.ids.back_label))
            anim_out.start(self.ids.front_label)
        else:
            anim_out.bind(on_complete=lambda *args: anim_in.start(self.ids.front_label))
            anim_out.start(self.ids.back_label)

class GameScreen(Screen):
    new_count = NumericProperty(5)
    learning_count = NumericProperty(3)
    reviewing_count = NumericProperty(2)
    mastered_count = NumericProperty(1)
    total_cards = NumericProperty(11)

    def on_enter(self):
        self.update_progress_bars()
        self.display_random_card()

    def update_progress_bars(self):
        self.ids.new_progress.value = self.new_count
        self.ids.learning_progress.value = self.learning_count
        self.ids.reviewing_progress.value = self.reviewing_count
        self.ids.mastered_progress.value = self.mastered_count

    def display_random_card(self):
        card_data = {
            "front_text": "Word: Example",
            "back_text": "Description: This is an example card."
        }
        self.ids.card.front_text = card_data["front_text"]
        self.ids.card.back_text = card_data["back_text"]

class FlashcardApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(GameScreen(name="game"))
        return sm

if __name__ == '__main__':
    FlashcardApp().run()
