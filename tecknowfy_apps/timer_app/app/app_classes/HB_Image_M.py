from kivy.core.window import Window
from kivy.uix.image import AsyncImage
from kivy.uix.button import ButtonBehavior
from app.app_classes.hoverable import HoverBehavior

# ------------------------------------------------------------------------------- #
#                                                                                 #
#                                 HB_Image_M Class                                #
#                                                                                 #
# ------------------------------------------------------------------------------- #
class HB_Image_M(ButtonBehavior, HoverBehavior, AsyncImage):
    # HB_Image_M is a combination between the Image widget and the Button widget with hover behaviors
    # HB_Image_M does have its own custom parameters, which are the following...
    #
    # +--------------------------------------------------------------------------------+
    # |                                                                                |
    # | hover: this param is a bool. If True, then change the cursor to a hand else    |
    # |         turn it to an arrow.                                                   |
    # |                                                                                |
    # | normal_cursor: this param is a string. When hovered it will display the cursor |
    # |                that is set. By default it is set to arrow, but you can change  |
    # |                it to any other cursor type such as: hand, ibeam, etc.          |
    # |                                                                                |
    # | hover_cursor: this param is a string. When hovered it will display the cursor  |
    # |                that is set. By default it is set to hand, but you can change   |
    # |                it to any other cursor type such as: arrow, ibeam, etc.         |
    # |                                                                                |
    # | change_image: this param is a bool. If True, then change the image             |
    # |                                                                                |
    # | normal_image: this param is a string. When not hovered it will display the     |
    # |                image that is set.                                              |
    # |                                                                                |
    # | hover_image: this param is a string. When hovered it will display the image    |
    # |                that is set.                                                    |
    # |                                                                                |
    # +--------------------------------------------------------------------------------+

    # init function
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hover = True
        self.change_image = True
        self.hover_image = None
        self.normal_image = None
        self.hover_cursor = "hand"
        self.normal_cursor = "arrow"
        self.bind(texture = self._update_texture_filters)

    # update_texture_filters
    def _update_texture_filters(self, image, texture):
        texture.mag_filter = 'nearest'

    # on_enter function
    def on_enter(self, *args):
        # If hover is true, then change cursor to hand
        if self.hover: Window.set_system_cursor(self.hover_cursor)

        # If change_image is true, then change background and text color
        if self.change_image: self.source = self.hover_image

        # Return
        return super().on_enter(*args)

    # on_leave function
    def on_leave(self, *args):
        # If hover is true, then change cursor to hand
        if self.hover: Window.set_system_cursor(self.normal_cursor)

        # If change_image is true, then change background and text color
        if self.change_image: self.source = self.normal_image

        # Return
        return super().on_leave(*args)