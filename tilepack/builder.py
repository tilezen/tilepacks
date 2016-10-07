from tilepack.util import point_to_tile
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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('min_lon', type=float, help='Bounding box minimum longitude/left')
    parser.add_argument('min_lat', type=float, help='Bounding box minimum latitude/bottom')
    parser.add_argument('max_lon', type=float, help='Bounding box maximum longitude/right')
    parser.add_argument('max_lat', type=float, help='Bounding box maximum latitude/top')
    parser.add_argument('min_zoom', type=int, help='The minimum zoom level to include')
    parser.add_argument('max_zoom', type=int, help='The maximum zoom level to include')
    parser.add_argument('output', help='The filename for the output tile package')
    parser.add_argument('--layer', default='all')
    parser.add_argument('--format', default='mvt')
    args = parser.parse_args()

    api_key = os.environ.get('MAPZEN_API_KEY')

    p = multiprocessing.Pool(25)

    fetches = []
    for zoom in range(args.min_zoom, args.max_zoom + 1):
        for x, y, z in cover_bbox(args.min_lon, args.min_lat, args.max_lon, args.max_lat, zoom=zoom):
            fetches.append(dict(x=x, y=y, zoom=z, layer=args.layer, fmt=args.format, api_key=api_key))

    tiles_to_get = len(fetches)

    with zipfile.ZipFile(args.output, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
        for i, (format_args, data) in enumerate(p.imap_unordered(fetch_tile, fetches)):
            key = '{layer}/{zoom}/{x}/{y}.{fmt}'.format(**format_args)
            zipf.writestr(key, data)

    p.close()

if __name__ == '__main__':
    main()
