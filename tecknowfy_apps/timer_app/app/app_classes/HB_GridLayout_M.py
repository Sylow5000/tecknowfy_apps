from kivy.graphics import Line
from kivy.graphics import Color
from kivy.core.window import Window
from kivy.graphics import RoundedRectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import ButtonBehavior
from app.app_classes.hoverable import HoverBehavior

# ------------------------------------------------------------------------------- #
#                                                                                 #
#                              HB_GridLayout_M Class                              #
#                                                                                 #
# ------------------------------------------------------------------------------- #
class HB_GridLayout_M(HoverBehavior, ButtonBehavior, GridLayout):
    # HB_GridLayout_M is a gridlayout that has hover behaviors and button behaviors
    # HB_GridLayout_M doesn't have any custom parameters
    #
    # +--------------------------------------------------------------------------------+
    # |                                                                                |
    # | radius: this param is an int. This determines the radius of the label          |
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
    # | change_color: this param is a bool. If True, then change the background color  |
    # |                                                                                |
    # | hover_color_b: this param is a tuple. This displays the background color when  |
    # |                 the label is hovered.                                          |
    # |                                                                                |
    # | normal_color_b: this param is a tuple. This displays the background color when |
    # |                  the label is not hovered.                                     |
    # |                                                                                |
    # +--------------------------------------------------------------------------------+
    def __init__(self, **kwargs):
        super(HB_GridLayout_M, self).__init__(**kwargs)
        self.radius = 100
        self.hover = True
        self.change_color = True
        self.hover_cursor = "hand"
        self.normal_cursor = "arrow"
        self.display_outline = False
        self.outline_width = 2
        self.outline_color = (50/255, 50/255, 50/255, 1)
        self.hover_color_b = (50/255, 168/255, 82/255, 1)
        self.normal_color_b = (40/255, 40/255, 40/255, 1)
        self.bind(pos = self.update_widget, size = self.update_widget)

        with self.canvas.before:
            Color(*self.normal_color_b)
            self.rect = RoundedRectangle(pos = self.pos, size = self.size, radius = [self.height / self.radius])

        if self.display_outline:
            with self.canvas.after:
                Color(*self.outline_color)
                Line(rectangle = [self.x, self.y, self.width, self.height], width = self.outline_width)

    # on_enter function
    def on_enter(self, *args):
        # If hover is true, then change cursor to hand
        if self.hover: Window.set_system_cursor(self.hover_cursor)

        # If change_color is true, then change background and text color
        if self.change_color:
            self.canvas.before.clear()
            with self.canvas.before:
                Color(*self.hover_color_b)
                self.rect = RoundedRectangle(pos = self.pos, size = self.size, radius = [self.width / self.radius])

        # Return
        return super().on_enter(*args)

    # on_leave function
    def on_leave(self, *args):
        # If hover is true, then change cursor to hand
        if self.hover: Window.set_system_cursor(self.normal_cursor)
        else: Window.set_system_cursor("arrow")

        # If change_color is true, then change background and text color
        if self.change_color:
            self.canvas.before.clear()
            with self.canvas.before:
                Color(*self.normal_color_b)
                self.rect = RoundedRectangle(pos = self.pos, size = self.size, radius = [self.width / self.radius])

        return super().on_leave(*args)

    # update_widget function
    def update_widget(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.rect.radius = [self.width / self.radius]
        self.canvas.before.clear()
        if self.display_outline: self.canvas.after.clear()

        with self.canvas.before:
            Color(*self.normal_color_b)
            self.rect = RoundedRectangle(pos = self.pos, size = self.size, radius = [self.height / self.radius])

        if self.display_outline:
            with self.canvas.after:
                Color(*self.outline_color)
                Line(rectangle = [self.x, self.y, self.width, self.height], width = self.outline_width)