import math


def convert_size(size_bytes):
    if size_bytes == 0 or size_bytes is None:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


class Callback:
    def __init__(self, callback, **kwargs):
        self.callback = callback
        self.kwargs = kwargs

    def __call__(self, *args):
        return self.callback(*args, **self.kwargs)

def size_verbose(size):
    if size < 1024:
        return str(size) + 'B'
    elif size < 1024 * 1024:
        return str(round(size / 1024, 2)) + 'KB'
    elif size < 1024 * 1024 * 1024:
        return str(round(size / 1024 / 1024, 2)) + 'MB'
    elif size < 1024 * 1024 * 1024 * 1024:
        return str(round(size / 1024 / 1024 / 1024, 2)) + 'GB'
    else:
        return str(round(size / 1024 / 1024 / 1024 / 1024, 2)) + 'TB'
