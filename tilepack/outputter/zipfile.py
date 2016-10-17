import zipfile

class ZipfileOutput(object):
    @staticmethod
    def build_from_basename(basename, **kwargs):
        return ZipfileOutput(basename + ".zip", **kwargs)

    def __init__(self, filename, **kwargs):
        self._filename = filename
        self._zipfile = None

    def open(self):
        self._zipfile = zipfile.ZipFile(self._filename, 'w', compression=zipfile.ZIP_DEFLATED)

    def add_tile(self, tile_info, data):
        key = '{layer}/{zoom}/{x}/{y}.{fmt}'.format(**tile_info)
        self._zipfile.writestr(key, data)

    def close(self):
        self._zipfile.close()

