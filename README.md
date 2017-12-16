# tilepacks
Tools to build tile packages meant for offline usage.

## Installation

1. Clone the repository locally:

   ```
   git clone https://github.com/tilezen/tilepacks.git
   ```
   
2. Create a Python virtual environment and install dependencies (requires Python3):

  ```
  cd tilepacks
  virtualenv -p python3 env
  source env/bin/activate
  pip install -e .
  ```

3. Run the `tilepack` command to get command-line help.

  ```
  $ tilepack
  usage: tilepack [-h] [--tile-format TILE_FORMAT]
                  [--output-formats OUTPUT_FORMATS] [-j CONCURRENCY]
                  min_lon min_lat max_lon max_lat min_zoom max_zoom output
  tilepack: error: the following arguments are required: min_lon, min_lat, max_lon, max_lat, min_zoom, max_zoom, output
  ```
  
  defaults: MVT tiles as a zipfile and an mbtiles package.
  
  TILE_FORMAT: default is `mvt`. `topojson`, `json` also available
  OUTPUT_FORMATS: default is both `zipfile` and `mbtiles`
  CONCURRENCY: default is ?, x to y

  sample command for 512px topojson tiles for San Francisco:
  
  `MAPZEN_API_KEY=mapzen-xxxxxx tilepack -122.51489 37.70808 -122.35698 37.83239 10 16 sf --tile-size 512 --tile-format topojson`
   
