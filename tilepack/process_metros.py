from tilepack.builder import build_tile_packages

import argparse
import os
import requests
import datetime
import json
import multiprocessing

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('min_zoom',
        type=int,
        help='The minimum zoom level to include')
    parser.add_argument('max_zoom',
        type=int,
        help='The maximum zoom level to include')
    parser.add_argument('--cities-url',
        default="https://mapzen.com/data/metro-extracts/cities-extractor.json",
        help='A GeoJSON URL with features to cover with tiles')
    parser.add_argument('--output-prefix',
        default="output",
        help='The path prefix to output coverage data to')
    parser.add_argument('-j', '--concurrency',
        type=int,
        default=multiprocessing.cpu_count() * 8,
        help='The size of the process pool to use when downloading tiles')
    args = parser.parse_args()

    cities_resp = requests.get(args.cities_url)
    cities_resp.raise_for_status()
    cities_data = cities_resp.json()

    api_key = os.environ.get('MAPZEN_API_KEY')

    for feature in cities_data:
        name = feature['id']
        metadata_filename = os.path.join(args.output_prefix, '{}_metadata.json'.format(name))
        if os.path.exists(metadata_filename):
            print("Skipping {} because the metadata file already exists".format(name))
            continue

        bbox = feature['bbox']
        min_lon, min_lat, max_lon, max_lat = float(bbox['left']), float(bbox['bottom']), float(bbox['right']), float(bbox['top'])

        start = datetime.datetime.utcnow()

        job_results = build_tile_packages(
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
            api_key,
            args.concurrency)

        stop = datetime.datetime.utcnow()
        elapsed = (stop - start).total_seconds()

        metadata = {
            'metro_name': name,
            'extract_start_datetime': start.isoformat(),
            'extract_finish_datetime': stop.isoformat(),
            'number_tiles': job_results['number_tiles'],
        }

        with open(metadata_filename, 'w') as f:
            json.dump(metadata, f)

        print("Wrote packages for {} in {:0.2f} sec".format(name, elapsed))

if __name__ == '__main__':
    main()
