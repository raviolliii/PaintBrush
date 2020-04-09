from PIL import Image
import numpy as np

from Brush import clump as c_clump, smooth as c_smooth
from Canvas import Canvas


class PaintBrush:
    """
    Applies effects to a Canvas. Currently supported 
    effects include clumping and smoothing, to create 
    some kind of effect I'm not quite sure how to 
    describe just yet (depends on the image really).
    """

    def __init__(self, canvas=None):
        """
        Creates a PaintBrush for the given Canvas
        """
        if not isinstance(canvas, Canvas):
            canvas = None
        self.canvas = canvas
    
    @property
    def canvas(self):
        """
        This PaintBrush's canvas to operate on
        """
        return self._canvas
    
    @canvas.setter
    def canvas(self, new_canvas):
        """
        Updates this canvas
        """
        self._canvas = new_canvas
    
    def paint(self, output_path, alpha, radius):
        """
        Applies both the clumping and smoothing effects
        on the current canvas. Uses the given alpha and 
        radius values for the effects. Saves the resulting 
        image to the output path
        """
        if not self.canvas:
            raise AttributeError('no Canvas exists for this paint brush')

        # use img properties of canvas
        img_pixels = self.canvas.pixels
        img_dim = self.canvas.dim

        # apply both effects in succession
        pixels = self.clump(img_pixels, img_dim, alpha)
        pixels = self.smooth(pixels, img_dim, radius)

        # save the resulting pixel data as a .png image
        # TODO: move saving functionality to Canvas
        data = np.array(pixels, dtype=np.uint8)
        output = Image.fromarray(data, 'RGB')

        output.save(output_path, 'PNG')
        return
    
    def clump(self, pixels, dim, alpha):
        """
        Groups pixels close together and similar in color, 
        setting them all to the same color. Creates a 
        clumped, flattened out effect on the image. 
        Implemented in cython for performance (see Brush.pyx)
        """
        return c_clump(pixels, dim, alpha)

    def smooth(self, pixels, dim, radius):
        """
        Smooths out jagged, pixelated edges in the pixels
        by applying a Median Filter. Implemented in
        cython for performance (see Brush.pyx)
        """
        return c_smooth(pixels, dim, radius)
   

