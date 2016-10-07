from tilepack.util import point_to_tile
import requests
import zipfile
import argparse
import os

def cover_bbox(min_lon, min_lat, max_lon, max_lat, zoom):
    min_x, max_y, _ = point_to_tile(min_lon, min_lat, zoom)
    max_x, min_y, _ = point_to_tile(max_lon, max_lat, zoom)

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            yield (x, y, zoom)

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

    apikey = os.environ.get('MAPZEN_API_KEY')

    with zipfile.ZipFile(args.output, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
        for zoom in range(args.min_zoom, args.max_zoom + 1):
            for x, y, z in cover_bbox(args.min_lon, args.min_lat, args.max_lon, args.max_lat, zoom=zoom):
                format_args = dict(
                    layer=args.layer,
                    zoom=z,
                    x=x,
                    y=y,
                    fmt=args.format,
                    apikey=apikey,
                )

                resp = requests.get('https://vector.mapzen.com/osm/{layer}/{zoom}/{x}/{y}.{fmt}?api_key={apikey}'.format(**format_args))
                key = '{layer}/{zoom}/{x}/{y}.{fmt}'.format(**format_args)
                zipf.writestr(key, resp.content)

if __name__ == '__main__':
    main()
