import os
from multiprocessing import Pool
from src.utils import FileData


def extract_file_data(path: str):
    _, ext = os.path.splitext(path)
    size = os.path.getsize(path)
    filename = os.path.basename(path)
    return (path, filename, ext[1:] or None, size)


def walk(directory: str, *, concurrency=4):
    with Pool(concurrency) as pool:
        walk_res = os.walk(directory)
        files = [os.path.join(root, file) for root, _, files in walk_res for file in files]

        return pool.map(extract_file_data, files)


def extract_dir_info(directory: str, *, concurrency=4):
    for path, filename, extension, size_in_bytes in walk(directory, concurrency=concurrency):
        yield FileData(filename=filename, extension=extension, size_in_bytes=size_in_bytes, path=path)
