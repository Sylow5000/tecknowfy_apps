from kivy.uix.image import AsyncImage
from kivy.uix.behaviors import CoverBehavior

# ------------------------------------------------------------------------------- #
#                                                                                 #
#                              HB_CoverImage_M Class                              #
#                                                                                 #
# ------------------------------------------------------------------------------- #
class HB_CoverImage_M(CoverBehavior, AsyncImage):
    # HB_CoverImage_M is an image that can cover the entire image
    # HB_CoverImage_M doesn't have any custom parameters
    #
    # +--------------------------------------------------------------------------------+
    # |                                                                                |
    # +--------------------------------------------------------------------------------+
    def __init__(self, **kwargs):
        super(HB_CoverImage_M, self).__init__(**kwargs)
        try:
            texture = self._coreimage.texture
            self.reference_size = texture.size
            self.texture = texture
        except:
            print("Img could not be loaded!")