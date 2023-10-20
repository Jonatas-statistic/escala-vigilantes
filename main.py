from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from kivy.uix.button import Button

from kivy.properties import (
    ObjectProperty, StringProperty
)


##### WIDGETS #####
class MenuButton(Button):
    pass


class VigilantName(BoxLayout):
    letter = StringProperty('')
    name = StringProperty('')


class DayButton(Button):
    pass
###################

##### PAGES #####
class MenuPage(BoxLayout):
    pass


class VigilantsPage(BoxLayout):
    
    def __init__(self, *args, **kwargs):
        super(VigilantsPage, self).__init__(*args, **kwargs)
        letters = 'ABCDE'
        for letter in letters:
            self.add_widget(VigilantName(letter=letter))


class CalendarPage(GridLayout):
    
    def __init__(self, *args, **kwargs):
        super(CalendarPage, self).__init__(*args, **kwargs)
        self.cols = 7
        for day in range(1, 36):
            self.add_widget(DayButton())
#################

class EscalaLayout(BoxLayout):
    current_page = ObjectProperty(None)


class EscalaApp(App):
    def build(self):
        return CalendarPage()


if __name__ == '__main__':
    EscalaApp().run()
