from __future__ import annotations

import logging
import re
from typing import Any
from urllib.parse import ParseResult

from zut import Header, build_url
from zut.db.base import DbAdapter, T_Connection, T_Cursor


def postgresql_notice_handler(diag: Diagnostic, logger: logging.Logger = None):
    """
    Handler required by psycopg 3 `connection.add_notice_handler()`.
    """
    # determine level
    level, message = postgresql_parse_notice(diag.severity_nonlocalized, diag.message_primary)
    
    # determine logger by parsing context
    if not logger:
        name = f'{PostgreSqlAdapter.__module__}.{PostgreSqlAdapter.__qualname__}'
        m = re.match(r"^fonction [^\s]+ (\w+)", diag.context or '')
        if m:
            name += f":{m[1]}"
        logger = logging.getLogger(name)

    # write log
    logger.log(level, message)


def postgresql_parse_notice(severity: str, message: str) -> tuple[int, str]:
    m = re.match(r'^\[?(?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL)[\]\:](?P<message>.+)$', message, re.DOTALL)
    if m:
        return getattr(logging, m['level']), m['message'].lstrip()

    if severity.startswith('DEBUG'): # not sent to client (by default)
        return logging.DEBUG, message
    elif severity == 'LOG': # not sent to client (by default), written on server log (LOG > ERROR for log_min_messages)
        return logging.DEBUG, message
    elif severity == 'NOTICE': # sent to client (by default) [=client_min_messages]
        return logging.DEBUG, message
    elif severity == 'INFO': # always sent to client
        return logging.INFO, message
    elif severity == 'WARNING': # sent to client (by default) [=log_min_messages]
        return logging.WARNING, message
    elif severity in ['ERROR', 'FATAL']: # sent to client
        return logging.ERROR, message
    elif severity in 'PANIC': # sent to client
        return logging.CRITICAL, message
    else:
        return logging.WARNING, message


