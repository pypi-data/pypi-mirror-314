from __future__ import annotations

from enum import Enum, Flag
import logging
import re
from contextlib import nullcontext
from datetime import datetime, time, tzinfo
from io import IOBase, StringIO
from pathlib import Path
from secrets import token_hex
import socket
from threading import current_thread
from time import time_ns
from typing import Any, Generic, Iterable, Mapping, Sequence, TypeVar
from urllib.parse import ParseResult, parse_qs, quote, unquote, urlparse

from zut import (ZUT_ROOT, Literal, NotFoundError, Row, ColumnsProvider, SeveralFoundError, TabDumper, TabularDumper, CsvDumper, Header, build_url, hide_url_password, is_aware, make_aware, make_naive, now_naive_utc, parse_tz, slugify, tabular_dumper, files)

try:
    from django.db.models import Model
    _with_django = True
except ImportError:
    _with_django = False


T_Connection = TypeVar('T_Connection')
T_Cursor = TypeVar('T_Cursor')


class DbAdapter(Generic[T_Connection, T_Cursor]):
    """
    Base class for database adapters.
    """

    # DB engine specifics
    scheme: str
    default_port: int
    default_schema: str|None = 'public'
    only_positional_params = False
    split_multi_statement_files = False
    table_in_path = True
    identifier_quotechar = '"'
    sql_placeholder = '%s'
    sql_named_placeholder = '%%(%s)s'
    int_sql_type = 'bigint'
    float_sql_type = 'float'
    str_sql_type = 'text'
    str_key_sql_type = 'varchar(255)' # type for key limited to 255 characters (max length for a 1-bit length VARCHAR on MariaDB)
    datetime_naive_sql_type = 'timestamp'
    datetime_aware_sql_type: str|None = 'timestamptz'
    truncate_with_delete = False
    can_cascade_truncate = True
    identity_definition_sql = 'GENERATED ALWAYS AS IDENTITY'
    procedure_caller = 'CALL'
    procedure_params_parenthesis = True
    function_requires_schema = False
    can_add_several_columns = False
    temporary_prefix = 'pg_temp.'
    
    # Global configurable
    default_autocommit = True
    use_http404 = False
    """ Use Django's HTTP 404 exception instead of NotFoundError (if Django is available). """

    @classmethod
    def is_available(cls):
        raise NotImplementedError()
    

    def __init__(self, origin: T_Connection|str|dict|ParseResult, *, password_required: bool = False, autocommit: bool = None, tz: tzinfo|str|None = None, table: str|None = None, schema: str|None = None):
        """
        Create a new adapter.
        - `origin`: an existing connection object, or the URL or django alias (e.g. 'default') for the new connection to create by the adapter.
        - `autocommit`: commit transactions automatically (applies only for connections created by the adapter).
        - `tz`: naive datetimes in results are made aware in the given timezone.
        """
        if not self.is_available():
            raise ValueError(f"Cannot use {type(self).__name__} (not available)")
        
        self._logger = logging.getLogger(f"{__name__}.{self.__class__.__qualname__}")
        
        self.table: str = table
        """ A specific table associated to this adapter. Used for example as default table for `dumper`. """

        self.schema: str = schema
        """ A specific schema associated to this adapter. Used for example as default table for `dumper`. """

        
        if isinstance(origin, (str,ParseResult)):
            self._close_connection = True
            self._connection: T_Connection = None
            if isinstance(origin, ParseResult) or ':' in origin or '/' in origin or ';' in origin or ' ' in origin:
                r = origin if isinstance(origin, ParseResult) else urlparse(origin)

                if r.fragment:
                    raise ValueError(f"Invalid {self.__class__.__name__}: unexpected fragment: {r.fragment}")
                if r.params:
                    raise ValueError(f"Invalid {self.__class__.__name__}: unexpected params: {r.params}")
                
                query = parse_qs(r.query)
                query_schema = query.pop('schema', [None])[-1]
                if query_schema and self.schema is None:
                    self.schema = query_schema
                query_table = query.pop('table', [None])[-1]                
                if query_table and self.table is None:
                    self.table = query_table
                if query:
                    raise ValueError(f"Invalid {self.__class__.__name__}: unexpected query data: {query}")
                
                scheme = r.scheme
                r = self._verify_scheme(r)
                if not r:
                    raise ValueError(f"Invalid {self.__class__.__name__}: invalid scheme: {scheme}")

                if not self.table and self.table_in_path:
                    table_match = re.match(r'^/?(?P<name>[^/@\:]+)/((?P<schema>[^/@\:\.]+)\.)?(?P<table>[^/@\:\.]+)$', r.path)
                else:
                    table_match = None

                if table_match:
                    if self.table is None:
                        self.table = table_match['table']
                    if self.schema is None:
                        self.schema = table_match['schema'] if table_match['schema'] else None
                
                    r = r._replace(path=table_match['name'])
                    self._connection_url = r.geturl()
                
                else:
                    self._connection_url = r.geturl()
            
            else:
                from django.conf import settings
                if not origin in settings.DATABASES:
                    raise ValueError(f"key \"{origin}\" not found in django DATABASES settings")
                config: dict[str,Any] = settings.DATABASES[origin]
                
                self._connection_url = build_url(
                    scheme = self.scheme,
                    hostname = config.get('HOST', None),
                    port = config.get('PORT', None),
                    username = config.get('USER', None),
                    password = config.get('PASSWORD', None),
                    path = config.get('NAME', None),
                )
                if not self.table:
                    self.table = config.get('TABLE', None)
                if not self.schema:
                    self.schema = config.get('SCHEMA', None)

        elif isinstance(origin, dict):
            self._close_connection = True
            self._connection: T_Connection = None

            if 'NAME' in origin:
                # uppercase (as used by django)
                self._connection_url = build_url(
                    scheme = self.scheme,
                    hostname = origin.get('HOST', None),
                    port = origin.get('PORT', None),
                    username = origin.get('USER', None),
                    password = origin.get('PASSWORD', None),
                    path = origin.get('NAME', None),
                )
                if not self.table:
                    self.table = origin.get('TABLE', None)
                if not self.schema:
                    self.schema = origin.get('SCHEMA', None)

            else:
                # lowercase (as used by some drivers' connection kwargs)
                self._connection_url = build_url(
                    scheme = self.scheme,
                    hostname = origin.get('host', None),
                    port = origin.get('port', None),
                    username = origin.get('user', None),
                    password = origin.get('password', None),
                    path = origin.get('name', origin.get('dbname', None)),
                )
                if not self.table:
                    self.table = origin.get('table', None)
                if not self.schema:
                    self.schema = origin.get('schema', None)

        else:
            origin = _get_connection_from_wrapper(origin)
            self._connection = origin
            self._connection_url: str = None
            self._close_connection = False
        
        self.password_required = password_required
        if isinstance(tz, str):
            tz = tz if tz == 'localtime' else parse_tz(tz)
        self.tz = tz
        
        self._autocommit = autocommit if autocommit is not None else self.__class__.default_autocommit
        self._last_autoclose_cursor = None
        self._is_port_opened = None
    
    
    def _verify_scheme(self, r: ParseResult) -> ParseResult|None:
        if r.scheme == self.scheme:
            return r
        else:
            return None

    def get_url(self, *, hide_password = False):
        if self._connection_url:
            url = self._connection_url
        else:
            url = self._get_url_from_connection()

        if hide_password:
            url = hide_url_password(url)

        if self.table:
            if self.table_in_path:
                url += f"/"
                if self.schema:
                    url += quote(self.schema)
                    url += '.'
                url += quote(self.table)
            else:
                url += f"?table={quote(self.table)}"
                if self.schema:
                    url += f"&schema={quote(self.schema)}"

        return url


    def _get_url_from_connection(self):
        raise NotImplementedError()
    

    def get_db_name(self):
        url = self.get_url()
        r = urlparse(url)
        return unquote(r.path).lstrip('/')


    @property
    def is_port_opened(self):
        if self._is_port_opened is None:
            r = urlparse(self.get_url())
            host = r.hostname or '127.0.0.1'
            port = r.port if r.port is not None else self.default_port
        
            if self._logger.isEnabledFor(logging.DEBUG):
                self._logger.debug("Check host %s, port %s (from thread %s)", host, port, current_thread().name)

            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((host, port))
                if result == 0:
                    self._logger.debug("Host %s, port %s: connected", host, port)
                    self._is_port_opened = True
                else:
                    self._logger.debug("Host %s, port %s: NOT connected", host, port)
                    self._is_port_opened = False
                sock.close()
            except Exception as err:
                raise ValueError(f"Cannot check host {host}, port {port}: {err}")
        
        return self._is_port_opened
    

    #region Connection

    def __enter__(self):
        return self


    def __exit__(self, exc_type = None, exc_value = None, exc_traceback = None):
        self.close()


    def close(self):
        if self._last_autoclose_cursor:
            # NOTE: for SqlServer/PyODBC, this should be enough to avoid committing when autocommit is False because we don't call __exit__()
            # See: https://github.com/mkleehammer/pyodbc/wiki/Cursor#context-manager
            self._last_autoclose_cursor.close()
            self._last_autoclose_cursor = None

        if self._connection and self._close_connection:
            if self._logger.isEnabledFor(logging.DEBUG):
                self._logger.debug(f"Close %s (%s) connection to %s", type(self).__name__, type(self._connection).__module__ + '.' + type(self._connection).__qualname__, hide_url_password(self._connection_url))
            self._connection.close()
            self._connection = None


    @property
    def connection(self):
        if not self._connection:                
            if self.password_required:
                password = urlparse(self._connection_url).password
                if not password:
                    raise ValueError("Cannot create %s connection to %s: password not provided" % (type(self).__name__, hide_url_password(self._connection_url)))
            if self._logger.isEnabledFor(logging.DEBUG):
                self._logger.debug(f"Create %s connection to %s", type(self).__name__, hide_url_password(self._connection_url))
            self._connection = self.create_connection(autocommit=self._autocommit)
        return self._connection
    

    @property
    def autocommit(self):
        if not self._connection:
            return self._autocommit
        else:
            return self._connection.autocommit


    def create_connection(self, *, autocommit: bool, **kwargs) -> T_Connection:
        raise NotImplementedError()


    def cursor(self, *, autoclose=True, **kwargs) -> T_Cursor:
        """
        A new cursor object that support the context manager protocol
        """
        if autoclose:
            if self._last_autoclose_cursor:
                self._last_autoclose_cursor.close()
                self._last_autoclose_cursor = None
            self._last_autoclose_cursor = self.connection.cursor(**kwargs)
            return self._last_autoclose_cursor
        else:
            return self.connection.cursor(**kwargs)

    #endregion
    

    #region Queries

    def to_positional_params(self, query: str, params: dict) -> tuple[str, Sequence[Any]]:
        from sqlparams import \
            SQLParams  # not at the top because the enduser might not need this feature

        if not hasattr(self.__class__, '_params_formatter'):
            self.__class__._params_formatter = SQLParams('named', 'qmark')
        query, params = self.__class__._params_formatter.format(query, params)

        return query, params
    

    def get_paginated_select_queries(self, query: str, *, limit: int|None, offset: int|None) -> tuple[str,str]:        
        if limit is not None:
            if isinstance(limit, str) and re.match(r"^[0-9]+$", limit):
                limit = int(limit)
            elif not isinstance(limit, int):
                raise TypeError(f"Invalid type for limit: {type(limit).__name__} (expected int)")
            
        if offset is not None:
            if isinstance(offset, str) and re.match(r"^[0-9]+$", offset):
                offset = int(offset)
            elif not isinstance(offset, int):
                raise TypeError(f"Invalid type for offset: {type(limit).__name__} (expected int)")
        
        beforepart, selectpart, orderpart = self._parse_select_query(query)

        paginated_query = beforepart
        total_query = beforepart
        
        paginated_query += self._paginate_parsed_query(selectpart, orderpart, limit=limit, offset=offset)
        total_query += f"SELECT COUNT(*) FROM ({selectpart}) s"

        return paginated_query, total_query
    

    def _parse_select_query(self, query: str):
        import sqlparse  # not at the top because the enduser might not need this feature

        # Parse SQL to remove token before the SELECT keyword
        # example: WITH (CTE) tokens
        statements = sqlparse.parse(query)
        if len(statements) != 1:
            raise sqlparse.exceptions.SQLParseError(f"Query contains {len(statements)} statements")

        # Get first DML keyword
        dml_keyword = None
        dml_keyword_index = None
        order_by_index = None
        for i, token in enumerate(statements[0].tokens):
            if token.ttype == sqlparse.tokens.DML:
                if dml_keyword is None:
                    dml_keyword = str(token).upper()
                    dml_keyword_index = i
            elif token.ttype == sqlparse.tokens.Keyword:
                if order_by_index is None:
                    keyword = str(token).upper()
                    if keyword == "ORDER BY":
                        order_by_index = i

        # Check if the DML keyword is SELECT
        if not dml_keyword:
            raise sqlparse.exceptions.SQLParseError(f"Not a SELECT query (no DML keyword found)")
        if dml_keyword != 'SELECT':
            raise sqlparse.exceptions.SQLParseError(f"Not a SELECT query (first DML keyword is {dml_keyword})")

        # Get part before SELECT (example: WITH)
        if dml_keyword_index > 0:
            tokens = statements[0].tokens[:dml_keyword_index]
            beforepart = ''.join(str(token) for token in tokens)
        else:
            beforepart = ''
    
        # Determine actual SELECT query
        if order_by_index is not None:
            tokens = statements[0].tokens[dml_keyword_index:order_by_index]
            selectpart = ''.join(str(token) for token in tokens)
            tokens = statements[0].tokens[order_by_index:]
            orderpart = ''.join(str(token) for token in tokens)
        else:
            tokens = statements[0].tokens[dml_keyword_index:]
            selectpart = ''.join(str(token) for token in tokens)
            orderpart = ''

        return beforepart, selectpart, orderpart
    

    def _paginate_parsed_query(self, selectpart: str, orderpart: str, *, limit: int|None, offset: int|None) -> str:
        result = f"{selectpart} {orderpart}"
        if limit is not None:
            result += f" LIMIT {limit}"
        if offset is not None:
            result += f" OFFSET {offset}"
        return result
    

    def _get_select_table_query(self, table: str|tuple = None, *, schema_only = False) -> str:
        """
        Build a query on the given table.

        If `schema_only` is given, no row will be returned (this is used to get information on the table).
        Otherwise, all rows will be returned.

        The return type of this function depends on the database engine.
        It is passed directly to the cursor's execute function for this engine.
        """
        schema, table = self.split_name(table)
        
        query = f'SELECT * FROM'
        if schema:
            query += f' {self.escape_identifier(schema)}.'
        query += f'{self.escape_identifier(table)}'
        if schema_only:
            query += ' WHERE 1 = 0'

        return query
    

    @classmethod
    def escape_identifier(cls, value: str) -> str:
        if not isinstance(value, str):
            raise TypeError(f"Invalid identifier: {value} (type: {type(value)})")
        if not cls.identifier_quotechar:
            raise ValueError(f"{cls.__name__}'s identifier_quotechar not defined")
        if cls.identifier_quotechar in value:
            raise ValueError(f"Identifier ({value}) cannot contain quote character ({cls.identifier_quotechar})")
        return f"{cls.identifier_quotechar}{value}{cls.identifier_quotechar}"


    @classmethod
    def escape_literal(cls, value) -> str:
        if value is None:
            return "null"
        else:
            return f"'" + str(value).replace("'", "''") + "'"
    
    
    #endregion
    

    #region Execution

    def execute_query(self, query: str, params: list|tuple|dict = None, *, cursor: T_Cursor = None, traverse: bool|Literal['warn'] = False, tz: tzinfo = None, limit: int = None, offset: int = None, query_id = None) -> DbResult[T_Cursor]:
        if limit is not None or offset is not None:
            query, _ = self.get_paginated_select_queries(query, limit=limit, offset=offset)
        
        # Example of positional param: cursor.execute("INSERT INTO foo VALUES (%s)", ["bar"])
        # Example of named param: cursor.execute("INSERT INTO foo VALUES (%(foo)s)", {"foo": "bar"})
        if params is None:
            params = []
        elif isinstance(params, dict) and self.only_positional_params:
            query, params = self.to_positional_params(query, params)

        if not cursor:
            cursor = self.cursor().__enter__() # will be closed in DbAdapter's next cursor() method, or in the final close() method

        with self._register_notice_handler(cursor, query_id=query_id):
            # Execute query
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            self._log_cursor_notices(cursor)

            if traverse:
                rows, columns = self._traverse_cursor(cursor, warn=traverse == 'warn', query_id=query_id)
            elif cursor.description:
                # None indicates to QueryResults to use the cursor
                rows, columns = None, [info[0] for info in cursor.description]
            else:
                rows, columns = [], []

            # Handle results
            return DbResult(self, cursor, rows=rows, columns=columns, query_id=query_id, tz=tz)

    
    def _register_notice_handler(self, cursor: T_Cursor, query_id = None):
        """
        Register a handle for messages produced during execution of a query or procedure.
        """
        return nullcontext()
    

    def _log_cursor_notices(self, cursor: T_Cursor):
        """
        Log messages produced during execution of a query or procedure, if this cannot be done through `_register_notice_handler`.
        """
        pass
    

    def _traverse_cursor(self, cursor: T_Cursor, *, warn: bool, query_id) -> tuple[list[tuple]|None, list[str]]:
        """
        Move to last result set of the cursor, returning (last_rows, last_columns).
        Useful mostfly for pyodbc on stored procedures.
        """
        if not cursor.description:
            # [] indicates to QueryResults that there are no rows
            return [], []
        
        columns = [info[0] for info in cursor.description]

        if warn:
            self._warn_if_rows(cursor, columns=columns, query_id=query_id)
            # [] indicates to QueryResults to not report rows that we just warned about
            return [], columns
        
        else:
            # None indicates to QueryResults to use the cursor
            return None, columns
        

    def _warn_if_rows(self, cursor: T_Cursor, *, columns: list[str], query_id):
        top_rows = []
        there_are_more = False
        iterator = iter(cursor)
        try:
            for i in range(11):
                row = next(iterator)
                if i < 10:
                    top_rows.append(row)
                else:
                    there_are_more = True
        except StopIteration:
            pass
        
        if not top_rows:
            return
        
        fp = StringIO()
        with (TabDumper if TabDumper.is_available() else CsvDumper)(fp, headers=columns) as dumper:
            for row in top_rows:
                dumper.append(row)
        text_rows = fp.getvalue()

        if there_are_more:
            text_rows += "\n…"

        self._logger.warning("Result set for query%s contain rows:\n%s", f" {query_id}" if query_id is not None else "", text_rows)


    def execute_file(self, path: str|Path, params: list|tuple|dict = None, *, cursor: T_Cursor = None, traverse: bool|Literal['warn'] = True, tz: tzinfo = None, limit: int = None, offset: int = None, query_id = None, encoding: str = 'utf-8', **file_kwargs) -> DbResult[T_Cursor]:
        file_content = files.read_text(path, encoding=encoding)

        if file_kwargs:
            file_content = file_content.format(**{key: '' if value is None else value for key, value in file_kwargs.items()})

        if self.split_multi_statement_files and ';' in file_content:
            # Split queries
            import sqlparse  # not at the top because the enduser might not need this feature
            queries = sqlparse.split(file_content, encoding)
            
            # Execute all queries
            query_count = len(queries)
    
            if not cursor:
                cursor = self.cursor().__enter__() # will be closed in DbAdapter's next cursor() method, or in the final close() method
        
            for index, query in enumerate(queries):
                query_num = index + 1
                if self._logger.isEnabledFor(logging.DEBUG):
                    title = re.sub(r"\s+", " ", query).strip()[0:100] + "…"
                    self._logger.debug("Execute query %d/%d: %s ...", query_num, query_count, title)

                # Execute query
                if query_id is not None and query_count > 1:
                    sub_id = f'{query_id}:{query_num}/{query_count}'
                elif query_id is not None or query_count > 1 :
                    sub_id = query_id
                elif query_count > 1:
                    sub_id = f'{query_num}/{query_count}'
                else:
                    sub_id = None
                
                results = self.execute_query(query, params, cursor=cursor, traverse='warn' if query_num < query_count else traverse, tz=tz, query_id=sub_id, limit=limit, offset=offset)

            return results
        else:
            return self.execute_query(file_content, params, cursor=cursor, traverse=traverse, tz=tz, limit=limit, offset=offset, query_id=query_id)
        
    
    def execute_function(self, name: str|tuple, params: list|tuple|dict = None, *, cursor: T_Cursor = None, traverse: bool|Literal['warn'] = True, tz: tzinfo = None, limit: int = None, offset: int = None, query_id = None, caller='SELECT', params_parenthesis=True) -> DbResult[T_Cursor]:
        schema, name = self.split_name(name)
        
        sql = f"{caller} "
        if not schema and self.function_requires_schema:
            schema = self.default_schema
        if schema:    
            sql += f"{self.escape_identifier(schema)}."
        sql += f"{self.escape_identifier(name)} "

        if params_parenthesis:
            sql += "("
                
        if isinstance(params, dict):
            list_params = []
            first = True
            for key, value in enumerate(params):
                if not key:
                    raise ValueError(f"Parameter cannot be empty")
                elif not re.match(r'^[\w\d0-9_]+$', key): # for safety
                    raise ValueError(f"Parameter contains invalid characters: {key}")
                
                if first:
                    first = False
                else:
                    sql += ','

                sql += f'{key}={self.sql_placeholder}'
                list_params.append(value)
        else:
            sql += ','.join([self.sql_placeholder] * len(params))
            list_params = params
    
        if params_parenthesis:
            sql += ")"

        if not query_id:
            query_id = f"{schema + '.' if schema and schema != self.default_schema else ''}{name}"

        return self.execute_query(sql, params, cursor=cursor, traverse=traverse, tz=tz, limit=limit, offset=offset, query_id=query_id)
    

    def execute_procedure(self, name: str|tuple, params: list|tuple|dict = None, *, cursor: T_Cursor = None, traverse: bool|Literal['warn'] = True, tz: tzinfo = None, limit: int = None, offset: int = None, query_id = None) -> DbResult[T_Cursor]:
        return self.execute_function(name, params, cursor=cursor, traverse=traverse, tz=tz, limit=limit, offset=offset, query_id=query_id, caller=self.procedure_caller, params_parenthesis=self.procedure_params_parenthesis)


    #endregion


    #region Results

    def get_scalar(self, query: str, params: list|tuple|dict = None, *, limit: int = None, offset: int = None, cursor: T_Cursor = None):
        with nullcontext(cursor) if cursor else self.cursor(autoclose=False) as cursor:
            results = self.execute_query(query, params, cursor=cursor, limit=limit, offset=offset)
            row = results.single()
            return row[0]


    def get_tuple(self, query: str, params: list|tuple|dict = None, *, limit: int = None, offset: int = None, cursor: T_Cursor = None):
        with nullcontext(cursor) if cursor else self.cursor(autoclose=False) as cursor:
            results = self.execute_query(query, params, cursor=cursor, limit=limit, offset=offset)
            row = results.single()
            return row.as_tuple()


    def get_dict(self, query: str, params: list|tuple|dict = None, *, limit: int = None, offset: int = None, cursor: T_Cursor = None):
        with nullcontext(cursor) if cursor else self.cursor(autoclose=False) as cursor:
            results = self.execute_query(query, params, limit=limit, offset=offset, cursor=cursor)
            row = results.single()
            return row.as_dict()
    

    def get_scalars(self, query: str, params: list|tuple|dict = None, *, limit: int = None, offset: int = None, cursor: T_Cursor = None):
        scalars = []

        with nullcontext(cursor) if cursor else self.cursor(autoclose=False) as cursor:
            results = self.execute_query(query, params, cursor=cursor, limit=limit, offset=offset)
            for row in results:
                scalars.append(row[0])

        return scalars


    def iter_dicts(self, query: str, params: list|tuple|dict = None, *, limit: int = None, offset: int = None, cursor: T_Cursor = None):
        with nullcontext(cursor) if cursor else self.cursor(autoclose=False) as cursor:
            results = self.execute_query(query, params, limit=limit, offset=offset, cursor=cursor)
            for row in results:
                yield row.as_dict()
                
    
    def get_dicts(self, query: str, params: list|tuple|dict = None, *, limit: int = None, offset: int = None, cursor: T_Cursor = None):
        with nullcontext(cursor) if cursor else self.cursor(autoclose=False) as cursor:
            results = self.execute_query(query, params, limit=limit, offset=offset, cursor=cursor)
            return results.as_dicts()
    

    def get_paginated_dicts(self, query: str, params: list|dict = None, *, limit: int, offset: int = 0, cursor: T_Cursor = None):
        paginated_query, total_query = self.get_paginated_select_queries(query, limit=limit, offset=offset)

        rows = self.get_dicts(paginated_query, params, cursor=cursor)
        total = self.get_scalar(total_query, params, cursor=cursor)
        return {"rows": rows, "total": total}

    #endregion


    #region Schemas, tables and columns

    def split_name(self, name: str|tuple|Model = None) -> tuple[str|None,str]:
        if name is None:
            if not self.table:
                raise ValueError("No table given")
            return self.schema, self.table
        
        if isinstance(name, tuple):
            return name
        
        if _with_django:
            if isinstance(name, Model):
                name = name._meta.db_table
                schema = self.schema
                return (schema, name)
        
        try:
            pos = name.index('.')
            schema = name[0:pos]
            name = name[pos+1:]
        except ValueError:
            schema = None
            name = name

        return (schema, name)
    

    def table_exists(self, table: str|tuple = None, *, cursor: T_Cursor = None) -> bool:
        raise NotImplementedError()

   
    def schema_exists(self, schema: str = None, *, cursor: T_Cursor = None) -> bool:        
        if self.default_schema is None:
            raise ValueError("This DbAdapter does not support schemas")
        raise NotImplementedError()
        

    def get_columns(self, table_or_cursor: str|tuple|T_Cursor = None, *, cursor: T_Cursor = None) -> list[str]:
        if table_or_cursor is None or isinstance(table_or_cursor, (str,tuple)):
            # table_or_cursor is assumed to be a table name (use self.table if None) 
            query = self._get_select_table_query(table_or_cursor, schema_only=True)
            with nullcontext(cursor) if cursor else self.cursor(autoclose=False) as cursor:
                cursor.execute(query)
                return self.get_columns(cursor)
        else:
            # table_or_cursor is assumed to be a cursor
            if not table_or_cursor.description:
                raise ValueError("No results in last executed query (no cursor description available)")
            return [info[0] for info in table_or_cursor.description]
        

    def get_headers(self, table_or_cursor: str|tuple|T_Cursor = None, *, cursor: T_Cursor = None) -> list[Header]:
        if table_or_cursor is None or isinstance(table_or_cursor, (str,tuple)):
            # table_or_cursor is assumed to be a table name (use self.table if None)        
            schema, table = self.split_name(table_or_cursor)
            with nullcontext(cursor) if cursor else self.cursor(autoclose=False) as cursor:
                results = self._get_table_headers(schema, table, cursor)
            headers: list[Header] = []

            def get_unique_from_together(unique_together: str):
                if unique_together:
                    unique = unique_together.split('|')
                    any_single = False
                    for i, u in enumerate(unique):
                        u = sorted(u.split(','))
                        unique[i] = u
                        if len(u) == 1:
                            any_single = True
                    if any_single:
                        return True
                    return sorted(unique)
                else:
                    return False

            for result in results:
                if isinstance(result, dict):                    
                    if isinstance(result['null'], int):
                        result['null'] = result['null'] == 1
                        
                    if isinstance(result['primary_key'], int):
                        result['primary_key'] = result['primary_key'] == 1

                    if isinstance(result['identity'], int):
                        result['identity'] = result['identity'] == 1

                    if 'unique_together' in result:
                        result['unique'] = get_unique_from_together(result.pop('unique_together', None))
                    headers.append(Header(**result))
                else:
                    if hasattr(result, 'unique_together'):
                        result.unique = get_unique_from_together(result.unique_together)
                        del result.unique_together
                    headers.append(result)

            return headers        

        else:
            # table_or_cursor is assumed to be a cursor
            if not table_or_cursor.description:
                raise ValueError("No results in last executed query (no cursor description available)")
            return self._get_cursor_headers(table_or_cursor)
    

    def _get_table_headers(self, schema, table, cursor) -> list[Header|dict]:            
        raise NotImplementedError()
    

    def _get_cursor_headers(self, cursor: T_Cursor) -> list[Header]:
        # ROADMAP: retrieve more Header settings
        return [Header(info[0]) for info in cursor.description]
    

    def _compute_sql_type(self, header: Header):
        # Try to determine sql_type from Python type
        if header.sql_type is not None:
            return header.sql_type
        elif header.type == int:
            return self.int_sql_type
        elif header.type == float:
            return self.float_sql_type
        # ROADMAP: more, in particular decimal (from tests.db)
        else:
            return self.str_sql_type
    

    def drop_table(self, table: str|tuple = None, *, if_exists = False, cursor: T_Cursor = None):
        schema, table = self.split_name(table)
        
        query = "DROP TABLE "
        if if_exists:
            query += "IF EXISTS "
        if schema:    
            query += f"{self.escape_identifier(schema)}."
        query += f"{self.escape_identifier(table)}"

        with self.cursor(autoclose=False) as cursor:
            self.execute_query(query, cursor=cursor)
    

    def truncate_table(self, table: str|tuple = None, *, if_exists = False, cascade = False, cursor: T_Cursor = None):
        if cascade:
            if not self.can_cascade_truncate or self.truncate_with_delete:
                raise ValueError(f"Cannot use cascade truncate with {self.__class__.__name__}")

        if self.truncate_with_delete:
            self.erase_table(table, if_exists=if_exists)
            return
        
        schema, table = self.split_name(table)
        
        with nullcontext(cursor) if cursor else self.cursor(autoclose=False) as cursor:
            if if_exists:
                if not self.table_exists((schema, table), cursor=cursor):
                    return
            
            query = "TRUNCATE TABLE "    
            if schema:    
                query += f"{self.escape_identifier(schema)}."
            query += f"{self.escape_identifier(table)}"

            if cascade:
                query += " CASCADE"

            self.execute_query(query, cursor=cursor)


    def erase_table(self, table: str|tuple = None, *, if_exists = False, cursor: T_Cursor = None):
        schema, table = self.split_name(table)

        if if_exists:
            if not self.table_exists((schema, table), cursor=cursor):
                return
        
        query = "DELETE FROM "          
        if schema:    
            query += f"{self.escape_identifier(schema)}."
        query += f"{self.escape_identifier(table)}"

        with nullcontext(cursor) if cursor else self.cursor(autoclose=False) as cursor:
            self.execute_query(query, cursor=cursor)
        

    def create_table(self, table: str|tuple, columns: list[str|Header], *, unique_together: list[tuple[str|Header]] = [], if_not_exists = False, cursor: T_Cursor = None):
        """
        Create a table from a list of columns.

        NOTE: This method does not intend to manage all cases, but only those usefull for zut library internals.
        """
        schema, table = self.split_name(table)
        
        columns = [Header(column) if not isinstance(column, Header) else column for column in columns]
        
        # Detect "unique together" columns by group
        unique_single: set[str] = set()
        unique_together_by_key: dict[str, list[str]] = {}

        for column in columns:
            if isinstance(column.unique, str):
                group = unique_together_by_key.get(column.unique)
                if group is None:
                    group = []
                    unique_together_by_key[column.unique] = group
                group.append(column.name)

        for key in list(unique_together_by_key):
            if len(unique_together_by_key[key]) == 1:
                unique_single.add(unique_together_by_key[key][0])
                del unique_together_by_key[key]

        for i, u in enumerate(unique_together):
            if len(u) == 1:
                unique_single.add(str(u[0]))
            else:
                key = f'__{i}'
                while key in unique_together_by_key:
                    key += '_'
                unique_together_by_key[key] = [str(column) for column in u]

        sql = "CREATE "
        if schema in {'pg_temp', 'temp'}:
            sql += "TEMPORARY "
        sql += "TABLE "
        if if_not_exists:
            sql += "IF NOT EXISTS "
        if schema:
            sql += f"{self.escape_identifier(schema)}."
        sql += f"{self.escape_identifier(table)}("


        all_columns: list[Header] = []
        primary_key_columns: list[Header] = []
        for column in columns:
            if not isinstance(column, Header):
                column = Header(column)
            
            all_columns.append(column)
            if column.primary_key:
                primary_key_columns.append(column)

        for i, column in enumerate(columns):
            if not isinstance(column, Header):
                column = Header(column)
            
            if i > 0:
                sql += ","
            
            sql_type = self._compute_sql_type(column)
            sql += f"{self.escape_identifier(column.name)} {sql_type} {'NOT NULL' if column.null is False or column.primary_key else 'NULL'}"            
            if column.primary_key:
                if not len(primary_key_columns) > 1:
                    sql += " PRIMARY KEY"
            elif column.unique is True or column.name in unique_single:
                sql += " UNIQUE"
            if column.identity:
                sql += f" {self.identity_definition_sql}"

        # Several primary keys ?
        if len(primary_key_columns) > 1:
            sql += ",PRIMARY KEY("
            for i, column in enumerate(primary_key_columns):
                sql += ("," if i > 0 else "") + f"{self.escape_identifier(column.name)}"
            sql += ")" # end PRIMARY KEY

        # Unique together ?
        for unique_columns in unique_together_by_key.values():
            sql += ",UNIQUE("
            for i, key in enumerate(unique_columns):
                sql += ("," if i > 0 else "") + f"{self.escape_identifier(key)}"
            sql += ")" # UNIQUE
        
        sql += ")" # end CREATE TABLE

        with nullcontext(cursor) if cursor else self.cursor(autoclose=False) as cursor:
            self.execute_query(sql, cursor=cursor)


    def add_table_columns(self, table: str|tuple, columns: list[str|Header], *, null = False, cursor: T_Cursor = None):
        """
        Add column(s) to a table.

        NOTE: This method does not intend to manage all cases, but only those usefull for zut library internals.
        """
        if len(columns) > 1 and not self.can_add_several_columns:
            for column in columns:
                self.add_table_columns(table, [column])
            return

        schema, table = self.split_name(table)
        
        sql = "ALTER TABLE "
        if schema:
            sql += f"{self.escape_identifier(schema)}."
        sql += f"{self.escape_identifier(table)}"

        for i, column in enumerate(columns):
            if not isinstance(column, Header):
                column = Header(column)

            if i == 0:
                sql += " ADD "
            else:
                sql += ","            
                
            sql_type = self._compute_sql_type(column)
            sql += f"{self.escape_identifier(column.name)} {sql_type} {'NOT NULL' if (column.null is False or column.primary_key) and not null else 'NULL'}"            
            if column.primary_key:
                raise ValueError(f"Cannot add a primary key column: {column.name}")
            elif column.unique:
                sql += " UNIQUE"
            if column.identity:
                sql += self.identity_definition_sql

        with nullcontext(cursor) if cursor else self.cursor(autoclose=False) as cursor:
            self.execute_query(sql, cursor=cursor)


    def duplicate_table_structure(self, src_table: str|tuple|None = None, dst_table: str|tuple = None, *, columns: list[str|Header]|None = None, key: str|list[str]|None = None, no_identity = False, no_constraints = False, cursor: T_Cursor = None) -> tuple[tuple[str,str], list[Header], list[str]]:
        src_schema, src_table = self.split_name(src_table)
        if dst_table is None:            
            dst_table = f"{self.temporary_prefix}{slugify(src_table, separator='_')[:40]}_tmp_{token_hex(4)}"
        dst_schema, dst_table = self.split_name(dst_table)

        keys: list[str] = []
        if key is not None:
            if isinstance(key, str):
                keys.append(key)
            else:
                for k in key:
                    if not isinstance(k, str):
                        raise TypeError(f"Invalid key: {k} (type {type(k).__name__})")
                    keys.append(k)

        target_columns = self.get_headers((src_schema, src_table), cursor=cursor)

        if columns:
            if isinstance(columns, str):
                columns = [columns]
            columns = [Header(column) if not isinstance(column, Header) else column for column in columns]
            for i, column in enumerate(columns):
                if column.name == '*':
                    for j, target_column in enumerate(target_columns):
                        if not any(c.name == target_column.name for c in columns):
                            if j == 0:
                                columns[i] = target_column
                            else:
                                columns.insert(i+j, target_column)
                    break
        else:
            columns = target_columns
        
        for i, column in enumerate(list(columns)):
            if column.primary_key:
                if key is None: # pk
                    keys.append(column.name)

            if no_identity and column.identity:
                if column.name in keys:
                    raise ValueError(f"Key column '{column.name}' is an identity column")
                del no_identity[i] # ignore identity columns
                
        missing_keys = [f'"{k}"' for k in keys if not any(c.name == k for c in columns)]
        if missing_keys:
            raise ValueError(f"Key{'s' if len(missing_keys) > 1 else ''}{', '.join(missing_keys)} not found in columns")
        
        if no_constraints:
            columns = [column.copy(no_constraints=True) for column in columns]
        
        self.create_table((dst_schema, dst_table), columns, unique_together=[keys], cursor=cursor)
        return (dst_schema, dst_table), columns, keys
    

    def drop_schema(self, schema: str = None, *, if_exists = False, cursor: T_Cursor = None):
        if self.default_schema is None:
            raise ValueError("This DbAdapter does not support schemas")
        
        if not schema:
            schema = self.schema or self.default_schema
            if not schema:
                raise ValueError("No schema defined for this db adapter")
        
        query = "DROP SCHEMA "
        if if_exists:
            query += "IF EXISTS "
        query += f"{self.escape_identifier(schema)}"
        
        with self.cursor(autoclose=False) as cursor:
            self.execute_query(query, cursor=cursor)
    

    def create_schema(self, schema: str = None, *, if_not_exists = False, cursor: T_Cursor = None):
        if self.default_schema is None:
            raise ValueError("This DbAdapter does not support schemas")

        if not schema:
            schema = self.schema or self.default_schema
            if not schema:
                raise ValueError("No schema defined for this db adapter")
        
        query = "CREATE SCHEMA "
        if if_not_exists:
            if self.scheme == 'sqlserver':
                if self.schema_exists(schema, cursor=cursor):
                    return
            else:
                query += "IF NOT EXISTS "
        query += f"{self.escape_identifier(schema)}"
        
        with self.cursor(autoclose=False) as cursor:
            self.execute_query(query, cursor=cursor)

    # endregion


    #region Convert    

    def convert_value(self, value: Any):
        """ Convert a value to types supported by the underlying connection adapter. """        
        if isinstance(value, (Enum,Flag)):
            return value.value
        elif isinstance(value, (datetime,time)):
            if value.tzinfo:
                if self.datetime_aware_sql_type:
                    return value
                elif self.tz:
                    value = make_naive(value, self.tz)
                else:
                    raise ValueError(f"Cannot store tz-aware datetimes with {type(self).__name__} without providing `tz` argument")
            
            # value is now naive
            datetime_naive_sql_type = self.datetime_naive_sql_type.lower()
            if 'text' in datetime_naive_sql_type or 'char' in datetime_naive_sql_type:
                return value.isoformat()
            elif datetime_naive_sql_type in {'real', 'float', 'double'}:
                return value.timestamp()
            elif datetime_naive_sql_type in {'integer', 'int', 'bigint'}:
                return int(value.timestamp())
            else:
                return value
        else:
            return value

    #endregion


    #region Migrate

    def migrate(self, dir: str|Path, *, cursor: T_Cursor = None, **file_kwargs):        
        with nullcontext(cursor) if cursor else self.cursor(autoclose=False) as cursor:
            last_name = self.get_last_migration_name(cursor=cursor)

            if last_name is None:
                sql_utils = ZUT_ROOT.joinpath("db", "sql", f"{self.scheme}.sql")
                if sql_utils.exists():
                    self._logger.info("Deploy SQL utils ...")
                    self.execute_file(sql_utils, cursor=cursor)

                self._logger.info("Create migration table ...")
                self.execute_query(f"CREATE TABLE migration(id {self.int_sql_type} NOT NULL PRIMARY KEY {self.identity_definition_sql}, name {self.str_key_sql_type} NOT NULL UNIQUE, deployed_utc {self.datetime_naive_sql_type} NOT NULL)", cursor=cursor)
                last_name = ''
            
            for path in sorted((dir if isinstance(dir, Path) else Path(dir)).glob('*.sql')):
                if path.stem == '' or path.stem.startswith('~') or path.stem.endswith('~'):
                    continue # skip
                if path.stem > last_name:
                    self._apply_migration(path, cursor=cursor, **file_kwargs)


    def _apply_migration(self, path: Path, *, cursor: T_Cursor = None, **file_kwargs):
        self._logger.info("Apply migration %s ...", path.stem)

        with nullcontext(cursor) if cursor else self.cursor(autoclose=False) as cursor:
            self.execute_file(path, cursor=cursor, **file_kwargs)
            self.execute_query(f"INSERT INTO migration (name, deployed_utc) VALUES({self.sql_placeholder}, {self.sql_placeholder})", [path.stem, self.convert_value(now_naive_utc())], cursor=cursor)


    def get_last_migration_name(self, *, cursor: T_Cursor = None) -> str|None:
        if not self.table_exists("migration", cursor=cursor):
            return None
        
        try:
            return self.get_scalar("SELECT name FROM migration ORDER BY name DESC", limit=1, cursor=cursor)
        except NotFoundError:
            return ''

    #endregion


    #region Dump

    def dumper(self,               
               # DB-specific options
               table: str|tuple = None, *,
               add_autoincrement_pk: bool|str = False,
               keep_connection: bool|None = None,
               batch: int|None = None,
               # Common TabularDumper options
               headers: Iterable[Header|Any]|None = None,
               truncate: bool = None,
               archivate: bool|str|Path|None = None,
               title: str|bool|None = None,
               dst_name: str|bool = True,
               dir: str|Path|Literal[False]|None = None,
               delay: bool = False,
               optional: str|Sequence[str]|Literal['*',True]|None = None,
               add_columns: bool|Literal['warn'] = False,
               after1970: bool|None = None,
               tz: tzinfo|str|bool|None = None,
               # Destination mask values
               **kwargs) -> TabularDumper:
        
        if tz is None:
            tz = self.tz

        extended_kwargs = {
                'headers': headers,
                'truncate': truncate,
                'archivate': archivate,
                'title': title,
                'dst_name': dst_name,
                'dir': dir,
                'delay': delay,
                'optional': optional,
                'add_columns': add_columns,
                'after1970': after1970,
                'tz': tz,
                **kwargs
            }

        return DbDumper(self,
                        table=table,
                        add_autoincrement_pk=add_autoincrement_pk,
                        keep_connection=keep_connection,
                        batch=batch,
                        **extended_kwargs)
    
    #endregion


