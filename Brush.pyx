from math import sqrt


# Brush Functions
# ---------------
# Clumping, Median Filter, etc.


cpdef list clump(list pixels, tuple dim, float alpha):
    """
    Groups pixels similar in color, and sets them all 
    to the same color. Uses a BFS approach to find groups.
    """
    cdef int width, height
    cdef int x, y
    cdef list clumped, visited
    cdef list points, pixel_rgbs, new_pixel

    width, height = dim
    clumped = [[False] * width for _ in range(height)]
    visited = [[False] * width for _ in range(height)]

    for x in range(width):
        for y in range(height):
            # ignore already visited pixels, mark new ones as visited
            if visited[y][x]:
                continue
            visited[y][x] = True

            # get current rgb values of pixels in this group
            points = explore(pixels, dim, (x, y), visited, alpha)
            pixel_rgbs = [pixels[py][px] for px, py in points]

            # set group's pixels to average rgb value
            new_pixel = avg(pixel_rgbs)
            for px, py in points:
                clumped[py][px] = new_pixel
    return clumped


cpdef list explore(list pixels, tuple dim, tuple origin, list visited, float alpha):
    """
    Finds and returns the positions of pixels in a group. 
    Neighbors are explored in a BFS approach, and are added
    to the group if they differ from the origin color less
    than the alpha value.
    """
    cdef list queue = [origin]
    cdef list o_color, n_color
    cdef tuple point, neighbor
    cdef int x, y
    # list of positions of pixels in group
    cdef list points = []

    # color of the origin pixel
    o_color = pixels[origin[1]][origin[0]]

    while queue:
        point = queue.pop(0)
        # check neighborhood for pixels to add
        for neighbor in get_neighbors(point, dim):
            x, y = neighbor
            # ignore visited pixels
            if visited[y][x]:
                continue

            # find difference in this color vs origin
            # ignore pixel if difference is more than given
            # alpha value 
            n_color = pixels[y][x]
            if diff(o_color, n_color) > alpha:
                continue

            # mark this pixel as visited and add to queue
            visited[y][x] = True
            queue.append(neighbor)
        points.append(point)
    return points


cpdef list get_neighbors(tuple pos, tuple dim):
    """
    Finds and returns the points surrounding the given
    position. Points are directly up/down/left/right to 
    the given position, and are filtered out if they
    are invalid by the dimensions.
    """
    cdef int width, height
    cdef int x, y
    cdef list surr = []

    width, height = dim
    x, y = pos

    # didn't use a simple loop here to minimize number of 
    # operations done while running explore
    # TODO: check if runtime is affected using a loop
    if y - 1 >= 0:
        surr.append((x, y - 1))
    if y + 1 < height:
        surr.append((x, y + 1))
    if x - 1 >= 0:
        surr.append((x - 1, y))
    if x + 1 < width:
        surr.append((x + 1, y))
    return surr


cpdef list smooth(list pixels, tuple dim, int radius):
    """
    Applies a Median Filter to the pixels with the given 
    radius. The process is very similar to that written in 
    a paper (see reference) with minor adjustments for 
    implementation. Pixel values (for each RGB channel) are 
    determined by the median value of the neighboring pixels.

    Reference: https://nomis80.org/ctmf.pdf
    """
    cdef int width, height
    width, height = dim

    # resulting smoothed out image
    cdef list smoothed = [[False] * width for _ in range(height)]
    cdef int x, y
    cdef int xs, xe, ys, ye
    cdef list r_hist, g_hist, b_hist
    cdef int r, g, b
    cdef int count, rank
    cdef list colors, row, col

    for y in range(height):
        # reset RGB frequencies
        r_hist = [0] * 256
        g_hist = [0] * 256
        b_hist = [0] * 256
        # keep track of the number of values
        count = 0

        # calculate the valid start and end positions 
        # in the y direction
        ys = y - radius
        ys = 0 if ys < 0 else ys
        ye = y + radius + 1
        ye = height if ye > height else ye

        # get pixels in radius at the beginning of this row
        colors = []
        for row in pixels[ys:ye]:
            colors += row[:radius + 1]
        # update RGB freqencies with values
        for r, g, b in colors:
            r_hist[r] += 1
            g_hist[g] += 1
            b_hist[b] += 1
            count += 1

        for x in range(width):
            # find median of each channel using frequencies
            rank = count // 2
            r = median(r_hist, rank)
            g = median(g_hist, rank)
            b = median(b_hist, rank)

            # set this pixel's RGB value
            smoothed[y][x] = [r, g, b]

            xs = x - radius
            xe = x + radius + 1
            # remove previous column from frequencies
            if xs >= 0:
                col = [row[xs] for row in pixels[ys:ye]]
                for r, g, b in col:
                    r_hist[r] -= 1
                    g_hist[g] -= 1
                    b_hist[b] -= 1
                    count -= 1
            # add next column to frequencies
            if xe < width:
                col = [row[xe] for row in pixels[ys:ye]]
                for r, g, b in col:
                    r_hist[r] += 1
                    g_hist[g] += 1
                    b_hist[b] += 1
                    count += 1

    return smoothed


cpdef int median(list buckets, int rank):
    """
    Finds the median value in the buckets. Buckets 
    represents freqency of values, with the index being 
    the value and the element being the frequency. The 
    median can then be found by accumulating a sum, and 
    returning its index when it exceeds the rank.
    """
    cdef int total = 0
    cdef int val = 0

    cdef int count
    for count in buckets:
        total += count
        # return the index (value of median) when rank 
        # is exceeded
        if total > rank:
            return val
        val += 1
    return 0


# Color Functions
# ---------------
# Operations on RGB values, etc.


cpdef list avg(list colors):
    """
    Finds the average RGB values of the given colors.
    Average is calculated individually for each channel.
    """
    cdef int R, G, B
    cdef int total

    R, G, B = 0, 0, 0
    for r, g, b in colors:
        R += r
        G += g
        B += b
        total += 1
    return [x // total for x in [R, G, B]]


cpdef list to_yuv(list rgb):
    """
    Converts RGB values to its YUV equivalent
    """
    cdef int r, g, b
    cdef float u, v

    r, g, b = rgb
    # NOTE: for this purpose, the Y value is not
    # needed, and so is not calculated or returned
    u = (-0.14713 * r) + (-0.28886 * g) + (0.436 * b)
    v = (0.615 * r) + (-0.51499 * g) + (-0.10001 * b)
    return [u, v]


cpdef float diff(list c1, list c2):
    """
    Finds the difference between two RGB values.
    Value is the Euclidean Distance between the 
    colors' YUV equivalents (YUV seems to be a 
    better scale to quantify the difference between
    two colors than RGB)
    """
    cdef list y1, y2
    cdef int d1, d2

    y1 = to_yuv(c1)
    y2 = to_yuv(c2)
    d1 = (y1[0] - y2[0]) ** 2
    d2 = (y1[1] - y2[1]) ** 2
    return sqrt(d1 + d2)
