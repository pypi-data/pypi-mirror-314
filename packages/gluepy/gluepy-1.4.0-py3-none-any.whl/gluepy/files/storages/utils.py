from io import BytesIO
import matplotlib.pyplot as plt
from contextlib import contextmanager
from . import default_storage


@contextmanager
def plot(file_path: str, root: bool = False):
    file_path = file_path if root is True else default_storage.runpath(file_path)

    stream = BytesIO()
    try:
        yield plt
    finally:
        plt.savefig(stream)
        plt.close()
        stream.seek(0)
        default_storage.touch(file_path, stream)
