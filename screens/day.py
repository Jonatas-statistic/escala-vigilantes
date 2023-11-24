from kivy.uix.screenmanager import Screen

from kivy.properties import (
    BooleanProperty, NumericProperty, StringProperty
)

from database.db_functions import get_vigilants_by_date, set_vigilants_by_date
from datetime import date


class DayScreen(Screen):
    is_weekday = BooleanProperty(False)
    is_holiday = BooleanProperty(False)
    day = NumericProperty(None)
    month = NumericProperty(None)
    year = NumericProperty(None)
    
    # night: vigilant 1
    letter_night_1 = StringProperty('')
    name_night_1 = StringProperty('')
    
    # night: vigilant 2
    letter_night_2 = StringProperty('')
    name_night_2 = StringProperty('')
    
    # day: vigilant 1
    letter_day_1 = StringProperty('')
    name_day_1 = StringProperty('')

    # day: vigilant 2
    letter_day_2 = StringProperty('')
    name_day_2 = StringProperty('')

    def __init__(self, *args, **kw):
        super(DayScreen, self).__init__(*args, **kw)

        # get day data
        self.get_day_data()

    def get_day_data(self):
        if self.day is not None:
            mdate = date(self.year, self.month, self.day)
            vigilants_by_date = get_vigilants_by_date(mdate)
            if vigilants_by_date is not None:
                (
                    self.letter_night_1,
                    self.name_night_1,
                    self.letter_night_2,
                    self.name_night_2,
                    self.letter_day_1,
                    self.name_day_1,
                    self.letter_day_2,
                    self.name_day_2,
                    self.is_holiday
                ) = vigilants_by_date
            self.is_weekday = True if mdate.weekday() > 4 else False        

    def save_changes(self):
            """Save changes in the day."""
            set_vigilants_by_date(
                mdate = self.date,
                vigilant_night1 = self.letter_night_1,
                vigilant_night2 = self.letter_night_2,
                vigilant_day1 = self.letter_day_1,
                vigilant_day2 = self.letter_day_2,
                is_holiday = self.is_holiday
            )

    