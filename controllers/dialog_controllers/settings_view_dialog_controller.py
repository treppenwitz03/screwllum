import flet as ft

from services import Database
from views import HomeView
from utils import Preferences

import subprocess

class AppearanceDialogController:
    def __init__(self, page: ft.Page, home_page: HomeView):
        self.page = page
        self.database: Database = page.session.get("database")
        self.home_page = home_page
        self.appearance_dialog = home_page.appearance_dialog
        self.prefs: Preferences = page.session.get("prefs")
        
        # open dialog
        self.home_page.settings_view.appearance_setting.on_click = self.handle_dialog_open
        
        # handle dark mode change
        self.appearance_dialog.on_change = self.change_darkmode
        self.appearance_dialog.accent_change = self.accent_color_changed
    
    def accent_color_changed(self, event: ft.ControlEvent):
        color = event.control.value
        self.prefs.set_preference("accent_color", color)

        self.page.theme = ft.Theme(color_scheme_seed=color, font_family="Product Sans")
        self.page.update()
    
    # change the dark mode setting
    def change_darkmode(self, event: ft.ControlEvent):
        if event.data == "true":
            self.prefs.set_preference("dark_mode", True)
            self.page.theme_mode = ft.ThemeMode.DARK
        else:
            self.prefs.set_preference("dark_mode", False)
            self.page.theme_mode = ft.ThemeMode.LIGHT
        
        self.page.update()
    
    # open the dialog
    def handle_dialog_open(self, event):
        self.appearance_dialog.accent_color_radio.value = self.prefs.get_preference("accent_color", "#8C161E")
        self.appearance_dialog.dark_mode_switch.value = self.prefs.get_preference("dark_mode", False)
        self.home_page.show_appearance_dialog()

class CurrencyDialogController:
    def __init__(self, page: ft.Page, home_page: HomeView):
        self.page = page
        self.database: Database = page.session.get("database")
        self.home_page = home_page
        self.currency_dialog = home_page.currency_dialog
        self.text_values: dict = page.session.get("text_values")
        self.prefs: Preferences = page.session.get("prefs")
        
        # handle events
        self.home_page.settings_view.currency_setting.on_click = self.handle_dialog_open
        self.currency_dialog.on_change = self.change_currency
    
    # change the currency according to setting
    def change_currency(self, currency):
        self.prefs.set_preference("currency", currency)
        self.page.snack_bar = ft.SnackBar(ft.Text(self.text_values["currency_change_success"]))
        self.page.snack_bar.open = True
        self.page.update()
    
    # open dialog
    def handle_dialog_open(self, event: ft.ControlEvent):
        self.currency_dialog.currency_choices.value = self.prefs.get_preference("currency", "PHP")
        self.home_page.show_currency_dialog()

class LanguageDialogController:
    def __init__(self, page: ft.Page, home_page: HomeView):
        self.page = page
        self.database: Database = page.session.get("database")
        self.home_page = home_page
        self.language_dialog = home_page.language_dialog
        self.prefs: Preferences = page.session.get("prefs")

        self.home_page.settings_view.language_setting.on_click = self.handle_dialog_open
        self.language_dialog.on_change = self.change_language
    
    def handle_dialog_open(self, event):
        self.language_dialog.language_choices.value = self.prefs.get_preference("lang", "en")
        self.home_page.show_language_dialog()
    
    def change_language(self, language):
        if (language == self.prefs.get_preference("lang", "en")):
            return

        self.prefs.set_preference("lang", language)
        self.page.window.close()
        subprocess.run(["python", "main.py"])