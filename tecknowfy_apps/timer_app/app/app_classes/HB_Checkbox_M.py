from kivy.uix.image import AsyncImage
from kivy.uix.button import ButtonBehavior

# ------------------------------------------------------------------------------- #
#                                                                                 #
#                              HB_CheckBox_M Class                                #
#                                                                                 #
# ------------------------------------------------------------------------------- #
class HB_Checkbox_M(ButtonBehavior, AsyncImage):
    # HB_CheckBox_M is a combination between the Image widget and the Button widget
    # HB_CheckBox_M does have its own custom parameters, which are the following...
    #
    # +--------------------------------------------------------------------------------+
    # |                                                                                |
    # | press: this param is a bool. If False, then prevent clicking.                  |
    # |                                                                                |
    # | active: this param is a bool. If toggles between active and not active.        |
    # |                                                                                |
    # | normal_image: this param is a string. This displays the image when not active. |
    # |                                                                                |
    # | active_image: this param is a string. This displays the image when active.     |
    # |                                                                                |
    # +--------------------------------------------------------------------------------+   
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.press = True
        self.active = False
        self.active_image = None
        self.normal_image = None

    def on_press(self):
        if not self.press:
            return

        if self.active:
            self.active = False
            self.source = self.normal_image
        else:
            self.active = True
            self.source = self.active_image

        return super().on_press()
