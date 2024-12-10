from __future__ import annotations

import sys
from contextlib import contextmanager
from datetime import tzinfo
from decimal import Decimal
from ipaddress import IPv4Address, IPv6Address
from pathlib import Path
from sqlite3 import Connection, Cursor, connect
from typing import Any, Generator
from urllib.parse import ParseResult, unquote, urlparse

from zut import Header, build_url
from zut.db.base import DbAdapter, T_Connection


class SqliteAdapter(DbAdapter[Connection, Cursor]):
    """
    Database adapter for SQLite 3 (using driver included in python3).
    """
    scheme = 'sqlite'
    default_schema = None
    split_multi_statement_files = True
    table_in_path = False # URL may be a path
    sql_placeholder = '?'
    sql_named_placeholder = ':%s'
    int_sql_type = 'integer'
    datetime_aware_sql_type = None
    datetime_naive_sql_type = 'real'
    identity_definition_sql = 'AUTOINCREMENT'
    truncate_with_delete = True
    can_cascade_truncate = False
    temporary_prefix = 'temp.'

    # Configurable globally
    mkdir = False
    
    @classmethod
    def is_available(cls):
        return True
    

    def __init__(self, db: T_Connection|str|Path|dict|ParseResult, *, password_required: bool = False, autocommit: bool = True, tz: tzinfo|str|None = None, mkdir: bool = None, **kwargs):
        if isinstance(db, Path):
            self._file = db.as_posix()
            db = build_url(scheme='sqlite', path=self._file)
        elif isinstance(db, str) and not db.startswith(('sqlite:', 'sqlite3:')) and db.endswith(('.db','.sqlite','.sqlite3')):
            self._file = db.replace('\\', '/')
            db = build_url(scheme='sqlite', path=self._file)
        else:
            self._file = None

        super().__init__(db, password_required=password_required, autocommit=autocommit, tz=tz, **kwargs)

        self.mkdir = mkdir if mkdir is not None else self.__class__.mkdir


    @property
    def file(self):
        if self._file is None:
            url = self.get_url()
            self._file = unquote(urlparse(url).path)
        return self._file

    
    @property
    def is_port_opened(self):
        from zut import files
        return files.exists(self._file)
   

    def create_connection(self, *, autocommit: bool, **kwargs) -> Connection:        
        if self.mkdir:
            from zut import files
            dir_path = files.dirname(self.file)
            if dir_path:
                files.makedirs(dir_path, exist_ok=True)

        if sys.version_info < (3, 12): # Sqlite connect()'s autocommit parameter introduced in Python 3.12
            return connect(self.file, isolation_level=None if autocommit else 'DEFERRED', **kwargs)
        else:
            return connect(self.file, autocommit=autocommit, **kwargs)
        

    @property
    def autocommit(self):
        if sys.version_info < (3, 12): # Sqlite connect()'s autocommit parameter introduced in Python 3.12
            return self._autocommit
        else:
            return super().autocommit


    @contextmanager
    def cursor(self, *, autoclose=True, **kwargs) -> Generator[Cursor, Any, Any]:
        # sqlite3's cursor is not a context manager so we have to wrap it
        yield super().cursor(autoclose=autoclose, **kwargs)
    

    def _get_url_from_connection(self):
        seq, name, file = self.get_tuple("PRAGMA database_list")
        return build_url(scheme=self.scheme, path=file)


    def table_exists(self, table: str|tuple = None, *, cursor = None) -> bool:
        schema, table = self.split_name(table)
        
        if schema == 'temp':
            query = "SELECT COUNT(*) FROM sqlite_temp_master WHERE type = 'table' AND name = ?"
        elif not schema:
            query = "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table' AND name = ?"
        else:
            raise ValueError(f'Cannot use schema "{schema}"')
        
        return self.get_scalar(query, [table], cursor=cursor) > 0
    

    def _get_table_headers(self, schema, table, cursor) -> list[Header]:
        sql = f"""
SELECT
	c.name
	,lower(c."type") AS sql_type
	,CASE WHEN c."notnull" = 1 THEN 0 ELSE 1 END AS "null"
	,c.pk AS primary_key	
	,CASE WHEN lower(c."type") = 'integer' AND c.pk = 1 AND lower(t."sql") LIKE '%autoincrement%' THEN 1 ELSE 0 END AS "identity" -- For sqlite, AUTOINCREMENT columns are necessarily INTEGER PRIMARY KEY columns
	-- ROADMAP: c.dflt_value
FROM {'temp' if schema == 'temp' else 'main'}.pragma_table_info(?) c
LEFT OUTER JOIN sqlite{'_temp' if schema == 'temp' else ''}_master t ON t.name = ?
ORDER BY c.cid
"""
        
        results = self.get_dicts(sql, [table, table], cursor=cursor)

        # Add 'unique' info
        uniques: dict[str, bool|list[list[str]]] = {}
        for index_name in self.get_scalars(f'SELECT name FROM {"temp" if schema == "temp" else "main"}.pragma_index_list(?) WHERE "unique" = 1 ORDER BY name', [table], cursor=cursor):
            index_columns = sorted(self.get_scalars(f'SELECT name FROM {"temp" if schema == "temp" else "main"}.pragma_index_info(?) ORDER BY cid', [index_name], cursor=cursor))
            for column in index_columns:
                column_uniques = uniques.get(column)
                if len(index_columns) == 1:
                    uniques[column] = True
                else:
                    if column_uniques is None:
                        uniques[column] = [index_columns]
                    elif column_uniques is not True:
                        column_uniques.append(index_columns)

        for result in results:
            result['unique'] = uniques.get(result['name'], False)
            if isinstance(result['unique'], list):
                result['unique'].sort()

        return results


    def convert_value(self, value: Any):
        if isinstance(value, (IPv4Address,IPv6Address)):
            return value.compressed
        elif isinstance(value, Decimal):
            return str(value)
        else:
            return super().convert_value(value)
