import subprocess
from sys import argv
from time import time

from PaintBrush import paint


def print_time(t):
    """
    Just prints elapsed time in a minutes and
    seconds format
    """
    t = int(t)
    time_str = f'{t // 60}m ' if t // 60 else ''
    time_str += f'{t % 60}s'
    print('[Time]: ' + time_str)


# parse arguments
img_path, out_path, alpha, radius = argv[1:]
alpha = float(alpha)
radius = int(radius)

# apply both effects + measure time taken
# FIX: this is a bad way to measure elapsed time
print('Processing Image ... ')
s = time()

# paint image
pixels = paint(file_path=img_path,
              output_path=out_path,
              alpha=alpha,
              radius=radius)

t = time() - s
print_time(t)

# auto open input and output images for comparison
# FIX: remove this or add support for other OS
subprocess.run(['open', img_path, out_path])

