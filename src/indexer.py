import os
from typing import Iterable
from whoosh import fields
from whoosh.fields import Schema
from whoosh.index import create_in, open_dir, FileIndex
from whoosh.multiproc import MpWriter
from whoosh import writing as whoosh_writing
from whoosh.writing import SegmentWriter
from whoosh.qparser import QueryParser
from whoosh import query as whoosh_query
from whoosh.query.qcore import Query
from src.utils import InvalidQueryException, FileData

INDEX_DIR = '.index'
DEFAULT_SEARCH_FIELD = 'filename'

schema = Schema(filename=fields.TEXT(stored=True),
                extension=fields.TEXT(stored=True),
                size=fields.NUMERIC(stored=True),
                path=fields.ID(stored=True))


class Types:
    Index = FileIndex
    Writter = MpWriter | SegmentWriter  # pylint: disable=unsupported-binary-operation
    NullQuery = whoosh_query.NullQuery


class Index:

    def __init__(self) -> None:
        self.index, _ = Index.__open_index()

    @staticmethod
    def __open_index() -> tuple[Types.Index, bool]:
        if os.path.exists(INDEX_DIR):
            return open_dir(INDEX_DIR, schema=schema), True

        os.mkdir(INDEX_DIR)
        return create_in(INDEX_DIR, schema=schema), False

    def add_documents(self, doc: Iterable[FileData]):
        with self.index.writer() as index_writter:
            i = 0

            for i, file_data in enumerate(doc):
                print('Indexing', i + 1, '       ', end='\r')
                index_writter.add_document(path=file_data.path,
                                           filename=file_data.filename,
                                           extension=file_data.extension,
                                           size=file_data.size_in_bytes)

            print('Indexed', i + 1, 'documents            ')

    def clear(self):
        self.index.writer().commit(mergetype=whoosh_writing.CLEAR)

    def search(self, query_str: str, limit: int = 10):
        with self.index.searcher() as searcher:
            query = Index.__parse_query(query_str)
            print('Searching with query:', query, '\n')

            res = searcher.search(query, limit=limit)
            for r in res:
                yield FileData.from_index(r.fields())

    @staticmethod
    def __parse_query(query_str: str) -> Query:
        parser = QueryParser(DEFAULT_SEARCH_FIELD, schema)
        query = parser.parse(query_str)

        if query == Types.NullQuery:
            raise InvalidQueryException(query_str)

        return query

    def close(self):
        self.index.close()