def _get_connection_from_wrapper(db):    
    if type(db).__module__.startswith(('django.db.backends.', 'django.utils.connection')):
        return db.connection
    elif type(db).__module__.startswith(('psycopg_pool.pool',)):
        return db.connection()
    elif type(db).__module__.startswith(('psycopg2.pool',)):
        return db.getconn()
    else:
        return db


class DbResult(ColumnsProvider, Generic[T_Cursor]):
    def __init__(self, db: DbAdapter, cursor: T_Cursor, *, rows: list[tuple]|None, columns: list[str], query_id, tz: tzinfo|None):
        super().__init__()
        self._columns = columns
        self.db = db
        self.cursor = cursor
        self._query_id = query_id
        self._tz = tz
        self._formatted_rows: list[Row] = []
        self._input_rows = rows
        self._input_rows_iterator = None
        self._input_rows_iteration_stopped = False

    def __iter__(self):
        return self.Iterator(self)

    def _next_input_row(self):
        if self._input_rows_iterator is None:
            if self._input_rows is not None:
                self._input_rows_iterator = iter(self._input_rows)
            else:
                self._input_rows_iterator = iter(self.cursor)
        
        if self._input_rows_iteration_stopped:
            raise StopIteration()
    
        try:
            values = next(self._input_rows_iterator)
        except StopIteration:
            self._input_rows_iterator_stopped = True
            raise

        return values

    def _format_input_row(self, row):
        if self._tz:
            tz = self._tz if self._tz == 'localtime' else parse_tz(self._tz)
        else:
            tz = self.db.tz

        if tz:
            for i, value in enumerate(row):
                if isinstance(value, (datetime,time)):
                    if not is_aware(value):
                        row[i] = make_aware(value, tz)
        return row
    
    @property
    def rowcount(self):
        return self.cursor.rowcount
    
    @property
    def lastrowid(self):
        if self.db.scheme == 'postgresql':
            self.cursor.execute("SELECT lastval()")
            return next(iter(self.cursor))[0]
        elif self.db.scheme == 'sqlserver':
            self.cursor.execute("SELECT @@IDENTITY")
            return next(iter(self.cursor))[0]
        
        return self.cursor.lastrowid
    
    def single(self):
        iterator = iter(self)
        try:
            row = next(iterator)
        except StopIteration:
            if _with_django and self.db.use_http404:
                from django.http import Http404
                raise Http404()
            raise NotFoundError()

        try:
            next(iterator)
            raise SeveralFoundError()
        except StopIteration:
            pass

        return row
    
    def as_dicts(self):
        """
        Return results as a list of row dictionnaries.
        """
        return [row.as_dict() for row in self]
    
    def as_tab(self):
        self.to_dumper('tab')
    
    def to_dumper(self, dumper: TabularDumper|IOBase|str|Path, close=True, **kwargs):
        """
        Send results to the given tabular dumper.
        
        If dumper is `tab`, `csv`, a stream or a str/path, create the appropriate Tab/CSV/Excel dumper.
        
        Return a tuple containing the list of columns and the number of exported rows.
        """
        if isinstance(dumper, TabularDumper):
            if dumper.headers is not None:
                if [header.name for header in dumper.headers] != self.columns:
                    raise ValueError("Invalid headers in given dumper")
            else:
                dumper.headers = self.headers
        else:
            dumper = tabular_dumper(dumper, headers=self.headers, **kwargs)

        try:
            for row in self:
                dumper.append(row.values)        
            return self.columns, dumper.count
        finally:
            if close:
                dumper.close()
    
    class Iterator(Generic[T_Cursor]):
        def __init__(self, results: DbResult[T_Cursor]):
            self.results = results
            self.next_index = 0

        def __next__(self):
            if self.next_index < len(self.results._formatted_rows):
                formatted_row = self.results._formatted_rows[self.next_index]
            else:
                values = self.results._next_input_row()
                self.results._formatted_rows.append(values)
                self.results._format_input_row(values)
                formatted_row = Row(self.results, values, skip_convert=True) # ColumnProvider's headers are just columns without any parameter, so there is nothing to convert
            
            self.next_index += 1
            return formatted_row


