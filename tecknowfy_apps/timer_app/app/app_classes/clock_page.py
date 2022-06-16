import os
import json
import socket
import geocoder
import requests
from kivy.graphics import Color
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivymd.uix.card import MDCard
from kivy.graphics import Rectangle
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import RoundedRectangle
from kivy.effects.scroll import ScrollEffect
from kivy.uix.relativelayout import RelativeLayout


api_key = str(os.environ.get('api_key_country', '-1'))
data = requests.get(f'https://api.ipdata.co/{socket.gethostname()}?api-key={api_key}').json()
print(data)


# g = geocoder.ip(socket.gethostname())
# print(g)
# print(g.lat)

class BaseShadowWidget(Widget):
    pass


class DeprecatedShadowWidget(MDCard, BaseShadowWidget):
    '''Deprecated shadow rendering. Doesn't require a lot of resources.'''

# ------------------------------------------------------------------------------- #
#                                                                                 #
#                                 Clock_Page_M Class                              #
#                                                                                 #
# ------------------------------------------------------------------------------- #
class Clock_Page_M(Screen):
    # Clock_Page_M is a screen module, that can be implemented into any other screen
    # Clock_Page_M has no custom parameters
    #
    # +--------------------------------------------------------------------------------+
    # |                                                                                |
    # | header_height: This param is an int or float. This declares the height of the  |
    # |                 header                                                         |
    # |                                                                                |
    # | header_background: This param is a string or tuple. This declares the          |
    # |                     background of the header. It can be image or color         |
    # |                                                                                |
    # | footer_height: This param is an int or float. This declares the height of the  |
    # |                 footer                                                         |
    # |                                                                                |
    # | footer_background: This param is a string or tuple. This declares the          |
    # |                     background of the footer. It can be image or color         |
    # +--------------------------------------------------------------------------------+
    
    def __init__(self, **kw):
        super().__init__(**kw)
        self.world_countries = []
        self.header_height = 100
        self.header_background = (167/255, 105/255, 255/255, 1)
        self.footer_height = 100
        self.footer_background = (40/255, 40/255, 40/255, 1)
        with open("app_media/world_countries.json") as JsonFile:
            Json = json.load(JsonFile)
        JsonFile.close()



    def menu(self, instance):
        self.display_world_menu() if instance.focus else self.hide_world_menu()

    def hide_world_menu(self):
        self.ids.world_country_menu_layout.clear_widgets()

    def display_world_menu(self):
        # create the menu
        menu_container = GridLayout()
        menu_container.id = "world_menu_container"
        menu_container.cols = 1
        menu_container.rows = 2
        menu_container.height = 50
        menu_container.size_hint = (1, None)
        menu_container.auto_bring_to_front = True

        # create the shadow container
        shadow_container = GridLayout()
        shadow_container.cols = 1

        # create relative shadow container
        relative_shadow_container = RelativeLayout()

        # create the shadow
        shadow = DeprecatedShadowWidget()
        shadow.id = "world_countries_shadow"
        shadow.size_hint = (None, None)
        shadow.width = 350
        shadow.height = 300
        shadow.elevation = 36
        shadow.pos_hint = {'center_x': .67, "top": 1}

        # create world countries container
        world_countries_container = GridLayout()
        world_countries_container.cols = 1

        # create the relativer world countries container
        relative_world_countries_container = RelativeLayout()

        # create a border for the scrollview
        world_countries_scrollview_border = GridLayout()
        world_countries_scrollview_border.padding = (2, 2)
        world_countries_scrollview_border.cols = 1
        world_countries_scrollview_border.width = 454
        world_countries_scrollview_border.height = 354
        world_countries_scrollview_border.size_hint = (None, None)
        world_countries_scrollview_border.pos_hint = {"center_x": .72, "top": 3}
        with world_countries_scrollview_border.canvas.before:
            Color(150/255, 150/255, 150/255, 1)
            world_countries_scrollview_border.rect = Rectangle(pos = world_countries_scrollview_border.pos, size = world_countries_scrollview_border.size, radius = [2])
        world_countries_scrollview_border.bind(pos = self.update_widget, size = self.update_widget)

        # create the scroll view of the world countries and city
        world_countries_scrollview = ScrollView()
        world_countries_scrollview.id = "world_countries_scrollview"
        world_countries_scrollview.width = 450
        world_countries_scrollview.height = 350
        world_countries_scrollview.do_scroll_x = False
        world_countries_scrollview.do_scroll_y = True
        world_countries_scrollview.size_hint = (None, None)
        world_countries_scrollview.effect_cls = ScrollEffect

        # create the container for the list of world countries
        world_countries_list = GridLayout()
        world_countries_list.id = "view_countries"
        world_countries_list.cols = 1
        world_countries_list.spacing = 20
        world_countries_list.padding = 20
        world_countries_list.size_hint = (1, None)
        world_countries_list.height = world_countries_list.minimum_height
        world_countries_list.bind(minimum_height = world_countries_list.setter('height'))
        with world_countries_list.canvas.before:
            Color(240/255, 240/255, 240/255, 1)
            world_countries_list.rect = RoundedRectangle(pos = world_countries_list.pos, size = world_countries_list.size)
        world_countries_list.bind(pos = self.update_widget, size = self.update_widget)

        # create a list of all the world countries in the world
        countries = ["Canada", "USA", "Mexico", "Germany", "Spain", "France", "Italy", "Russia", "China", "Hawaii", "Brazil"]

        # create a label and add each label to the world_countries_list
        for i in range(0, 10):
            world_countries_list.add_widget(Label(text=countries[i],size_hint=(1,None),height=60,color=(0,0,0,1)))

        # add the widgets to create the menu  
        world_countries_scrollview.add_widget(world_countries_list)
        world_countries_scrollview_border.add_widget(world_countries_scrollview)
        relative_world_countries_container.add_widget(world_countries_scrollview_border)
        world_countries_container.add_widget(relative_world_countries_container)    

        relative_shadow_container.add_widget(shadow)
        shadow_container.add_widget(relative_shadow_container)   

        menu_container.add_widget(shadow_container)
        menu_container.add_widget(world_countries_container)

        self.ids.world_country_menu_layout.add_widget(menu_container)




    def update_widget(self, *args):
        args[0].rect.pos = args[0].pos
        args[0].rect.size = args[0].size
        try: args[0].rect.radius = [2]
        except: pass

