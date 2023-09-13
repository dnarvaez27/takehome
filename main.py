from typing import Optional
from enum import Enum
import qprompt
from src.file_utils import traverse_files
from src.indexer import Index
from src.utils import InvalidQueryException

DEFAULT_DIR = './test_data'
TRAVERSAL_PROCESSES = 2
MAX_SEARCH_RESULTS = 50


class MenuOptions(Enum):
    SEARCH = ('s', 'Search query')
    REFRESH = ('r', 'Refresh the index')
    QUIT = ('q', 'Quit')

    def __init__(self, key: str, title: str):
        self.key = key
        self.title = title


def show_menu():
    qprompt.echo('\nWhat do you want to do?')
    menu = qprompt.Menu()
    menu.add(MenuOptions.SEARCH.key, MenuOptions.SEARCH.title)
    menu.add(MenuOptions.REFRESH.key, MenuOptions.REFRESH.title)
    menu.add(MenuOptions.QUIT.key, MenuOptions.QUIT.title)
    return menu.show()


def make_search(index: Index):
    query = qprompt.ask_str('Input your search query?')
    if not query:
        return

    try:
        res = index.search(query, limit=MAX_SEARCH_RESULTS)
        qprompt.hrule()
        for row in res:
            print(row)
        qprompt.hrule()
    except InvalidQueryException:
        qprompt.alert('Invalid query')
        make_search(index)


def refresh_index(index: Index):
    dir_path = qprompt.ask_str(f'Enter directory path (default to {DEFAULT_DIR})')
    index.clear()
    index.add_documents(traverse_files(dir_path or DEFAULT_DIR, concurrency=TRAVERSAL_PROCESSES))


def prompt(index: Optional[Index]):
    choice = show_menu()
    if choice == MenuOptions.QUIT.key:
        if index:
            index.close()
        return

    if not index:
        index = Index()

    if choice == MenuOptions.REFRESH.key:
        refresh_index(index)
    elif choice == MenuOptions.SEARCH.key:
        make_search(index)

    prompt(index)


if __name__ == '__main__':
    prompt(index=None)
