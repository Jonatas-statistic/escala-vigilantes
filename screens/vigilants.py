from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from kivy.properties import StringProperty

from database.db_functions import get_vigilants_names, update_names


class VigilantName(BoxLayout):
    letter = StringProperty('')
    name = StringProperty('')


class VigilantsPage(BoxLayout):
    
    def __init__(self, *args, **kwargs):
        super(VigilantsPage, self).__init__(*args, **kwargs)
        letters = 'ABCDE'
        names = get_vigilants_names()
        for letter, name in zip(letters, names):
            self.add_widget(VigilantName(letter=letter, name=name[0]))


class VigilantsScreen(Screen):
    
    def update_vigilants_names(self):
        """Update first five names to vigilats table
        :param names: list of strings with vigilants names
        :return:
        """
        names = []
        for child in self.ids.vigilants.children[::-1]:
            names.append(child.ids.name_imput.text)
        update_names(names)