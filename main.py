import subprocess
from sys import argv
from time import time

from PaintBrush import PaintBrush
from Canvas import Canvas


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

# create brush and canvas
canvas = Canvas(img_path=img_path)
brush = PaintBrush()
brush.canvas = canvas

# print out image meta
print('\n' + ('-' * 12) + ' Image Meta ' + ('-' * 12))
for key, value in canvas.meta.items():
    tag = f'{key}: '.ljust(12)
    data = value.rjust(24)
    print(tag + data)
print(('-' * 36) + '\n')

# apply both effects + measure time taken
# FIX: this is a bad way to measure elapsed time
s = time()
brush.paint(out_path, alpha, radius)
t = time() - s
print_time(t)

# auto open input and output images for comparison
subprocess.run(['open', img_path, out_path])

