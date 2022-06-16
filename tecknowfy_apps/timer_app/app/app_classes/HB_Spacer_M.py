from kivy.uix.boxlayout import BoxLayout

# ------------------------------------------------------------------------------- #
#                                                                                 #
#                               HB_Spacer_M Class                                 #
#                                                                                 #
# ------------------------------------------------------------------------------- #
class HB_Spacer_M(BoxLayout):
    # HB_Spacer_M is a BoxLayout that is meant to be space
    # HB_Spacer_M does have its own custom parameters, which are the following...
    #
    # +--------------------------------------------------------------------------------+
    # |                                                                                |
    # | height: this param is an int or float. It declares the height of the space     |
    # |                                                                                |
    # +--------------------------------------------------------------------------------+
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, None)
        self.height = 100 
