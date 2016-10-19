import sqlite3

class MbtilesOutput(object):
    @staticmethod
    def build_from_basename(basename, **kwargs):
        return MbtilesOutput(basename + ".mbtiles", **kwargs)

    def __init__(self, filename, **kwargs):
        self._filename = filename

    def _setup_mbtiles(self, cur):
        cur.execute("""
            CREATE TABLE tiles (
            zoom_level integer,
            tile_column integer,
            tile_row integer,
            tile_data blob);
            """)
        cur.execute("""
            CREATE TABLE metadata
            (name text, value text);
            """)
        cur.execute("""
            CREATE TABLE grids (
            zoom_level integer,
            tile_column integer,
            tile_row integer,
            grid blob);
            """)
        cur.execute("""
            CREATE TABLE grid_data (
            zoom_level integer,
            tile_column integer,
            tile_row integer,
            key_name text,
            key_json text);
            """)
        cur.execute("""
            CREATE UNIQUE INDEX name ON metadata (name);
            """)
        cur.execute("""
            CREATE UNIQUE INDEX tile_index ON tiles (
            zoom_level, tile_column, tile_row);
            """)

    def _optimize_connection(self, cur):
        cur.execute("""
            PRAGMA synchronous=0
            """)
        cur.execute("""
            PRAGMA locking_mode=EXCLUSIVE
            """)
        cur.execute("""
            PRAGMA journal_mode=DELETE
            """)

    def _flip_y(self, zoom, row):
        """
        mbtiles requires WMTS (origin in the upper left),
        and Tilezen stores in TMS (origin in the lower left).
        This adjusts the row/y value to match WMTS.
        """

        if row is None or zoom is None:
            raise TypeError("zoom and row cannot be null")

        return (2 ** zoom) - 1 - row

    def add_metadata(self, name, value):
        self._cur.execute("""
            INSERT INTO metadata (
                name, value
            ) VALUES (
                ?, ?
            );
            """,
            (
                name,
                value,
            )
        )

    def open(self):
        self._conn = sqlite3.connect(self._filename)
        self._cur = self._conn.cursor()
        self._optimize_connection(self._cur)
        self._setup_mbtiles(self._cur)

    def add_tile(self, tile_info, data):
        self._cur.execute("""
            INSERT INTO tiles (
                zoom_level, tile_column, tile_row, tile_data
            ) VALUES (
                ?, ?, ?, ?
            );
            """,
            (
                tile_info.get('zoom'),
                tile_info.get('x'),
                self._flip_y(tile_info.get('zoom'), tile_info.get('y')),
                sqlite3.Binary(data),
            )
        )

    def close(self):
        self._conn.commit()
        self._conn.close()
