from PIL import Image
import numpy as np


class Canvas:
    """
    Contains Image data for for applying effects to.
    """
    
    def __init__(self, img_path=None):
        """
        Creates a Canvas using the given image path
        """
        if isinstance(img_path, str):
            # FIX: this is a bad way to check for jpg images only
            valid_exts = ['.jpg', '.jpeg']
            _img_path = img_path.lower()
            valid = [_img_path.endswith(e) for e in valid_exts]
            if not any(valid):
                raise ValueError('image must be a jpg (or jpeg)')
        self.img_path = img_path
    
    @property
    def img_path(self):
        """
        The image path for this Canvas
        """
        return self._img_path
    
    @img_path.setter
    def img_path(self, new_path):
        """
        Updates the image path and relative data using
        the new image path
        """
        self._img_path = new_path
        img = Image.open(new_path)
        # update image data
        self.dim = img.size
        self.pixels = self.parse_img_data(img.getdata())
    
    def parse_img_data(self, data):
        """
        Splits the 1D image pixel data into a 2D list, 
        respecting the width/height of the image. Uses
        numpy for performance, but returns the 2D result
        as a pure list.
        """
        chunkify = np.array_split
        _, height = self.dim
        return [c.tolist() for c in chunkify(data, height)]
    
    @property
    def meta(self):
        """
        Returns a dictionary with this Canvas' image data
        """
        size = self.dim
        meta = {
            'File': self.img_path,
            'Size': 'x'.join(map(str, size)),
            'Pixels': f'{size[0] * size[1]:,}',
        }
        return meta
    

