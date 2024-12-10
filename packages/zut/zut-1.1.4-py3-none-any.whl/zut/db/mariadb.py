from __future__ import annotations

import logging
from urllib.parse import unquote, urlparse

from zut import Header
from zut.db.base import DbAdapter

try:
    from MySQLdb import connect
    from MySQLdb.connections import Connection
    from MySQLdb.cursors import Cursor

    class MariaDbAdapter(DbAdapter[Connection, Cursor]):
        """
        Database adapter for Microsoft SQL Server (using `pyodbc` driver).
        """
        scheme = 'mariadb'
        default_port = 3306
        default_schema = None
        identifier_quotechar = '`'
        identity_definition_sql = 'AUTO_INCREMENT'
        datetime_aware_sql_type = None
        datetime_naive_sql_type = 'datetime(6)'
        can_cascade_truncate = False
        temporary_prefix = 'temp.'

        @classmethod
        def is_available(cls):
            return True
        

        def create_connection(self, *, autocommit: bool, **kwargs) -> Connection:
            r = urlparse(self._connection_url)
            
            if r.hostname and not 'host' in kwargs:
                kwargs['host'] = unquote(r.hostname)
            if r.port and not 'port' in kwargs:
                kwargs['port'] = r.port
            
            path = r.path.lstrip('/')
            if path and not 'database' in kwargs:
                kwargs['database'] = unquote(path)

            if r.username and not 'user' in kwargs:
                kwargs['user'] = unquote(r.username)
            if r.password and not 'password' in kwargs:
                kwargs['password'] = unquote(r.password)
            
            return connect(**kwargs, sql_mode='STRICT_ALL_TABLES', autocommit=autocommit)

        @property
        def autocommit(self):
            if not self._connection:
                return self._autocommit
            else:
                return self._connection.get_autocommit()

        def table_exists(self, table: str|tuple = None, *, cursor = None) -> bool:        
            _, table = self.split_name(table)

            query = "SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = %s)"
            params = [table]

            return self.get_scalar(query, params, cursor=cursor) == 1


        def _get_table_headers(self, schema, table, cursor) -> list[Header]:
            sql = "SHOW COLUMNS FROM "
            if schema:
                sql += f"{self.escape_identifier(schema)}."
            sql += self.escape_identifier(table)

            details: list[Header] = []
            any_multi = False
            for data in self.get_dicts(sql, cursor=cursor):
                if data['Key'] == 'UNI':
                    unique = True
                elif data['Key'] == 'MUL':
                    any_multi = True
                    unique = ['?']
                else:
                    unique = False
                
                details.append(Header(name=data['Field'], sql_type=data['Type'], null=data['Null'] == 'YES', primary_key=data['Key'] == 'PRI', unique=unique, identity='auto' in data['Extra']))

            # Add unique details
            if any_multi and schema != 'temp':
                # ROADMAP/FIXME: does not work with temporary tables:
                # - They appear in information_schema.tables (at least for MariaDB, probably not for MySQL v8.0 according to https://dev.mysql.com/doc/mysql-infoschema-excerpt/8.0/en/information-schema-tables-table.html)
                # - Their constraints do NOT appear in information_schema.table_constraints
                sql = """
WITH table_info AS (
    SELECT
        table_schema
        ,table_name
    FROM information_schema.tables
    WHERE
        table_schema = CASE WHEN %(schema)s IS NULL THEN table_schema ELSE %(schema)s END
        AND table_name = %(table)s
)
,unique_constraints AS (
	SELECT
		k.table_schema
		,k.table_name
		,k.constraint_name
		,group_concat(s.column_name ORDER BY s.column_name) AS column_names
	FROM table_info t
    INNER JOIN information_schema.table_constraints k ON k.table_schema = t.table_schema AND k.table_name = t.table_name
	LEFT OUTER JOIN information_schema.statistics s ON s.table_schema = k.table_schema AND s.table_name = k.table_name AND s.index_name = k.constraint_name
	WHERE k.constraint_type = 'UNIQUE'
	GROUP BY
		k.table_schema
		,k.table_name
		,k.constraint_name
)
SELECT
	s.column_name
	,group_concat(uc.column_names SEPARATOR '|') AS unique_together
FROM table_info t
INNER JOIN information_schema.table_constraints k ON k.table_schema = t.table_schema AND k.table_name = t.table_name
LEFT OUTER JOIN information_schema.statistics s ON s.table_schema = k.table_schema AND s.table_name = k.table_name AND s.index_name = k.constraint_name
LEFT OUTER JOIN unique_constraints uc ON uc.table_schema = k.table_schema AND uc.table_name = k.table_name AND uc.constraint_name = k.constraint_name
WHERE k.constraint_type = 'UNIQUE'
GROUP BY
	s.column_name
"""
                for data in self.get_dicts(sql, {'schema': schema, 'table': table}, cursor=cursor):
                    detail = None
                    for d in details:
                        if d.name == data['column_name']:
                            detail = d
                            break
                    if detail is None:
                        raise ValueError(f"Column not found: {data['column_name']}")
                    detail.unique_together = data['unique_together']
                
            
            return details


except ImportError:  

    class MariaDbAdapter(DbAdapter):
        """
        Database adapter for Microsoft SQL Server (using `pyodbc` driver).
        """
                
        scheme = 'mariadb'

        @classmethod
        def is_available(cls):
            return False
