import mercantile
import argparse

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
    args = parser.parse_args()

    print("zoom\tmissing from toi\tin aoi")

    for zoom in range(args.min_zoom, args.max_zoom + 1):
        tiles_in_aoi = set([
            '{}/{}/{}'.format(z, x, y)
            for x, y, z in mercantile.tiles(
                args.min_lon, args.min_lat, args.max_lon, args.max_lat,
                [zoom]
            )
        ])

        with open('toi.z{}.txt'.format(zoom), 'r') as f:
            tiles_in_toi = set([
                l.strip()
                for l in f.readlines()
            ])

        print("{zoom:2d}\t{tiles_not_in_toi}\t{tiles_in_aoi}".format(
            zoom=zoom,
            tiles_not_in_toi=len(tiles_in_aoi - tiles_in_toi),
            tiles_in_aoi=len(tiles_in_aoi),
        ))


if __name__ == '__main__':
    main()
