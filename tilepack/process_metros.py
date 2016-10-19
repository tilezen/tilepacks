from tilepack.builder import cover_bbox, build_tile_packages

import argparse
import os
import requests
import time

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('min_zoom',
        type=int,
        help='The minimum zoom level to include')
    parser.add_argument('max_zoom',
        type=int,
        help='The maximum zoom level to include')
    parser.add_argument('--cities-url',
        default="https://raw.githubusercontent.com/mapzen/metro-extracts/master/cities.json",
        help='A GeoJSON URL with features to cover with tiles')
    parser.add_argument('--output-prefix',
        default="output",
        help='The path prefix to output coverage data to')
    args = parser.parse_args()

    cities_resp = requests.get(args.cities_url)
    cities_resp.raise_for_status()
    cities_data = cities_resp.json()

    api_key = os.environ.get('MAPZEN_API_KEY')

    for feature in cities_data:
        name = feature['id']
        bbox = feature['bbox']
        min_lon, min_lat, max_lon, max_lat = float(bbox['left']), float(bbox['bottom']), float(bbox['right']), float(bbox['top'])

        start = time.time()

        build_tile_packages(
            min_lon,
            min_lat,
            max_lon,
            max_lat,
            args.min_zoom,
            args.max_zoom,
            'all',
            'mvt',
            os.path.join(args.output_prefix, name),
            ['mbtiles', 'zipfile'],
            api_key)

        elapsed = time.time() - start

        print("Wrote packages for {} in {:0.2f} sec".format(name, elapsed))

if __name__ == '__main__':
    main()
