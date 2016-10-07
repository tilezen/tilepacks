from tilepack.util import point_to_tile

def cover_bbox(min_lon, min_lat, max_lon, max_lat, zoom):
    min_x, max_y, _ = point_to_tile(min_lon, min_lat, zoom)
    max_x, min_y, _ = point_to_tile(max_lon, max_lat, zoom)

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            yield (x, y, zoom)