class DbDumper(TabularDumper[DbAdapter]):
    """ 
    Line-per-line INSERT commands (to be used when `InsertSqlDumper` is not available).
    """
    def __init__(self, dst: DbAdapter, *,
                 table: str|tuple|None = None,
                 add_autoincrement_pk: bool|str = False,
                 keep_connection: bool|None = None,
                 batch: int|None = None,
                 **kwargs):
        
        if table:
            self._schema, self._table = dst.split_name(table)
        elif dst.table:
            self._schema, self._table = dst.schema, dst.table
        else:
            raise ValueError("Table name not provided")

        dst_name = kwargs.pop('dst_name', None)
        if not dst_name:
            dst_name = f"{self._schema + '.' if self._schema else ''}{self._table}"

        super().__init__(dst, dst_name=dst_name, **kwargs)

        self._add_autoincrement_pk = 'id' if add_autoincrement_pk is True else add_autoincrement_pk
        if keep_connection is None:
            keep_connection = False if dst.autocommit else True
        self._keep_connection = keep_connection
        self._insert_sql_headers: list[Header] = []
        self._insert_sql_single: str = None
        self._insert_sql_batch: str = None
        if self.dst.scheme == 'sqlite':
            self._max_params = 999
        elif self.dst.scheme == 'sqlserver':
            self._max_params = 2100
        else:
            self._max_params = 65535 # postgresql limit
        self.batch = batch

        self._connection = None
        self._cursor = None
        self._batch_rows = []
        self._executed_batch_count = 0

        self._insert_schema = self._schema
        self._insert_table = self._table

    @property
    def connection(self):
        if self._connection is None:
            if self._keep_connection:
                self._connection = self.dst.connection
            else:
                if self._logger.isEnabledFor(logging.DEBUG):
                    self._logger.debug(f"Create new DbDumber %s connection to %s", type(self).__name__, hide_url_password(self.dst._connection_url))
                self._connection = self.dst.create_connection(autocommit=False)
        return self._connection

    @property
    def cursor(self):
        if self._cursor is None:
            self._cursor = self.connection.cursor()
        return self._cursor

    def close(self, *final_queries):
        """
        Export remaining rows, execute optional final SQL queries, and then close the dumper.
        """
        super().close()

        self.flush(*final_queries)

        if self._cursor is not None:
            self._cursor.close()
            self._cursor = None
        
        if self._connection is not None:
            if self._keep_connection:
                if not self.dst.autocommit:
                    self._connection.commit()
            else:
                self._connection.commit()
                self._connection.close()
                self._connection = None

    def _build_insert_sqls(self, additional_headers: list[Header]):
        self._insert_sql_headers += additional_headers

        into_sql = f""
        if self._insert_schema:
            into_sql += f"{self.dst.escape_identifier(self._insert_schema)}."
        into_sql += self.dst.escape_identifier(self._insert_table)

        into_sql += "("
        values_sql = "("
        need_comma = False
        for header in self._insert_sql_headers:
            if need_comma:
                into_sql += ","
                values_sql += ","
            else:
                need_comma = True
            into_sql += f"{self.dst.escape_identifier(header.name)}"
            values_sql += self.dst.sql_placeholder
        into_sql += ")"
        values_sql += ")"

        max_batch = int(self._max_params / len(self._insert_sql_headers))
        if self.batch is None or max_batch < self.batch:
            self.batch = max_batch

        self._insert_sql_single = f"INSERT INTO {into_sql} VALUES {values_sql}"
        self._insert_sql_batch = f"INSERT INTO {into_sql} VALUES "
        for i in range(self.batch):
            self._insert_sql_batch += (',' if i > 0 else '') + values_sql

    def open(self) -> list[Header]|None:
        # Called at first exported row, before headers are analyzed.
        # Return list of existing headers if table exists, None if not.
        if self.dst.table_exists((self._schema, self._table), cursor=self.cursor):
            if self.truncate:
                self.dst.truncate_table((self._schema, self._table), cursor=self.cursor)
            
            headers = [header for header in self.dst.get_headers((self._schema, self._table), cursor=self.cursor) if not header.identity]
            self._build_insert_sqls(headers)
            return headers
        else:
            return None
    
    def export_headers(self, headers: list[Header]):
        # Called at first exported row, if there are no pre-existing headers (= table does not exist) => create table
        columns = [header for header in headers]
        
        if self._add_autoincrement_pk and not any(header.name == self._add_autoincrement_pk for header in headers):
            columns.insert(0, Header(name=self._add_autoincrement_pk, sql_type=self.dst.int_sql_type, primary_key=True, identity=True))

        self.dst.create_table((self._schema, self._table), columns, cursor=self.cursor)

        self._build_insert_sqls(headers)

    def new_headers(self, headers: list[Header]) -> bool|None:
        self.dst.add_table_columns((self._schema, self._table), headers, null=True, cursor=self.cursor)
        self._build_insert_sqls(headers)
        return True

    def _prepare_and_export_row(self, row: Iterable|dict):
        if not self.headers:
            raise ValueError(f"Cannot dump to db without headers")
        return super()._prepare_and_export_row(row)

    def _convert_value(self, value: Any, header: Header|None):
        value = super()._convert_value(value, header)
        value = self.dst.convert_value(value)
        return value

    def export(self, row: list):
        self._batch_rows.append(row)
        if len(self._batch_rows) >= self.batch:
            self._export_batch()

    def _export_batch(self):
        kwargs = {}
        if self.dst.scheme == 'postgresql':
            kwargs['prepare'] = True
            
        inlined_row = []
        while len(self._batch_rows) / self.batch >= 1:
            for row in self._batch_rows[:self.batch]:
                inlined_row += row
                
            if self._logger.isEnabledFor(logging.DEBUG):
                t0 = time_ns()
                if self._executed_batch_count == 0:
                    self._d_total = 0
            
            self.cursor.execute(self._insert_sql_batch, inlined_row, **kwargs)
            self._executed_batch_count += 1

            if self._logger.isEnabledFor(logging.DEBUG):
                t = time_ns()
                d = t - t0
                self._d_total += d
                self._logger.debug(f"Batch {self._executed_batch_count}: {self.batch:,} rows inserted in {d/1e6:,.1f} ms (avg: {self._d_total/1e3/(self._executed_batch_count * self.batch):,.1f} ms/krow, inst: {d/1e3/self.batch:,.1f} ms/krow)")
            
            self._batch_rows = self._batch_rows[self.batch:]

    def flush(self, *final_queries):
        """
        Export remaining rows, and then execute optional final SQL queries.
        """
        super().flush()

        kwargs = {}
        if self.dst.scheme == 'postgresql':
            kwargs['prepare'] = True
        
        self._export_batch()

        if self._batch_rows:
            if self._logger.isEnabledFor(logging.DEBUG):
                t0 = time_ns()

            for row in self._batch_rows:
                while len(row) < len(self._insert_sql_headers):
                    row.append(None)
                self.cursor.execute(self._insert_sql_single, row, **kwargs)
                
            if self._logger.isEnabledFor(logging.DEBUG):
                d = time_ns() - t0
                self._logger.debug(f"Remaining: {len(self._batch_rows):,} rows inserted one by one in {d/1e6:,.1f} ms ({d/1e3/(len(self._batch_rows)):,.1f} ms/krow)")

            self._batch_rows.clear()

        for final_query in final_queries:
            self.cursor.execute(final_query)
