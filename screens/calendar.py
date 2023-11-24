from datetime import date
from calendar import Calendar

from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

from kivy.properties import (
    BooleanProperty, NumericProperty, StringProperty
)

from database.db_functions import get_vigilants_by_date


MONTHS = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril',
    'Maio', 'Junho', 'Julho', 'Agosto',
    'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]


class DayButton(Button):
    is_weekday = BooleanProperty(False)
    is_holiday = BooleanProperty(False)
    day = NumericProperty(None)
    
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

    def __init__(self, *args, **kwargs):
        super(DayButton, self).__init__(*args, **kwargs)
        self.date = None

    def update_date(self, mdate: date):
        """update self.date"""
        self.date = mdate
        self.day = mdate.day

    def update_vigilants(self):
        vigilants_by_date = get_vigilants_by_date(self.date)
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
                is_holiday
            ) = vigilants_by_date

    def transfer_changes(self, day_screen):
        """Transfer to DayScreen all informations.
        :param day_screen: DayScreen Widget
        :return:
        """
        pass


class CalendarPage(GridLayout):
    month = NumericProperty(None)
    year = NumericProperty(None)
    text_month_year = StringProperty('')
    
    def __init__(self, *args, **kwargs):
        super(CalendarPage, self).__init__(*args, **kwargs)
        
        #number of columns
        self.cols = 7
        
        # set date as today
        today = date.today()
        self.month = today.month
        self.year = today.year

        # add day buttons 
        for day in range(1, 36):
            self.add_widget(DayButton())

        # set day buttons about today date
        self.update_day_buttons()

    def update_day_buttons(self):
        # write the month and year on top
        self.write_month_year() # update text_month_year
        
        # draw the days buttons
        c = Calendar(6)
        monthdates = c.itermonthdates(year=self.year, month=self.month)

        for mdate, child in zip(monthdates, self.children[::-1]):
            # set if it' a weekday
            if mdate.weekday() in (5, 6): # test if it is a weekday
                child.is_weekday = True
            child.update_date(mdate)

            # get vigilants names and letters by date
            child.update_vigilants()
        
       
    def write_month_year(self):
        month_name = MONTHS[self.month - 1]
        self.text_month_year = f'{month_name} de {self.year}'
    
    def go_to_last_month(self):
        if self.month == 1:
            self.year -= 1
            self.month = 12
        else:
            self.month -= 1
        self.update_day_buttons()

    def go_to_next_month(self):
        if self.month == 12:
            self.year += 1
            self.month = 1
        else:
            self.month += 1
        self.update_day_buttons()


class CalendarScreen(Screen):
    pass