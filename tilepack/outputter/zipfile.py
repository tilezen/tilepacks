import zipfile
import json

class ZipfileOutput(object):
    @staticmethod
    def build_from_basename(basename, **kwargs):
        return ZipfileOutput(basename + ".zip", **kwargs)

    def __init__(self, filename, **kwargs):
        self._filename = filename
        self._zipfile = None
        self._metadata = {}

    def add_metadata(self, name, value):
        self._metadata[name] = value

    def open(self):
        self._zipfile = zipfile.ZipFile(self._filename, 'w', compression=zipfile.ZIP_DEFLATED)

    def add_tile(self, tile_info, data):
        key = '{layer}/{zoom}/{x}/{y}.{fmt}'.format(**tile_info)
        self._zipfile.writestr(key, data)

    def close(self):
        self._zipfile.writestr('metadata.json', json.dumps(dict(metadata=self._metadata)).encode('utf-8'))
        self._zipfile.close()

