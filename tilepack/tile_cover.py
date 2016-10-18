from tilepack.builder import cover_bbox

import argparse
import os
import requests

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('min_zoom',
        type=int,
        help='The minimum zoom level to include')
    parser.add_argument('max_zoom',
        type=int,
        help='The maximum zoom level to include')
    parser.add_argument('--cities_url',
        default="https://raw.githubusercontent.com/mapzen/metroextractor-cities/master/cities.geojson",
        help='A GeoJSON URL with features to cover with tiles')
    parser.add_argument('--output_prefix',
        default="output",
        help='The path prefix to output coverage data to')
    args = parser.parse_args()

    cities_resp = requests.get(args.cities_url)
    cities_resp.raise_for_status()
    cities_data = cities_resp.json()

    features = cities_data['features']
    for feature in features:
        min_lon, min_lat, max_lon, max_lat = feature['bbox']
        feature['properties']['area'] = (max_lon - min_lon) * (max_lat - min_lat)
    biggest_features = sorted(features, key=lambda f: f['properties']['area'], reverse=True)[:200]

    for feature in biggest_features:
        name = feature['properties']['name']
        min_lon, min_lat, max_lon, max_lat = feature['bbox']
        count = 0
        with open(os.path.join(args.output_prefix, '{}.csv'.format(name)), 'w') as f:
            for zoom in range(args.min_zoom, args.max_zoom + 1):
                for x, y, z in cover_bbox(min_lon, min_lat, max_lon, max_lat, zoom=zoom):
                    f.write('{}/{}/{}\n'.format(z, x, y))
                    count += 1
        print("Wrote out {} tiles to {}".format(count, f.name))

if __name__ == '__main__':
    main()
