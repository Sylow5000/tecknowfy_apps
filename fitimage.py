from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import RoundedRectangle
from kivy.properties import StringProperty, Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget

"""
By Benedikt Zwölfer
Example usage:
    BoxLayout:
        size_hint_y: None
        height: dp(200)
        orientation: 'vertical'
        
        FitImage:
            size_hint_y: 3
            source: 'images/img1.jpg'
            
        FitImage:
            size_hint_y: 1
            source: 'images/img2.jpg'
Works with KivyMD
"""


class FitImage(BoxLayout):
    source = StringProperty()

    def __init__(self, **kwargs):
        if "radius" in kwargs:
            self.radius = kwargs["radius"]
            kwargs.pop("radius")
        else:
            self.radius = [0, 0, 0, 0]
        super().__init__(**kwargs)
        Clock.schedule_once(self._late_init)

    def _late_init(self, *args):
        self.container = Container(self.source, self.radius)
        self.add_widget(self.container)

    def _update_radius(self):
        try: 
            self.container.radius = self.radius
            self.container.adjust_size()
        except: pass


class Container(Widget):
    def __init__(self, source, radius, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.adjust_size)
        self.radius = radius
        self.image = Image(source = source)

    def adjust_size(self, *args):
        (par_x, par_y) = self.parent.size

        if par_x == 0 or par_y == 0:
            with self.canvas:
                self.canvas.clear()
            return

        par_scale = par_x / par_y

        (img_x, img_y) = self.image.texture.size
        img_scale = img_x / img_y

        if par_scale > img_scale:
            (img_x_new, img_y_new) = (img_x, img_x / par_scale)
        else:
            (img_x_new, img_y_new) = (img_y * par_scale, img_y)

        crop_pos_x = (img_x - img_x_new) / 2
        crop_pos_y = (img_y - img_y_new) / 2

        subtexture = self.image.texture.get_region(crop_pos_x, crop_pos_y, img_x_new, img_y_new)

        with self.canvas:
            self.canvas.clear()
            Color(1, 1, 1)
            RoundedRectangle(texture=subtexture, pos=self.pos, size=(par_x, par_y), radius = self.radius)