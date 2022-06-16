from decimal import *
from kivy.clock import Clock
from kivy.graphics import Color
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.button import ButtonBehavior
from kivy.graphics import RoundedRectangle
from app.app_classes.hoverable import HoverBehavior

# ------------------------------------------------------------------------------- #
#                                                                                 #
#                                 HB_Label_M Class                                #
#                                                                                 #
# ------------------------------------------------------------------------------- #
class HB_Label_M(ButtonBehavior, HoverBehavior, Label):
    # HB_Label_M is a combination between the Label widget and the Button widget with hover behaviors
    # HB_Label_M does have its own custom parameters, which are the following...
    #
    # +--------------------------------------------------------------------------------+
    # |                                                                                |
    # | radius: this param is an int. This determines the radius of the label          |
    # |                                                                                |
    # | hover: this param is a bool. If True, then change the cursor to a hand else    |
    # |         turn it to an arrow.                                                   |
    # |                                                                                |
    # | font_divider: this param is a list. This will give the size of the text        |
    # |                                                                                |
    # | responsive_text: this param is a bool. If True, then the text will change size |
    # |                   according to the parent element's size                       |
    # |                                                                                |
    # | minimum_text_size: this param is a bool. If True, the size of the label will   |
    # |                     be the size of the text                                    |
    # |                                                                                |
    # | static_font_size: this param is an int. This is the font size, if text not     |
    # |                    responsive. WARNING: Use instead of "font_size"!            |
    # |                                                                                |
    # | normal_cursor: this param is a string. When hovered it will display the cursor |
    # |                that is set. By default it is set to arrow, but you can change  |
    # |                it to any other cursor type such as: hand, ibeam, etc.          |
    # |                                                                                |
    # | hover_cursor: this param is a string. When hovered it will display the cursor  |
    # |                that is set. By default it is set to hand, but you can change   |
    # |                it to any other cursor type such as: arrow, ibeam, etc.         |
    # |                                                                                |
    # | change_color: this param is a bool. If True, then change the background and    |
    # |                text color.                                                     |
    # |                                                                                |
    # | hover_color_t: this param is a tuple. This displays the color of the text when |
    # |                 hovered.                                                       |
    # |                                                                                |
    # | normal_color_t: this param is a tuple. This displays the color of the text not |
    # |                  hovered.                                                      |
    # |                                                                                |
    # | hover_color_b: this param is a tuple. This displays the background color when  |
    # |                 the label is hovered.                                          |
    # |                                                                                |
    # | normal_color_b: this param is a tuple. This displays the background color when |
    # |                  the label is not hovered.                                     |
    # |                                                                                |
    # +--------------------------------------------------------------------------------+

    # init function
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.radius = 100
        self.hover = True
        self.change_color = True
        self.static_font_size = 30
        self.responsive_text = True
        self.hover_cursor = "hand"
        self.normal_cursor = "arrow"
        self.font_divider = ["/", 5]
        self.minimum_text_size = False
        self.hover_color_t = (1, 1, 1, 1)
        self.normal_color_t = (0, 0, 0, 1)
        self.hover_color_b = (50/255, 168/255, 82/255, 1)
        self.normal_color_b = (40/255, 40/255, 40/255, 1)
        self.bind(pos = self.update_widget, size = self.update_widget)
        with self.canvas.before:
            Color(*self.normal_color_b)
            self.rect = RoundedRectangle(pos = self.pos, size = self.size, radius = [self.width / self.radius])
        Clock.schedule_once(self.update_widget, 4)

    # on_enter function
    def on_enter(self, *args):
        # If hover is true, then change cursor to hand
        if self.hover: 
            Window.set_system_cursor(self.hover_cursor)

        # If change_color is true, then change background and text color
        if self.change_color:
            self.canvas.before.clear()
            self.color = self.hover_color_t
            with self.canvas.before:
                Color(*self.hover_color_b)
                self.rect = RoundedRectangle(pos = self.pos, size = self.size, radius = [self.width / self.radius])

        # Return
        return super().on_enter(*args)

    # on_leave function
    def on_leave(self, *args):
        # If hover is true, then change cursor to hand
        if self.hover: 
            Window.set_system_cursor(self.normal_cursor)

        # If change_color is true, then change background and text color
        if self.change_color:
            self.canvas.before.clear()
            self.color = self.normal_color_t
            with self.canvas.before:
                Color(*self.normal_color_b)
                self.rect = RoundedRectangle(pos = self.pos, size = self.size, radius = [self.width / self.radius])

        return super().on_leave(*args)

    # update_widget function
    def update_widget(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.rect.radius = [self.width / self.radius]
        if self.minimum_text_size: self.size = self.texture_size
        if self.responsive_text: self.font_size = self.calculate_font_size()
        if not self.responsive_text: self.font_size = self.static_font_size
        self.canvas.before.clear()
        self.color = self.normal_color_t
        with self.canvas.before:
            Color(*self.normal_color_b)
            self.rect = RoundedRectangle(pos = self.pos, size = self.size, radius = [self.width / self.radius])        

    # calculate_font_size function
    def calculate_font_size(self):
        if self.font_divider[0] == "+": return self.width + self.font_divider[1]
        if self.font_divider[0] == "-": return self.width - self.font_divider[1]
        if self.font_divider[0] == "*": return self.width * self.font_divider[1]
        if self.font_divider[0] == "/": return self.width / self.font_divider[1]

