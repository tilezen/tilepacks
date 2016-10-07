import math

def point_to_tile_fraction(lon, lat, zoom):
    sin = math.sin(math.radians(lat))
    z2 = math.pow(2, zoom)
    x = z2 * (lon / 360 + 0.5)
    y = z2 * (0.5 - 0.25 * math.log((1 + sin) / (1 - sin)) / math.pi)
    return [x, y, zoom]

def point_to_tile(lon, lat, zoom):
    (x, y, z) = point_to_tile_fraction(lon, lat, zoom)
    return [int(x), int(y), zoom]