class BasePostgreSqlAdapter(DbAdapter[T_Connection, T_Cursor]):
    """
    Base class for PostgreSql database adapters (:class:`PostgreSqlAdapter` using `psycopg` (v3) driver or :class:`PostgreSqlOldAdapter` using `psycopg2` driver).
    """
    scheme = 'postgresql'
    default_port = 5432
    _sql: Any

    def _verify_scheme(self, r: ParseResult) -> ParseResult|None:
        # See: https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING
        if r.scheme == 'postgresql':
            return r
        elif r.scheme in {'pg', 'postgres'}:
            return r._replace(scheme='postgresql')
        else:
            return None


    def create_connection(self, *, autocommit: bool, **kwargs):
        return connect(self._connection_url, autocommit=autocommit, **kwargs)
    
    
    def _get_url_from_connection(self):
        with self.cursor(autoclose=False) as cursor:
            cursor.execute("SELECT session_user, inet_server_addr(), inet_server_port(), current_database()")
            user, host, port, dbname = next(iter(cursor))
        return build_url(scheme=self.scheme, username=user, hostname=host, port=port, path='/'+dbname)


    def _get_composable_param(self, value):
        if value is None:
            return self._sql.SQL("null")
        elif value == '__now__':
            return self._sql.SQL("NOW()")
        elif isinstance(value, self._sql.Composable):
            return value
        else:
            return self._sql.Literal(value)
    

    def table_exists(self, table: str|tuple = None, *, cursor = None) -> bool:
        schema, table = self.split_name(table)

        query = "SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname = %s AND tablename = %s)"
        return self.get_scalar(query, [schema or self.default_schema, table], cursor=cursor)
    
    
    def schema_exists(self, schema: str = None, *, cursor: T_Cursor = None) -> bool:
        if not schema:
            schema = self.schema or self.default_schema

        query = "SELECT EXISTS (SELECT FROM pg_namespace WHERE nspname = %s)"
        return self.get_scalar(query, [schema], cursor=cursor)


    def _get_table_headers(self, schema, table, cursor) -> list[Header]:
        sql = """
WITH table_info AS (
    SELECT
        table_schema
        ,table_name
    FROM information_schema.tables
    WHERE
        table_schema = CASE WHEN %(schema)s = 'pg_temp' THEN table_schema ELSE %(schema)s END
        AND table_type = CASE WHEN %(schema)s = 'pg_temp' THEN 'LOCAL TEMPORARY' ELSE table_type END
        AND table_name = %(table)s
)
,pk_columns AS (
    SELECT c.column_name
    FROM table_info t
    INNER JOIN information_schema.table_constraints k ON k.constraint_schema = t.table_schema AND k.table_name = t.table_name
    INNER JOIN information_schema.constraint_column_usage u ON u.table_name = k.table_name AND u.constraint_catalog = k.constraint_catalog AND u.constraint_schema = k.constraint_schema AND u.constraint_name = k.constraint_name
    INNER JOIN information_schema.columns c ON c.table_schema = k.constraint_schema AND c.table_name = u.table_name AND c.column_name = u.column_name
    WHERE k.constraint_type = 'PRIMARY KEY'
)
,unique_constraints AS (
    SELECT
        k.constraint_schema
        ,k.constraint_name
        ,string_agg(c.column_name, ',' order by c.column_name) AS column_names
    FROM table_info t
    INNER JOIN information_schema.table_constraints k ON k.constraint_schema = t.table_schema AND k.table_name = t.table_name
    INNER JOIN information_schema.constraint_column_usage u ON u.table_name = k.table_name AND u.constraint_catalog = k.constraint_catalog AND u.constraint_schema = k.constraint_schema AND u.constraint_name = k.constraint_name
    INNER JOIN information_schema.columns c ON c.table_schema = k.constraint_schema AND c.table_name = u.table_name AND c.column_name = u.column_name
    WHERE k.constraint_type = 'UNIQUE'
    GROUP BY
        k.constraint_schema
        ,k.constraint_name
)
,unique_columns AS (
    SELECT
        column_name
        ,string_agg(column_names, '|') AS unique_together
    FROM (
        SELECT
            u.column_name
            ,uc.column_names
        FROM table_info t
        INNER JOIN information_schema.table_constraints k ON k.constraint_schema = t.table_schema AND k.table_name = t.table_name
        INNER JOIN information_schema.constraint_column_usage u ON u.table_name = k.table_name AND u.constraint_catalog = k.constraint_catalog AND u.constraint_schema = k.constraint_schema AND u.constraint_name = k.constraint_name
        INNER JOIN unique_constraints uc ON uc.constraint_schema = k.constraint_schema AND uc.constraint_name = k.constraint_name
        WHERE k.constraint_type = 'UNIQUE'
    ) s
    GROUP BY
        column_name
)
SELECT
    c.column_name AS name
    ,c.udt_name || CASE
		WHEN c.character_maximum_length IS NOT NULL THEN '('||c.character_maximum_length||')'
		ELSE ''
	END AS sql_type
    ,c.is_nullable = 'YES' AS "null"
    ,p.column_name IS NOT NULL AS primary_key
    ,u.unique_together
    ,c.is_identity = 'YES' AS "identity"
FROM table_info t
INNER JOIN information_schema.columns c ON c.table_schema = t.table_schema AND c.table_name = t.table_name
LEFT OUTER JOIN pk_columns p ON p.column_name = c.column_name
LEFT OUTER JOIN unique_columns u ON u.column_name = c.column_name
ORDER BY c.ordinal_position
"""

        return self.get_dicts(sql, {'schema': schema or self.default_schema, 'table': table}, cursor=cursor)
    
    
try:
    from psycopg import Connection, Cursor, connect, sql
    from psycopg.errors import Diagnostic


    class PostgreSqlAdapter(BasePostgreSqlAdapter[Connection, Cursor]):
        """
        Database adapter for PostgreSQL (using `psycopg` (v3) driver).
        """
        _sql = sql

        @classmethod
        def is_available(cls):
            return True
        
        def _register_notice_handler(self, cursor, query_id = None):
            if query_id is not None:
                logger = logging.getLogger(self._logger.name + f':{query_id}')
            else:
                logger = self._logger
            
            return PostgreSqlNoticeManager(cursor.connection, logger)


    class PostgreSqlNoticeManager:
        """
        This class can be used as a context manager that remove the handler on exit.

        The actual handler required by psycopg 3 `connection.add_notice_handler()` is the `postgresql_notice_handler` method.
        """
        def __init__(self, connection: Connection, logger: logging):
            self.connection = connection
            self.logger = logger
            for handler in list(self.connection._notice_handlers):
                self.connection._notice_handlers.remove(handler)
            self.connection.add_notice_handler(self.handler)

        def __enter__(self):
            return self.handler
        
        def __exit__(self, exc_type = None, exc_value = None, exc_traceback = None):
            self.connection._notice_handlers.remove(self.handler)

        def handler(self, diag: Diagnostic):
            return postgresql_notice_handler(diag, logger=self.logger)


except ImportError:

    class PostgreSqlAdapter(BasePostgreSqlAdapter):
        """
        Database adapter for PostgreSQL (using `psycopg` (v3) driver).
        """

        @classmethod
        def is_available(cls):
            return False
