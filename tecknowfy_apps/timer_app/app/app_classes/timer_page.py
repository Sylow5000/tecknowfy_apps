import json
import threading
from kivy.clock import Clock, mainthread
from functools import partial
from kivy.graphics import Color
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import RoundedRectangle
from kivy.graphics import Rectangle
from kivy.uix.scrollview import ScrollView
from kivy.effects.scroll import ScrollEffect
from kivy.uix.recycleview import RecycleView
from kivy.uix.relativelayout import RelativeLayout
from numpy import spacing
from app.app_classes.HB_Label_M import HB_Label_M
from app.app_classes.HB_Spacer_M import HB_Spacer_M
from app.app_classes.HB_TextInput_M import HB_TextInput_M
from app.app_classes.HB_GridLayout_M import HB_GridLayout_M



# ------------------------------------------------------------------------------- #
#                                                                                 #
#                                 Timer_Page_M Class                              #
#                                                                                 #
# ------------------------------------------------------------------------------- #
class Timer_Page_M(Screen):
    # Timer_Page_M is a screen module, that can be implemented into any other screen
    # Timer_Page_M has no custom parameters
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
    
    # init function
    def __init__(self, **kw):
        super().__init__(**kw)
        self.editing = False
        self.id_widgets = {}
        self.timer_amount = 1
        self.quit_all_threads = False
        self.timers = {
            "first_timer": {"time": [0, 0, 0], "state": "none", "previous_time": [0, 0, 0]},
            "second_timer": {"time": [0, 0, 0], "state": "none", "previous_time": [0, 0, 0]},
            "third_timer": {"time": [0, 0, 0], "state": "none", "previous_time": [0, 0, 0]}
        }
        self.header_height = 100
        self.header_background = (167/255, 105/255, 255/255, 1)
        self.footer_height = 100
        self.footer_background = (40/255, 40/255, 40/255, 1)
        Clock.schedule_once(self._private_initialize_timer_page, 1)

    # start_timer
    def start_timer(self, *args):
        # Declare variables
        timer_prefix = args[0][:args[0].find("_start_button")]
        hour_text = int(self.id_widgets["{}_hour_textinput".format(timer_prefix)].text)
        minute_text = int(self.id_widgets["{}_minute_textinput".format(timer_prefix)].text)
        second_text = int(self.id_widgets["{}_second_textinput".format(timer_prefix)].text)

        # Check Statements
        if [hour_text, minute_text, second_text] == [0, 0, 0]: return

        # Initialize the timers
        self.timers[timer_prefix]["time"] = [hour_text, minute_text, second_text]
        self.timers[timer_prefix]["previous_time"] = self.timers[timer_prefix]["time"]
        self.timers[timer_prefix]["state"] = "play"

        # Run python code below here...
        pause_button_params = [
            {"id": "{}_pause_button".format(timer_prefix)},
            {"radius": 10},
            {"text": "Pause"},
            {"hover": True},
            {"width": 180},
            {"height": 90},
            {"static_font_size": 30},
            {"responsive_text": False},
            {"minimum_text_size": False},
            {"size_hint": (None, None)},
            {"on_press": partial(self.pause_timer, "{}_pause_button".format(timer_prefix))},
            {"hover_color_b": (75/255, 184/255, 81/255, 1)},
            {"normal_color_b": (148/255, 90/255, 230/255, 1)},
            {"normal_color_t": (1, 1, 1, 1)},
            {"hover_color_t": (1, 1, 1, 1)},
            {"pos_hint": {"center_x": .6, "center_y": .5}},
        ]
        reset_button_params = [
            {"id": "{}_reset_button".format(timer_prefix)},
            {"radius": 10},
            {"text": "Reset"},
            {"hover": True},
            {"width": 180},
            {"height": 90},
            {"static_font_size": 35},
            {"responsive_text": False},
            {"minimum_text_size": False},
            {"size_hint": (None, None)},
            {"on_press": partial(self.reset_timer, timer_prefix)},
            {"normal_color_b": (173/255, 3/255, 3/255, 1)},
            {"hover_color_b": (250/255, 110/255, 110/255, 1)},
            {"normal_color_t": (1, 1, 1, 1)},
            {"hover_color_t": (1, 1, 1, 1)},
            {"pos_hint": {"center_x": .4, "center_y": .5}},
        ]  
        [pause_button, reset_button] = self._private_create_buttons(pause_button_params, reset_button_params)
        print(self.id_widgets)
        self.id_widgets[pause_button.children[0].id] = pause_button.children[0]
        self.id_widgets[reset_button.children[0].id] = reset_button.children[0]
        self.id_widgets.pop("{}_start_button".format(timer_prefix))
        self.id_widgets["{}_button_container".format(timer_prefix)].clear_widgets()
        self.id_widgets["{}_button_container".format(timer_prefix)].cols = 2
        self.id_widgets["{}_button_container".format(timer_prefix)].add_widget(pause_button)
        self.id_widgets["{}_button_container".format(timer_prefix)].add_widget(reset_button)
        thread = threading.Thread(target = partial(self._private_play_timer, timer_prefix))
        thread.start()
        print("\n\n\n\n\n==========================================================================",self.id_widgets)

    # set_timer
    def set_timer(self, instance):
        # Run python code below here...
        self.ids.hour_textinput.text = instance.children[0].children[0].text[:2]
        self.ids.minute_textinput.text = instance.children[0].children[0].text[3:5]
        self.ids.second_textinput.text = instance.children[0].children[0].text[6:]

    # toggle_selected
    def toggle_selected(self, instance):
        # Run python code below here...
        if instance.selected:
            instance.selected = False
            instance.normal_color_b = (160/255, 160/255, 160/255, 1)
            instance.hover_color_b = (180/255, 180/255, 180/255, 1)
            instance.hover = True
        else:
            instance.hover = False
            instance.selected = True
            instance.normal_color_b = (216/255, 181/255, 255/255, 1)
            instance.hover_color_b = (216/255, 181/255, 255/255, 1)

    # toggle_edit_mode
    def toggle_edit_mode(self):
        return
        # Declare variables
        start_button_params = [
            {"radius": 10},
            {"text": "Start"},
            {"hover": True},
            {"width": 300},
            {"height": 110},
            {"static_font_size": 35},
            {"responsive_text": False},
            {"minimum_text_size": False},
            {"size_hint": (None, None)},
            {"on_press": self.start_timer},
            {"hover_color_b": (75/255, 184/255, 81/255, 1)},
            {"normal_color_b": (148/255, 90/255, 230/255, 1)},
            {"normal_color_t": (1, 1, 1, 1)},
            {"hover_color_t": (1, 1, 1, 1)},
            {"pos_hint": {"center_x": .5, "center_y": .5}},
        ]
        edit_button_params = [
            {"id": "edit_button"},
            {"radius": 100},
            {"text": "Edit"},
            {"hover": True},
            {"static_font_size": 30},
            {"responsive_text": False},
            {"minimum_text_size": True},
            {"size_hint": (None, None)},
            {"hover_color_b": (0, 0, 0, 0)},
            {"normal_color_b": (0, 0, 0, 0)},
            {"normal_color_t": (50/255, 50/255, 50/255, 1)},
            {"hover_color_t": (148/255, 90/255, 230/255, 1)},
            {"pos_hint": {"center_x": 0, "center_y": .5}}
        ]
        delete_button_params = [
            {"id": "delete_button"},
            {"radius": 100},
            {"text": "Delete"},
            {"hover": True},
            {"static_font_size": 30},
            {"responsive_text": False},
            {"minimum_text_size": True},
            {"size_hint": (None, None)},
            {"hover_color_b": (0, 0, 0, 0)},
            {"normal_color_b": (0, 0, 0, 0)},
            {"on_press": self.delete_presets},
            {"normal_color_t": (50/255, 50/255, 50/255, 1)},
            {"hover_color_t": (148/255, 90/255, 230/255, 1)},
            {"pos_hint": {"center_x": 0, "center_y": .5}},
        ]

        # Run python code below here...
        self.editing = False if self.editing else True
        for i in range(0, self.timer_amount):
            if i == 0: timer_prefix = "first_timer"
            if i == 1: timer_prefix = "second_timer"
            if i == 2: timer_prefix = "third_timer"
            self.id_widgets["{}_container".format(timer_prefix)].normal_color_b = (205/255, 205/255, 205/255, 1) if self.editing else (1, 1, 1, 1)
            self.id_widgets["{}_label".format(timer_prefix)].normal_color_b = (190/255, 190/255, 190/255, 1) if self.editing else (240/255, 240/255, 240/255, 1)
            self.id_widgets["{}_start_button".format(timer_prefix)].normal_color_b = (108/255, 50/255, 190/255, 1) if self.editing else (148/255, 90/255, 230/255, 1)
            self.id_widgets["{}_start_button".format(timer_prefix)].hover = False if self.editing else True
            self.id_widgets["{}_start_button".format(timer_prefix)].change_color = False if self.editing else True
            self.id_widgets["{}_start_button".format(timer_prefix)].on_press = self._private_useless_function if self.editing else partial(self.start_timer, "{}_start_button".format(timer_prefix))
            self.id_widgets["{}_start_button".format(timer_prefix)].update_widget()
            self.id_widgets["{}_container".format(timer_prefix)].update_widget()
            self.id_widgets["{}_label".format(timer_prefix)].update_widget()

            for j in range(0, 3):
                if j == 0: textinput_name = "hour"
                if j == 1: textinput_name = "minute"
                if j == 2: textinput_name = "second"
                self.id_widgets["{}_{}_textinput".format(timer_prefix, textinput_name)].hover = False if self.editing else True
                self.id_widgets["{}_{}_textinput".format(timer_prefix, textinput_name)].is_focusable = False if self.editing else True
                self.id_widgets["{}_{}_textinput".format(timer_prefix, textinput_name)].selection_color = (0, 0, 0, 0) if self.editing else (0.1843, 0.6549, 0.8313, .5)
        self.ids.body.background_color = (200/255, 200/255, 200/255, 1) if self.editing else (250/255, 250/255, 250/255, 1)
        self.ids.quick_timer_presets.clear_widgets()
        self.ids.quick_timer_presets.cols = 2
        self._private_create_timer_presets(self.editing)
        [edit_button, delete_button] = self._private_create_buttons(edit_button_params if self.editing else start_button_params, delete_button_params if self.editing else None)
        layout = GridLayout()
        layout.cols = 1
        layout.width = 100
        layout.size_hint = (.3, 1)
        layout.add_widget(edit_button)
        layout.add_widget(delete_button)
        # self.ids.timer_button_container.cols = 2 if self.editing else 1
        self.ids.quick_timer_presets.add_widget(layout)
        # if delete_button: self.ids.timer_button_container.add_widget(delete_button) 
        # self.ids.
        # quick_timer_presets
        # self.ids.timer_button_container.clear_widgets()
        # self._private_create_timer_presets(self.editing)
        # [edit_button, delete_button] = self._private_create_buttons(edit_button_params if self.editing else start_button_params, delete_button_params if self.editing else None)
        # self.ids.timer_button_container.cols = 2 if self.editing else 1
        # self.ids.timer_button_container.add_widget(edit_button)
        # if delete_button: self.ids.timer_button_container.add_widget(delete_button) 


        # self.ids.hour_textinput.is_focusable = False if self.editing else True
        # self.ids.minute_textinput.is_focusable = False if self.editing else True
        # self.ids.second_textinput.is_focusable = False if self.editing else True
        # self.ids.hour_textinput.selection_color = (0, 0, 0, 0) if self.editing else (0.1843, 0.6549, 0.8313, .5)
        # self.ids.minute_textinput.selection_color = (0, 0, 0, 0) if self.editing else (0.1843, 0.6549, 0.8313, .5)
        # self.ids.second_textinput.selection_color = (0, 0, 0, 0) if self.editing else (0.1843, 0.6549, 0.8313, .5)
        # self.ids.body.background_color = (200/255, 200/255, 200/255, 1) if self.editing else (250/255, 250/255, 250/255, 1)
        # self.ids.timer_navigation.background_color = (200/255, 200/255, 200/255, 1) if self.editing else (250/255, 250/255, 250/255, 1)
        # for button in [self.ids.world_clock_button, self.ids.alarm_clock_button, self.ids.stopwatch_button]:
        #     button.hover = False if self.editing else True
        #     button.change_color = False if self.editing else True
        # self.ids.quick_timer_presets.clear_widgets()
        # self.ids.timer_button_container.clear_widgets()
        # self._private_create_timer_presets(self.editing)
        # [edit_button, delete_button] = self._private_create_buttons(edit_button_params if self.editing else start_button_params, delete_button_params if self.editing else None)
        # self.ids.timer_button_container.cols = 2 if self.editing else 1
        # self.ids.timer_button_container.add_widget(edit_button)
        # if delete_button: self.ids.timer_button_container.add_widget(delete_button)     

    # delete_presets
    def delete_presets(self):
        # Declare variables
        deleted_ids = []
        preset_container = None
        quick_timer_presets = self.ids.quick_timer_presets

        # Initialize "preset_container" variable
        while not preset_container:
            try: 
                if quick_timer_presets.children[0].id == "preset_container": preset_container = quick_timer_presets.children[0]
                else: quick_timer_presets = quick_timer_presets.children[0]
            except: quick_timer_presets = quick_timer_presets.children[0]

        # Find ids that are about to be deleted
        for preset in preset_container.children:
            if preset.selected:
                deleted_ids.append(preset.identifier)

        # Check statement
        if not deleted_ids: return

        # Load app_data.json file
        with open("app/app_data/app_data.json") as JsonFile:
            Json = json.load(JsonFile)
        JsonFile.close()

        # Remove all ids that match
        new_json = []
        for i in range(0, len(Json["timer_data"])):
            if Json["timer_data"][i]["id"] not in deleted_ids: new_json.append(Json["timer_data"][i])
        Json["timer_data"] = new_json

        # Change app_data.json file
        with open("app/app_data/app_data.json", "w") as JsonFile:
            json.dump(Json, JsonFile)
        JsonFile.close()

        # Redisplay preset times
        self._private_create_timer_presets(True)

    # pause_timer
    def pause_timer(self, *args):
        self.id_widgets[args[0]].text = "Play" if self.id_widgets[args[0]].text == "Pause" else "Pause"
        if self.timers[args[0][:args[0].find("_pause_button")]]["state"] == "pause":
            self.timers[args[0][:args[0].find("_pause_button")]]["state"] = "play"
            thread = threading.Thread(target = partial(self._private_play_timer, args[0][:args[0].find("_pause_button")]))
            thread.start()
            return
        self.timers[args[0][:args[0].find("_pause_button")]]["state"] = "pause"

    # reset_timer
    def reset_timer(self, timer_name):
        self.timers[timer_name]["time"] = self.timers[timer_name]["previous_time"]
        self.timers[timer_name]["state"] = "none"
        for i in range(0, 3):
            if i == 0: textinput_name = "hour"
            if i == 1: textinput_name = "minute"
            if i == 2: textinput_name = "second"
            self.id_widgets["{}_{}_textinput".format(timer_name, textinput_name)].text = "00"
        self.id_widgets.clear()
        self.ids.timers_container.clear_widgets()
        self._private_initialize_timer_page()

    # ----------------------- #
    # ---PRIVATE_FUNCTIONS--- #
    # ----------------------- #

    # _private_initialize_timer_page
    def _private_initialize_timer_page(self, *args):
        # Declare variables
        timer_buttons = []

        # Initialize variables
        for i in range(0, self.timer_amount):
            if i == 0: timer_button_id = "first_timer_start_button"
            if i == 1: timer_button_id = "second_timer_start_button"
            if i == 2: timer_button_id = "third_timer_start_button"
            timer_buttons.append(self._private_create_buttons([
            {"id": timer_button_id},
            {"radius": 10},
            {"text": "Start"},
            {"hover": True},
            {"width": 250},
            {"height": 100},
            {"static_font_size": 35},
            {"responsive_text": False},
            {"size_hint": (None, None)},
            {"minimum_text_size": False},
            {"on_press": partial(self.start_timer, timer_button_id)},
            {"hover_color_b": (75/255, 184/255, 81/255, 1)},
            {"normal_color_b": (148/255, 90/255, 230/255, 1)},
            {"normal_color_t": (1, 1, 1, 1)},
            {"hover_color_t": (1, 1, 1, 1)},
            {"pos_hint": {"center_x": .5, "center_y": .5}},
        ], None)[0])

        # Run python code below here...
        self.ids.timers_container.cols = self.timer_amount
        for i in range(0, self.timer_amount):
            if i == 0: self._private_create_timer_containers("Label1", (1, 1) if self.timer_amount == 3 else (None, 1), "first_timer")
            if i == 1: self._private_create_timer_containers("Label2", (1, 1) if self.timer_amount == 3 else (None, 1), "second_timer")
            if i == 2: self._private_create_timer_containers("Label3", (1, 1) if self.timer_amount == 3 else (None, 1), "third_timer")
        for i in range(0, self.timer_amount):
            self.id_widgets[timer_buttons[i].children[0].id] = timer_buttons[i].children[0]
        for i in range(0, self.timer_amount):
            if i == 0: self.id_widgets["first_timer_button_container"].add_widget(timer_buttons[i])
            if i == 1: self.id_widgets["second_timer_button_container"].add_widget(timer_buttons[i])
            if i == 2: self.id_widgets["third_timer_button_container"].add_widget(timer_buttons[i])
        self._private_create_timer_presets()

    # _private_create_timer_containers
    def _private_create_timer_containers(self, timer_name, content_width, prefix_timer):
        timer_hour_label = Label()
        timer_minute_label = Label()
        timer_second_label = Label()
        # Create Timer Container (eg. first_timer_container)
        timer_container = HB_GridLayout_M()
        timer_container.id = "{}_container".format(prefix_timer)
        timer_container.cols = 1
        timer_container.hover = False
        timer_container.outline_width = 2
        timer_container.change_color = False
        timer_container.display_outline = True
        timer_container.normal_color_b = (1, 1, 1, 1)
        timer_container.outline_color = (50/255, 50/255, 50/255, 1)
        self.id_widgets[timer_container.id] = timer_container

        # Create Timer Label (eg. first_timer_label)
        timer_label = HB_Label_M()
        timer_label.id = "{}_label".format(prefix_timer)
        timer_label.height = 80
        timer_label.hover = False
        timer_label.text = timer_name
        timer_label.change_color = False
        timer_label.size_hint = (1, None)
        timer_label.static_font_size = 40
        timer_label.responsive_text = False
        timer_label.color = (50/255, 50/255, 50/255, 1)
        timer_label.normal_color_b = (240/255, 240/255, 240/255, 1)
        self.id_widgets[timer_label.id] = timer_label

        # Create Timer Divider (eg. first_timer_divider)
        timer_divider = HB_GridLayout_M()
        timer_divider.id = "{}_divider".format(prefix_timer)
        timer_divider.height = 3
        timer_divider.hover = False
        timer_divider.change_color = False
        timer_divider.size_hint = (1, None)
        timer_divider.normal_color_b = (0, 0, 0, 1)
        timer_divider.bind(pos = self._private_update_widget, size = self._private_update_widget)
        self.id_widgets[timer_divider.id] = timer_divider

        # Create Timer Label Relative Layout (eg. first_timer_label_rel_layout)
        timer_label_rel_layout = RelativeLayout()
        timer_label_rel_layout.id  = "{}_label_rel_layout".format(prefix_timer)
        timer_label_rel_layout.height = 100
        timer_label_rel_layout.size_hint = (1, None)
        self.id_widgets[timer_label_rel_layout.id] = timer_label_rel_layout

        # Create Timer Label Container (eg. first_timer_label_container)
        timer_label_container = GridLayout()
        timer_label_container.id = "{}_label_container".format(prefix_timer)
        timer_label_container.cols = 3
        timer_label_container.width = 600
        timer_label_container.padding = (50, 0)
        timer_label_container.size_hint = content_width
        timer_label_container.pos_hint = {"center_x": .5, "center_y": .5}
        timer_label_container.bind(pos = self._private_update_timer_spacing, size = self._private_update_timer_spacing)
        self.id_widgets[timer_label_container.id] = timer_label_container

        # Create Timer Labels (eg. first_timer_hour_label)
        timer_label_array = [timer_hour_label, timer_minute_label, timer_second_label]     
        for i in range(0, 3):
            timer_time_label = timer_label_array[i]
            if i == 0: textinput_name = "Hour"
            if i == 1: textinput_name = "Minute"
            if i == 2: textinput_name = "Second"
            timer_time_label.id = "{}_{}{}_label".format(prefix_timer, textinput_name[0].lower(), textinput_name[1:])
            timer_time_label.text = textinput_name
            timer_time_label.font_size = 40
            timer_time_label.halign = "center"
            timer_time_label.size_hint = (None, 1)
            timer_time_label.color = (50/255, 50/255, 50/255, 1)
            timer_time_label.width = timer_time_label.texture_size[0] 
            timer_time_label.bind(pos = self._private_update_timer_label, size = self._private_update_timer_label)  
            self.id_widgets[timer_time_label.id] = timer_time_label

        # Create Timer TextInput Relative Layout (eg. first_timer_textinput_rel_layout)
        timer_textinput_rel_layout = RelativeLayout()
        timer_textinput_rel_layout.size_hint = (1, None)
        timer_textinput_rel_layout.height = 150

        # Create Timer TextInput Container (eg. first_timer_textinput_container)
        timer_textinput_container = GridLayout()
        timer_textinput_container.id = "{}_textinput_container".format(prefix_timer)
        timer_textinput_container.cols = 5
        timer_textinput_container.width = 600
        timer_textinput_container.padding = (50, 0)
        timer_textinput_container.size_hint = content_width
        timer_textinput_container.pos_hint = {"center_x": .5, "center_y": .5}
        self.id_widgets[timer_textinput_container.id] = timer_textinput_container

        # Create Timer TextInputs (eg. first_timer_hour_textinput)
        timer_textinput_array = []
        for i in range(0, 3):
            if i == 0: textinput_name = "hour"
            if i == 1: textinput_name = "minute"
            if i == 2: textinput_name = "second"
            timer_textinput = HB_TextInput_M()
            timer_textinput.id = "{}_{}_textinput".format(prefix_timer, textinput_name)
            timer_textinput.length = 2
            timer_textinput.alpha = False
            timer_textinput.numeric = True
            timer_textinput.special_characters = False
            timer_textinput.responsive_text = False
            timer_textinput.width = self.id_widgets["first_timer_minute_label"].width
            timer_textinput.text = "00"
            timer_textinput.font_size = 90
            timer_textinput.multiline = False
            timer_textinput.halign = "center"
            timer_textinput.size_hint = (None, 1)
            timer_textinput.background_color = (0, 0, 0, 0)
            timer_textinput.color = (50/255, 50/255, 50/255, 1)
            timer_textinput.bind(pos = self._private_update_textinput, size = self._private_update_textinput)
            timer_textinput_array.append(timer_textinput)
            self.id_widgets[timer_textinput.id] = timer_textinput
           
        # Create Timer First Colon Relative Layout (eg. first_timer_first_colon_rel_layout)
        timer_first_colon_rel_layout = RelativeLayout()

        # Create Timer Second Colon Relative Layout (eg. first_timer_second_colon_rel_layout)
        timer_second_colon_rel_layout = RelativeLayout()

        # Create Timer Colons (eg. first_timer_first_colon_label)
        timer_colon_array = []
        for i in range(0, 2):
            if i == 0: textinput_name = "first"
            if i == 1: textinput_name = "second"
            timer_colon_label = Label()
            timer_colon_label.id = "{}_{}_colon_label".format(prefix_timer, textinput_name)
            timer_colon_label.text = ":"
            timer_colon_label.font_size = 90
            timer_colon_label.size_hint = (None, None)
            timer_colon_label.size = timer_colon_label.texture_size
            timer_colon_label.color = (50/255, 50/255, 50/255, 1)
            timer_colon_label.pos_hint = {"center_x": .5, "center_y": .5}
            timer_colon_array.append(timer_colon_label)
            self.id_widgets[timer_colon_label.id] = timer_colon_label

        # Create Timer Button Container (eg. first_timer_button_container)
        timer_button_rel_layout = RelativeLayout()
        timer_button_container = GridLayout()
        timer_button_container.id = "{}_button_container".format(prefix_timer)
        timer_button_container.cols = 1
        timer_button_container.height = 200
        timer_button_container.size_hint = (1, None)
        timer_button_container.pos_hint = {"center_y": .5}
        self.id_widgets[timer_button_container.id] = timer_button_container

        # Add to screen
        timer_label_container.add_widget(timer_hour_label)
        timer_label_container.add_widget(timer_minute_label)
        timer_label_container.add_widget(timer_second_label)
        timer_label_rel_layout.add_widget(timer_label_container)

        timer_first_colon_rel_layout.add_widget(timer_colon_array[0])
        timer_second_colon_rel_layout.add_widget(timer_colon_array[1])
        timer_textinput_container.add_widget(timer_textinput_array[0])
        timer_textinput_container.add_widget(timer_first_colon_rel_layout)
        timer_textinput_container.add_widget(timer_textinput_array[1])
        timer_textinput_container.add_widget(timer_second_colon_rel_layout)
        timer_textinput_container.add_widget(timer_textinput_array[2])
        timer_textinput_rel_layout.add_widget(timer_textinput_container)

        timer_button_rel_layout.add_widget(timer_button_container)

        timer_container.add_widget(timer_label)
        timer_container.add_widget(timer_divider)
        timer_container.add_widget(timer_label_rel_layout)
        timer_container.add_widget(timer_textinput_rel_layout)
        timer_container.add_widget(timer_button_rel_layout)
        
        self.ids.timers_container.add_widget(timer_container)
        Clock.schedule_once(partial(self._private_update_timer_spacing, self.id_widgets["first_timer_label_container"]))

    # _private_create_buttons
    def _private_create_buttons(self, button1_param, button2_param = None):
        # Declare variables
        button1_rel_layout = RelativeLayout()
        button2_rel_layout = RelativeLayout()
        button1 = HB_Label_M()
        button2 = HB_Label_M()

        # Initialize button1
        for param in button1_param: self._private_set_button_param(button1, list(param.keys())[0], list(param.values())[0])
        button1_rel_layout.add_widget(button1)

        # Return if button2_param == None
        if not button2_param: return [button1_rel_layout, None]

        # Initialize button2
        for param in button2_param: self._private_set_button_param(button2, list(param.keys())[0], list(param.values())[0])
        button2_rel_layout.add_widget(button2)
            
        # Return both buttons
        return [button1_rel_layout, button2_rel_layout]    

    # _private_set_button_param
    def _private_set_button_param(self, button, param, value):
        if param == "id": button.id = value
        if param == "text": button.text = value
        if param == "hover": button.hover = value
        if param == "width": button.width = value
        if param == "radius": button.radius = value
        if param == "height": button.height = value
        if param == "on_press": button.on_press = value
        if param == "pos_hint": button.pos_hint = value
        if param == "size_hint": button.size_hint = value
        if param == "hover_color_t": button.hover_color_t = value
        if param == "hover_color_b": button.hover_color_b = value
        if param == "normal_color_t": button.normal_color_t = value
        if param == "normal_color_b": button.normal_color_b = value
        if param == "responsive_text": button.responsive_text = value
        if param == "static_font_size": button.static_font_size = value
        if param == "minimum_text_size": button.minimum_text_size = value

    # _private_create_timer_presets
    def _private_create_timer_presets(self, edit = False):
        # Load app_data.json file
        with open("app/app_data/app_data.json") as JsonFile:
            Json = json.load(JsonFile)
            Json = Json["timer_data"]
        JsonFile.close()

        # Check Statements
        if not Json: return

        # Declare variables
        JsonLength = len(Json)
        timer_presets_relative_layout = RelativeLayout()
        timer_presets_scrollview = ScrollView()
        timer_presets_container = GridLayout()

        # Run python code below here...
        timer_presets_relative_layout.add_widget(self._private_initialize_containers(JsonLength, timer_presets_scrollview, timer_presets_container))
        for i in range(0, JsonLength): 
            timer_presets_container.add_widget(self._private_create_preset(Json[i]["title"], Json[i]["time"], Json[i]["id"], True if edit else False))
        self.ids.quick_timer_presets.clear_widgets()
        self.ids.quick_timer_presets.add_widget(timer_presets_relative_layout)
 
    # _private_initialize_containers
    def _private_initialize_containers(self, preset_amount, scrollview, gridlayout):
        # Run python code below here...
        gridlayout.id = "preset_container"
        gridlayout.rows = 1
        gridlayout.padding = (50, 0)
        gridlayout.spacing = (50, 0)
        gridlayout.size_hint = (None, 1)
        gridlayout.pos_hint = {"center_x": .5}
        gridlayout.width =  gridlayout.minimum_width
        gridlayout.bind(pos = self._private_update_preset_container, size = self._private_update_preset_container)

        if preset_amount <= 4: return gridlayout

        scrollview.effect_cls = ScrollEffect
        scrollview.do_scroll_x = True
        scrollview.do_scroll_y = False
        scrollview.width = 950
        scrollview.size_hint = (None, 1)
        scrollview.pos_hint = {"center_x": .5}  

        scrollview.add_widget(gridlayout) 

        return scrollview

    # _private_create_preset
    def _private_create_preset(self, title, time, id, edit = False):
        # Declare variables
        letter_in_title = 0
        timer_preset_container = HB_GridLayout_M()
        timer_preset_title_containter = RelativeLayout()
        timer_preset_title = Label()
        timer_preset_time_containter = RelativeLayout()
        timer_preset_time = Label()

        # Run python code below here...
        timer_preset_container.identifier = id
        timer_preset_container.selected = False
        timer_preset_container.rows = 2
        timer_preset_container.radius = 2
        timer_preset_container.width = 200
        timer_preset_container.padding = 5
        timer_preset_container.height = 200
        timer_preset_container.size_hint = (None, None)
        timer_preset_container.bind(on_press = self.set_timer if not edit else self.toggle_selected)
        timer_preset_container.normal_color_b = (200/255, 200/255, 200/255, 1) if not edit else (160/255, 160/255, 160/255, 1)
        timer_preset_container.hover_color_b = (216/255, 181/255, 255/255, 1) if not edit else (180/255, 180/255, 180/255, 1)

        for i in range(0, len(title)):
            if title[i] in "WMQOwm":
                letter_in_title += 1

        if letter_in_title <= 3: timer_preset_title.text = title if len(title) < 9 else "{}...".format(title[:6])
        if letter_in_title > 3: timer_preset_title.text = title if len(title) < 7 else "{}...".format(title[:6])
        timer_preset_title.bold = True
        timer_preset_title.font_size = 27
        timer_preset_title.color = (20/255, 20/255, 20/255, 1)
        timer_preset_title.pos_hint = {"center_x": .5, "center_y": .30}            

        timer_preset_time.text = time
        timer_preset_time.font_size = 28
        timer_preset_time.color = (50/255, 50/255, 50/255, 1)
        timer_preset_time.pos_hint = {"center_x": .5, "center_y": .65}

        timer_preset_time_containter.add_widget(timer_preset_time)
        timer_preset_title_containter.add_widget(timer_preset_title)
        timer_preset_container.add_widget(timer_preset_title_containter)
        timer_preset_container.add_widget(timer_preset_time_containter)

        return timer_preset_container    

    # _private_play_timer
    @mainthread
    def _private_play_timer(self, timer_prefix):
        # Declare variables
        timer_data = self.timers[timer_prefix]
        timer_data = self.timers[timer_prefix]
        timer_data = self.timers[timer_prefix]

        # Check statements
        if self.quit_all_threads: return

        # Check it timer is inactive
        if timer_data["state"] == "none": return

        # Check it timer is paused
        if timer_data["state"] == "pause":
            self.id_widgets["{}_pause_button".format(timer_prefix)].text = "Play"
            print("Paused!")
            return

        # Check if the timer is at zero
        if timer_data["time"] == [0, 0, 0] and timer_data["state"] == "play":
            self.timers[timer_prefix]["state"] = "finished"
            print("{}: Timer finished!".format(timer_prefix))
            return

        # Run python code below here...
        if timer_data["time"][0] == 0 and timer_data["time"][1] == 0 and timer_data["time"][2] <= 5:
            self.id_widgets["{}_hour_textinput".format(timer_prefix)].foreground_color = (1, 0, 0, 1)
            self.id_widgets["{}_minute_textinput".format(timer_prefix)].foreground_color = (1, 0, 0, 1)
            self.id_widgets["{}_second_textinput".format(timer_prefix)].foreground_color = (1, 0, 0, 1)
            self.id_widgets["{}_first_colon_label".format(timer_prefix)].color = (1, 0, 0, 1)
            self.id_widgets["{}_second_colon_label".format(timer_prefix)].color = (1, 0, 0, 1)


        if timer_data["time"][2] == 0:
            if timer_data["time"][1] == 0:
                timer_data["time"][0] -= 1
                timer_data["time"][1] = 59
                timer_data["time"][2] = 59
            else:
                timer_data["time"][2] = 59
                timer_data["time"][1] -= 1
        else:
            timer_data["time"][2] -= 1

        self.id_widgets["{}_hour_textinput".format(timer_prefix)].text = "0{}".format(timer_data["time"][0]) if timer_data["time"][0] < 10 else str(timer_data["time"][0])
        self.id_widgets["{}_minute_textinput".format(timer_prefix)].text = "0{}".format(timer_data["time"][1]) if timer_data["time"][1] < 10 else str(timer_data["time"][1])
        self.id_widgets["{}_second_textinput".format(timer_prefix)].text = "0{}".format(timer_data["time"][2]) if timer_data["time"][2] < 10 else str(timer_data["time"][2])

        threading.Timer(.1, self._private_play_timer, [timer_prefix]).start()

    # _private_update_widget
    def _private_update_widget(self, *args):
        args[0].rect.pos = args[0].pos
        args[0].rect.size = args[0].size

    # _private_update_preset_container
    def _private_update_preset_container(self, *args):
        args[0].pos = args[0].pos
        args[0].width = args[0].minimum_width  

    # _private_update_timer_label
    def _private_update_timer_label(self, *args):
        args[0].font_size = 40
        args[0].width = self.id_widgets["first_timer_minute_label"].texture_size[0]

    # _private_update_textinput
    def _private_update_textinput(self, *args):
        args[0].width = self.id_widgets["first_timer_minute_label"].width
        args[0].padding_y = [(args[0].height - args[0].font_size) / 2, 0]

    # _private_update_timer_spacing
    def _private_update_timer_spacing(self, *args):
        args[0].spacing = ((int(args[0].width) - 100) - (int(self.id_widgets["first_timer_minute_label"].width) * 3)) / 2


    def _private_useless_function(self, *args):
        pass