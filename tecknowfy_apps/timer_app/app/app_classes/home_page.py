import webbrowser 
from kivy.uix.screenmanager import Screen

# ------------------------------------------------------------------------------- #
#                                                                                 #
#                                Home_Page_M Class                                #
#                                                                                 #
# ------------------------------------------------------------------------------- #
class Home_Page_M(Screen):
    # Home_Page_M is a screen module, that can be implemented into any other screen
    # Home_Page_M has custom parameters, which are the following...
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
        self.header_height = 100
        self.header_background = (167/255, 105/255, 255/255, 1)
        self.footer_height = 0
        self.footer_background = (40/255, 40/255, 40/255, 1)

    def sign_up(self):
        # Remember to put a safe condition, if zamerine can't be opened!
        webbrowser.open_new_tab("https://zamerine.com")