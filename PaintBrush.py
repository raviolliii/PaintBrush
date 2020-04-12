from PIL import Image
import numpy as np

from Brush import clump as c_clump, smooth as c_smooth


def paint(file_path: str = None,
          pixels: list = None,
          output_path: str = None,
          alpha: float = 3,
          radius: int = 2) -> list:
    """
    Applies both the clumping and smoothing effects on the
    given pixels. If the file_path is given, the pixels of
    the file are used. Specifying the output_path saves the 
    resulting pixel data to the path.
    
    Args:
        file_path: the path of the input image
        pixels: 2d list of pixel values
        output_path: path to save the resulting image to
        alpha: color variation threshold
        radius: the blur radius

    Returns:
        list: the new, resulting pixels
    """

    # load in pixels from file
    if file_path is not None:
        pixels = _load_img_data(file_path)

    # apply both effects
    pixels = _paint(pixels, alpha, radius)

    # save to file if path is specified
    if output_path:
        _save_img_data(pixels, output_path)
    return pixels


def _load_img_data(file_path: str) -> list:
    """
    Opens the image at the file path and returns an
    array of the pixel values by width/height.

    Args:
        file_path: the path of the input image

    Returns:
        A 2d list of the pixel values
    """
    img = Image.open(file_path)
    _, height = img.size
    pixels = img.getdata()
    # split flat list into chunks respecting img dimensions
    chunk = np.array_split
    return [c.tolist() for c in chunk(pixels, height)]


def _save_img_data(pixels: list, output_path: str) -> None:
    """
    Saves pixel data as a PNG image.
    Note: only supports .png format for now.

    Args:
        pixels: list of pixel values to save
        output_path: path of saved file
    """
    data = np.array(pixels, dtype=np.uint8)
    output = Image.fromarray(data, 'RGB')
    output.save(output_path, 'PNG')
    return


def _paint(pixels: list, alpha: float, radius: int) -> list:
    """
    Applies both the clumping and smoothing effects
    on the given pixel set

    Args:
        pixels: list of image pixel values
        alpha: threshold of color variation allowed
        radius: blur radius of Median Filter
    
    Returns:
        The resulting pixel values
    """
    dim = (len(pixels[0]), len(pixels))

    # apply both effects in succession
    pixels = clump(pixels, dim, alpha)
    return smooth(pixels, dim, radius)


def clump(pixels: list, dim: tuple, alpha: float) -> list:
    """
    Sets adjacent, similar colored pixels to the same color.
    Creates a clumped, flattened out effect on the image. 
    Implemented in cython for performance (see Brush.pyx)

    Args:
        pixels: list of image pixel values
        dim: width/height pair of pixels
        alpha: threshold of color variation
    
    Returns:
        The resulting pixel values
    """
    return c_clump(pixels, dim, alpha)


def smooth(pixels: list, dim: tuple, radius: int) -> list:
    """
    Smooths out jagged, pixelated edges in the pixels
    by applying a Median Filter. Implemented in
    cython for performance (see Brush.pyx)

    Args:
        pixels: list of image pixel values
        dim: width/height pair of pixels
        radius: blur radius of Median Filter
    
    Returns:
        The resulting pixel values
    """
    return c_smooth(pixels, dim, radius)
   

