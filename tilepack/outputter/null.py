class NullOutput(object):
    @staticmethod
    def build_from_basename(basename, **kwargs):
        return NullOutput(basename, **kwargs)

    def __init__(self, filename, **kwargs):
        pass

    def add_metadata(self, name, value):
        pass

    def open(self):
        pass

    def add_tile(self, tile_info, data):
        pass

    def close(self):
        pass
