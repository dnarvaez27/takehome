import os
from multiprocessing import Pool
from src.utils import FileData


def extract_file_data(path: str):
    _, ext = os.path.splitext(path)
    size = os.path.getsize(path)
    filename = os.path.basename(path)[:-len(ext)]

    return FileData(filename=filename, extension=ext[1:], size_in_bytes=size, path=path)


def traverse_files(directory: str, *, concurrency=4):
    with Pool(concurrency) as pool:
        walk_res = os.walk(directory)
        files = [os.path.join(root, file) for root, _, files in walk_res for file in files]

        return pool.map(extract_file_data, files)
