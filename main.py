from src.file_utils import extract_dir_info
from src.indexer import Index


def populate_to_index():
    return extract_dir_info('./test_data', concurrency=2)


def run():
    index = Index(populate_to_index)

    for row in index.search('filename:user*'):
        print(row)


if __name__ == '__main__':
    run()
