#!/python_virt_env_3.9/bin/python
from kivy.config import Config
# Config.set('graphics', 'resizable', 1)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from screeninfo import get_monitors
from kivy.uix.screenmanager import *
from kivy.uix.screenmanager import ScreenManager
from kivy.interactive import InteractiveLauncher
# from app.app_classes.welcome_page import Welcome_Page_M
# from app.app_classes.home_page import Home_Page_M
# from app.app_classes.clock_page import Clock_Page_M
from app.app_classes.timer_page import Timer_Page_M
from app.app_classes.HB_Image_M import HB_Image_M
from app.app_classes.HB_Label_M import HB_Label_M
from app.app_classes.HB_Spacer_M import HB_Spacer_M
# from app.app_classes.HB_Checkbox_M import HB_Checkbox_M
from app.app_classes.HB_TextInput_M import HB_TextInput_M
from app.app_classes.HB_GridLayout_M import HB_GridLayout_M
# from app.app_classes.HB_CoverImage_M import HB_CoverImage_M

# Builder.load_file("app_ui/welcome_page.kv")
# Builder.load_file("app_ui/home_page.kv")
# Builder.load_file("app_ui/clock_page.kv")
Builder.load_file("app/app_ui/timer_page.kv")
Builder.load_file("app/app_ui/root_widget.kv")

# ------------------------------------------------------------------------------- #
#                                                                                 #
#                                   Welcome Class                                 #
#                                                                                 #
# ------------------------------------------------------------------------------- #
# class Welcome_Page(Welcome_Page_M):
#     pass

# ------------------------------------------------------------------------------- #
#                                                                                 #
#                                  Home_Page Class                                #
#                                                                                 #
# ------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------- #
#                                                                                 #
#                                 Clock_Page Class                                #
#                                                                                 #
# ------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------- #
#                                                                                 #
#                                 Timer_Page Class                                #
#                                                                                 #
# ------------------------------------------------------------------------------- #
class Timer_Page(Timer_Page_M):
    pass

# ------------------------------------------------------------------------------- #
#                                                                                 #
#                                  HB_Label Class                                 #
#                                                                                 #
# ------------------------------------------------------------------------------- #
class HB_Label(HB_Label_M):
    pass

# ------------------------------------------------------------------------------- #
#                                                                                 #
#                                  HB_Image Class                                 #
#                                                                                 #
# ------------------------------------------------------------------------------- #
class HB_Image(HB_Image_M):
    pass

# ------------------------------------------------------------------------------- #
#                                                                                 #
#                                  HB_Image Class                                 #
#                                                                                 #
# ------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------- #
#                                                                                 #
#                                  HB_Spacer Class                                #
#                                                                                 #
# ------------------------------------------------------------------------------- #
class HB_Spacer(HB_Spacer_M):
    pass

# ------------------------------------------------------------------------------- #
#                                                                                 #
#                                  HB_Image Class                                 #
#                                                                                 #
# ------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------- #
#                                                                                 #
#                                 HB_TextInput Class                              #
#                                                                                 #
# ------------------------------------------------------------------------------- #
class HB_TextInput(HB_TextInput_M):
    pass

# ------------------------------------------------------------------------------- #
#                                                                                 #
#                                 HB_GridLayout Class                             #
#                                                                                 #
# ------------------------------------------------------------------------------- #
class HB_GridLayout(HB_GridLayout_M):
    pass

# ------------------------------------------------------------------------------- #
#                                                                                 #
#                                 Root Widget Class                               #
#                                                                                 #
# ------------------------------------------------------------------------------- #
class Root_Widget(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = SlideTransition()

# ------------------------------------------------------------------------------- #
#                                                                                 #
#                                  Main App  Class                                #
#                                                                                 #
# ------------------------------------------------------------------------------- #
class Main_App(MDApp):
    # Main_App is the entire app
    # Main_App has its own custom parameters, which are the following...
    #
    # +--------------------------------------------------------------------------------+
    # |                                                                                |
    # | mouse_resize: this param is bool. This determines if the mouse can change size |
    # |                of the window.
    # |                                                                                |
    # | app_title: this param is an string. This determines the title of the app.      |
    # |                                                                                |
    # | app_size: this param is a tuple. This determines the size of the window.       |
    # |                                                                                |
    # | app_icon: this param is a string. This determines the icon used by the app.    |
    # |                                                                                |
    # +--------------------------------------------------------------------------------+

    # init function
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mouse_resize = False
        self.app_size = (1000, 700)
        self.app_title = "TecKnowfy Timer"
        self.app_icon = "app/app_media/icon.icns"

    # build function
    def build(self):
        Window.bind(on_resize = self.resize_window)
        Window.size = self.app_size
        Window.minimum_height = 500
        Window.minimum_width = 400
        Window.allow_screensaver = False
        self.title = self.app_title
        self.icon = self.app_icon
        self.center_window()
        self.current_i = 0
        Clock.schedule_interval(self.update, 1)
        return Root_Widget()

    def update(self, *args):
        # self.name.text = str(self.current_i)
        self.current_i += 1
        if self.current_i >= 50:
            Clock.unschedule(self.update)

    # resize_window function
    def resize_window(self, *args):
        if not self.mouse_resize: Window.size = self.app_size

    # center_window function
    def center_window(self):
        Window.left = (get_monitors()[0].width - self.app_size[0]) / 2
        Window.top = (get_monitors()[0].height - self.app_size[1]) / 2

# ------------------------------------------------------------------------------- #
#                                                                                 #
#                                   Run App  Code                                 #
#                                                                                 #
# ------------------------------------------------------------------------------- #
if __name__ == "__main__":
    Main_App().run()