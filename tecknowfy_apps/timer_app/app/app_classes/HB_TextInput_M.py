from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.button import ButtonBehavior
from app.app_classes.hoverable import HoverBehavior

# ------------------------------------------------------------------------------- #
#                                                                                 #
#                               HB_TextInput_M Class                              #
#                                                                                 #
# ------------------------------------------------------------------------------- #
class HB_TextInput_M(ButtonBehavior, HoverBehavior, TextInput):
    # HB_TextInput_M is a TextInput widget with hover behaviors
    # HB_TextInput_M does have its own custom parameters, which are the following...
    #
    # +--------------------------------------------------------------------------------+
    # |                                                                                |
    # | hover: this param is a bool. If True, then change the cursor to a ibeam else   |
    # |         turn it to an arrow.                                                   |
    # |                                                                                |
    # | font_divider: this param is a tuple. This will *,/,+,- the height by the second|
    # |                parameter. [Eg. font_size = self.height / 2.5]                  |
    # |                                                                                |
    # | alpha: this param is a bool. If True, then the HB_TextInput_M can accept       |
    # |         letters, if False then it can't accept letters.                        |
    # |                                                                                |
    # | numeric: this param is a bool. If True, then the HB_TextInput_M can accept     |
    # |           numbers, if False it can't accept numbers.                           |  
    # |                                                                                |
    # | special_characters: this param is a bool. If True, then the HB_TextInput_M can |
    # |                      accept special characters, if not, then it can't.         |
    # |                                                                                |
    # | normal_cursor: this param is a string. When hovered it will display the cursor |
    # |                that is set. By default it is set to arrow, but you can change  |
    # |                it to any other cursor type such as: hand, ibeam, etc.          |
    # |                                                                                |
    # | hover_cursor: this param is a string. When hovered it will display the cursor  |
    # |                that is set. By default it is set to hand, but you can change   |
    # |                it to any other cursor type such as: arrow, ibeam, etc.         |
    # |                                                                                |
    # | certain_characters: this param is a bool. If True, then the HB_TextInput_M can |
    # |                      accept only certain characters, in the specific_characters|
    # |                      string.                                                   |
    # |                                                                                |
    # | specific_characters: this param is a string. If certain_characters is true,    |
    # |                       then the listed characters in this string can only be    |
    # |                       accepted, nothing else.                                  |
    # |                                                                                |
    # | specify_length: this param is a bool. If True, then the HB_TextInput_M, will   |
    # |                  have a specified length of the length param.                  |
    # |                                                                                |
    # | length: this param in an int. This variable holds how many characters the      |
    # |          HB_TextInput_M can hold.                                              |
    # |                                                                                |
    # | uppercase: this param is a bool. This param will convert all letters to        |
    # |             uppercase.                                                         |
    # |                                                                                |
    # +--------------------------------------------------------------------------------+

    # init function
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.length = 0
        self.alpha = True
        self.hover = True
        self.numeric = True
        self.uppercase = False
        self.responsive_text = True
        self.hover_cursor = "ibeam"
        self.specify_length = False
        self.normal_cursor = "arrow"
        self.font_divider = ["/", 10]
        self.special_characters = True
        self.certain_characters = False
        self.specific_characters = None
        self.NumericCharacters = "0123456789"
        self.SpecialCharacters = "`~!@#$%^&*()-_=+]}[{|:;'\"<,.>?/\\"
        self.AlphaCharacters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.bind(pos = self.update_widget, size = self.update_widget)

    # on_enter function
    def on_enter(self, *args):
        if self.hover: Window.set_system_cursor(self.hover_cursor)  
        return super().on_enter(*args)

    # on_leave function
    def on_leave(self, *args):
        if self.hover: Window.set_system_cursor(self.normal_cursor)  
        return super().on_leave(*args)

    # on_touch_up function
    def on_touch_up(self, touch):
        try: return super().on_touch_up(touch)
        except: return

    # update_widget function
    def update_widget(self, *args):
        if self.responsive_text: self.font_size = self.calculate_font_size()
        # self.padding_y = [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0]
        # self.padding = (40, self.height / 2 - self.font_size / 2)

    # calculate_font_size function
    def calculate_font_size(self):
        if self.font_divider[0] == "+": return self.height + self.font_divider[1]
        if self.font_divider[0] == "-": return self.height - self.font_divider[1]
        if self.font_divider[0] == "*": return self.height * self.font_divider[1]
        if self.font_divider[0] == "/": return self.height / self.font_divider[1]

    # insert_text function
    def insert_text(self, substring, from_undo = False):
        if self.specify_length and len(self.text) >= self.length:
            return

        if self.uppercase and substring in "abcdefghiklmnopqrstuvwxyz":
            substring = substring.upper()

        if self.certain_characters:
            if substring in self.specific_characters:
                return super().insert_text(substring, from_undo = from_undo)

        if self.alpha:
            if substring in self.AlphaCharacters:
                return super().insert_text(substring, from_undo = from_undo)

        if self.numeric:
            if substring in self.NumericCharacters:
                return super().insert_text(substring, from_undo = from_undo)

        if self.special_characters:
            if substring in self.SpecialCharacters:
                return super().insert_text(substring, from_undo = from_undo)