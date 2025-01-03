from flet_route import Params, Basket, Routing, path
import flet as ft

from typing import List

class AbstractView(ft.View):
    route: str = ""
    should_clear: bool = True
    def get_view(self, page: ft.Page, params: Params, basket: Basket):
        pass

class Views(object):
    def __init__(self, page: ft.Page, text_values: dict):
        self.__pages = dict()
        self.flet_page = page
        self.text_values = text_values
        self.routes = []
    
    def __add_page__(self, page: AbstractView):
        current_page = page(self.text_values)
        self.routes.append(path(url=current_page.route, clear=current_page.should_clear, view=current_page.get_view))
        self.__pages[current_page.__class__.__name__] = current_page
    
    def add_pages(self, pages):
        for page in pages:
            self.__add_page__(page)
        
        Routing(page = self.flet_page, app_routes = self.routes)
    
    def get(self, page_name: str):
        return self.__pages[page_name]