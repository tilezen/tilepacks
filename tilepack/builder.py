from tilepack.util import point_to_tile
import tilepack.outputter
import requests
import zipfile
import argparse
import os
import multiprocessing

def cover_bbox(min_lon, min_lat, max_lon, max_lat, zoom):
    min_x, max_y, _ = point_to_tile(min_lon, min_lat, zoom)
    max_x, min_y, _ = point_to_tile(max_lon, max_lat, zoom)

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            yield (x, y, zoom)

# def fetch_tile(x, y, z, layer, format, api_key):
def fetch_tile(format_args):
    while True:
        try:
            url = 'https://vector.mapzen.com/osm/{layer}/{zoom}/{x}/{y}.{fmt}?api_key={api_key}'.format(**format_args)
            resp = requests.get(url)
            return (format_args, resp.content)
        except requests.exceptions.ConnectionError:
            print("Connection error, retrying")

output_type_mapping = {
    'mbtiles': tilepack.outputter.MbtilesOutput,
    'zipfile': tilepack.outputter.ZipfileOutput,
}

def build_tile_packages(min_lon, min_lat, max_lon, max_lat, min_zoom, max_zoom,
        layer, tile_format, output, output_formats, api_key):

    fetches = []
    for zoom in range(min_zoom, max_zoom + 1):
        for x, y, z in cover_bbox(min_lon, min_lat, max_lon, max_lat, zoom=zoom):
            fetches.append(dict(x=x, y=y, zoom=z, layer=layer, fmt=tile_format, api_key=api_key))

    tiles_to_get = len(fetches)

    tile_ouputters = [output_type_mapping.get(t).build_from_basename(output) for t in set(output_formats)]

    try:
        p = multiprocessing.Pool(multiprocessing.cpu_count() * 10)

        for t in tile_ouputters:
            t.open()
            t.add_metadata('name', output)
            # FIXME: Need to include the `json` key
            t.add_metadata('format', 'application/vnd.mapbox-vector-tile')
            t.add_metadata('bounds', ','.join(map(str, [min_lon, min_lat, max_lon, max_lat])))
            t.add_metadata('minzoom', min_zoom)
            t.add_metadata('maxzoom', max_zoom)

        for i, (format_args, data) in enumerate(p.imap_unordered(fetch_tile, fetches)):
            for t in tile_ouputters:
                t.add_tile(format_args, data)
    finally:
        p.close()
        p.join()
        for t in tile_ouputters:
            t.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('min_lon',
        type=float,
        help='Bounding box minimum longitude/left')
    parser.add_argument('min_lat',
        type=float,
        help='Bounding box minimum latitude/bottom')
    parser.add_argument('max_lon',
        type=float,
        help='Bounding box maximum longitude/right')
    parser.add_argument('max_lat',
        type=float,
        help='Bounding box maximum latitude/top')
    parser.add_argument('min_zoom',
        type=int,
        help='The minimum zoom level to include')
    parser.add_argument('max_zoom',
        type=int,
        help='The maximum zoom level to include')
    parser.add_argument('output',
        help='The filename for the output tile package')
    parser.add_argument('--layer',
        default='all',
        help='The Mapzen Vector Tile layer to request')
    parser.add_argument('--tile-format',
        default='mvt',
        help='The Mapzen Vector Tile format to request')
    parser.add_argument('--output-formats',
        default='mbtiles,zipfile',
        type=lambda x: x.split(','),
        help='A comma-separated list of output formats to write to')
    args = parser.parse_args()

    api_key = os.environ.get('MAPZEN_API_KEY')

    build_tile_packages(
        args.min_lon,
        args.min_lat,
        args.max_lon,
        args.max_lat,
        args.min_zoom,
        args.max_zoom,
        args.layer,
        args.tile_formats,
        api_key
    )

if __name__ == '__main__':
    main()
