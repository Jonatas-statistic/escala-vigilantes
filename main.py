from kivy.app import App

from kivy.uix.screenmanager import ScreenManager
from kivy.properties import (
    BooleanProperty, NumericProperty, StringProperty
)

from screens.menu import MenuScreen
from screens.vigilants import VigilantsScreen
from screens.calendar import CalendarScreen
from screens.day import DayScreen

from database.db_functions import create_tables, insert_letters


class EscalaApp(App):
    # ScreenDay's date
    day = NumericProperty(None)
    month = NumericProperty(None)
    year = NumericProperty(None)

    # screen manager
    sm = ScreenManager()

    def build(self):
        try:
            create_tables()
        except:
            print('Error! Cannot create a database connection.')
        
        try:
            insert_letters()
        except:
            print('Error! Cannot insert vigilants letters in database.')
            
        self.sm.add_widget(MenuScreen(name='menu'))
        self.sm.add_widget(VigilantsScreen(name='vigilants'))
        self.sm.add_widget(CalendarScreen(name='calendar'))
        self.sm.add_widget(DayScreen(name='day'))

        return self.sm



if __name__ == '__main__':
    EscalaApp().run()
