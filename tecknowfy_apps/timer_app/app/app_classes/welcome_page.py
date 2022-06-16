from kivy.uix.screenmanager import Screen

# ------------------------------------------------------------------------------- #
#                                                                                 #
#                                Welcome_Page_M Class                             #
#                                                                                 #
# ------------------------------------------------------------------------------- #
class Welcome_Page_M(Screen):
    # Welcome_Page_M is a screen module, that can be implemented into any other screen
    # Welcome_Page_M has no custom parameters
    #
    # +--------------------------------------------------------------------------------+
    # |                                                                                |
    # +--------------------------------------------------------------------------------+

    def home_page_gt(self):
        self.manager.switch_to(self.manager.get_screen("Home_Page"), direction='left', duration = .5)

        