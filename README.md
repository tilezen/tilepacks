# tilepacks
Tools to build tile packages meant for offline usage.

## Installation

1. Clone the repository locally:

   ```
   git clone https://github.com/tilezen/tilepacks.git
   ```
   
2. Create a Python virtual environment and install dependencies:

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
