from PIL import Image
import math

from . import constants, generated_set


class Thumbnails(generated_set.GeneratedSet):
    """
    Handles generation of thumbnails. All paths in this class, in the API and
    internally, are expected to be hashlib.Path instances
    """

    def __init__(self, generated_dir):
        super().__init__(generated_dir)

    def generated_file_prefix(self):
        return 'thumb'

    def create_file(self, source, destination):
        im = Image.open(source)
        x, y = im.size
        pixels = x * y
        scale = math.sqrt(pixels / constants.thumbnail_target_pixels)
        im.thumbnail((x / scale, y / scale))
        im.save(destination)
