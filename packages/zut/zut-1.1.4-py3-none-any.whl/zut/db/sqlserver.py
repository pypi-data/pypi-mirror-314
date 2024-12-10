from __future__ import annotations

import logging
import re
from urllib.parse import unquote, urlparse

from zut import Header, build_url
from zut.db.base import DbAdapter


def sqlserver_parse_notice(nature: str, message: str) -> tuple[int, str]:
    m = re.match(r"^\[Microsoft\]\[[\w\d ]+\]\[SQL Server\](.+)$", message)
    if m:
        message = m[1]

    if nature == '[01000] (0)':
        nature = 'PRINT'
    elif nature == '[01000] (50000)':
        nature = 'RAISERROR'
    elif nature == '[01003] (8153)': # Avertissement : la valeur NULL est éliminée par un agrégat ou par une autre opération SET
        return logging.INFO, message
    
    m = re.match(r'^\[?(?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL)\s?[\]\:](?P<message>.+)$', message, re.DOTALL|re.IGNORECASE)
    if m:
        return getattr(logging, m['level']), m['message'].lstrip()
    
    if nature == 'PRINT':
        return logging.INFO, message
    else:
        return logging.WARNING, message
   

try:
    from pyodbc import Connection, Cursor, connect, drivers

    class SqlServerAdapter(DbAdapter[Connection, Cursor]):
        """
        Database adapter for Microsoft SQL Server (using `pyodbc` driver).
        """
        scheme = 'sqlserver' # or sqlservers (if encrypted)
        default_port = 1433
        default_schema = 'dbo'
        sql_placeholder = '?'
        sql_named_placeholder = ':%s'
        only_positional_params = True
        split_multi_statement_files = True
        identity_definition_sql = 'IDENTITY'
        datetime_aware_sql_type = None
        datetime_naive_sql_type = 'datetime'
        procedure_caller = 'EXEC'
        procedure_params_parenthesis = False
        can_cascade_truncate = False
        can_add_several_columns = True
        function_requires_schema = True
        temporary_prefix = '#'

        @classmethod
        def is_available(cls):
            return True
        

        def create_connection(self, *, autocommit: bool|None, **kwargs) -> Connection:
            def escape(s):
                if ';' in s or '{' in s or '}' in s or '=' in s:
                    return "{" + s.replace('}', '}}') + "}"
                else:
                    return s
                
            r = urlparse(self._connection_url)
            
            server = unquote(r.hostname) or '(local)'
            if r.port:
                server += f',{r.port}'

            # Use "ODBC Driver XX for SQL Server" if available ("SQL Server" seems not to work with LocalDB, and takes several seconds to establish connection on my standard Windows machine with SQL Server Developer).
            driver = "SQL Server"
            for a_driver in sorted(drivers(), reverse=True):
                if re.match(r'^ODBC Driver \d+ for SQL Server$', a_driver):
                    driver = a_driver
                    break

            connection_string = 'Driver={%s};Server=%s;Database=%s;' % (escape(driver), escape(server), escape(r.path.lstrip('/')))

            if r.username:
                connection_string += 'UID=%s;' % escape(unquote(r.username))
                if r.password:
                    connection_string += 'PWD=%s;' % escape(unquote(r.password))
            else:
                connection_string += 'Trusted_Connection=yes;'
                
            connection_string += f"Encrypt={'yes' if r.scheme in {'mssqls', 'sqlservers'} else 'no'};"
            return connect(connection_string, autocommit=autocommit, **kwargs)


        def _get_url_from_connection(self):
            with self.cursor(autoclose=False) as cursor:
                cursor.execute("SELECT @@SERVERNAME, local_tcp_port, SUSER_NAME(), DB_NAME() FROM sys.dm_exec_connections WHERE session_id = @@spid")
                host, port, user, dbname = next(iter(cursor))
            return build_url(scheme=self.scheme, username=user, hostname=host, port=port, path='/'+dbname)
    

        def _paginate_parsed_query(self, selectpart: str, orderpart: str, *, limit: int|None, offset: int|None) -> str:
            if orderpart:
                result = f"{selectpart} {orderpart} OFFSET {offset or 0} ROWS"
                if limit is not None:
                    result += f" FETCH NEXT {limit} ROWS ONLY"
                return result
            elif limit is not None:
                if offset is not None:
                    raise ValueError("an ORDER BY clause is required for OFFSET")
                return f"SELECT TOP {limit} * FROM ({selectpart}) s"
            else:
                return selectpart
            

        def escape_identifier(self, value: str):
            if not isinstance(value, str):
                raise TypeError(f"Invalid identifier: {value} (type: {type(value)})")
            return f"[{value.replace(']', ']]')}]"


        def _log_cursor_notices(self, cursor: Cursor):
            if cursor.messages:                        
                for nature, message in cursor.messages:
                    level, message = sqlserver_parse_notice(nature, message)
                    self._logger.log(level, message)


        def _traverse_cursor(self, cursor: Cursor, *, warn: bool, query_id):
            columns = []
            rows = []
            set_num = 1

            while True:
                if cursor.description:
                    columns = [info[0] for info in cursor.description]

                    if warn:
                        set_id = f'{query_id} (set {set_num})' if query_id is not None else f'(set {set_num})'
                        self._warn_if_rows(cursor, columns=columns, query_id=set_id)
                        rows = [] # indicates to QueryResults to not report rows that we just warned about

                    else:
                        rows = [row for row in iter(cursor)]

                else:
                    columns = []
                    rows = []

                if not cursor.nextset():
                    break

                set_num += 1
                self._log_cursor_notices(cursor)

            # Return rows and columns from the last result set
            return rows, columns


        def table_exists(self, table: str|tuple = None, *, cursor = None) -> bool:
            schema, table = self.split_name(table)

            sql = "SELECT CASE WHEN EXISTS(SELECT 1 FROM information_schema.tables WHERE table_schema = ? AND table_name = ?) THEN 1 ELSE 0 END"
            params = [schema or self.default_schema, table]

            return self.get_scalar(sql, params, cursor=cursor) == 1
        
        
        def schema_exists(self, schema: str = None, *, cursor = None) -> bool:
            if not schema:
                schema = self.schema or self.default_schema

            query = "SELECT CASE WHEN EXISTS(SELECT 1 FROM information_schema.schemata WHERE schema_name = ?) THEN 1 ELSE 0 END"
            return self.get_scalar(query, [schema], cursor=cursor) == 1


        def _get_table_headers(self, schema, table, cursor) -> list[Header]:
            if table.startswith('#'):
                table = self.get_scalar("(SELECT name FROM tempdb.sys.objects WHERE object_id = OBJECT_ID('tempdb.dbo.' + ?))", [table], cursor=cursor)
                syschema_prefix = 'tempdb.'
            else:
                syschema_prefix = ''

            sql = f"""
WITH pk_columns AS (
    SELECT c.column_name
    FROM {syschema_prefix}information_schema.table_constraints k 
    LEFT OUTER JOIN {syschema_prefix}information_schema.constraint_column_usage u ON u.table_name = k.table_name AND u.constraint_catalog = k.constraint_catalog AND u.constraint_schema = k.constraint_schema AND u.constraint_name = k.constraint_name
    LEFT OUTER JOIN {syschema_prefix}information_schema.columns c ON c.table_schema = k.constraint_schema AND c.table_name = u.table_name AND c.column_name = u.column_name
    WHERE k.constraint_type = 'PRIMARY KEY' AND k.constraint_schema = :schema AND k.table_name = :table
)
,identity_columns AS (
	SELECT c.name AS column_name
	FROM {syschema_prefix}sys.tables t
	INNER JOIN {syschema_prefix}sys.schemas s ON s.schema_id = t.schema_id
	INNER JOIN {syschema_prefix}sys.columns c ON c.object_id = t.object_id
	INNER JOIN {syschema_prefix}sys.types ty ON ty.system_type_id = c.system_type_id
	WHERE c.is_identity = 1 AND s.name = :schema AND t.name = :table
)
,unique_constraints AS (
    SELECT
		k.constraint_catalog
		,k.constraint_schema
	    ,k.table_name
    	,k.constraint_name
    	,string_agg(u.column_name, ',') WITHIN GROUP (ORDER BY u.column_name) AS column_names
    FROM {syschema_prefix}information_schema.table_constraints k 
    LEFT OUTER JOIN {syschema_prefix}information_schema.constraint_column_usage u ON u.table_name = k.table_name AND u.constraint_catalog = k.constraint_catalog AND u.constraint_schema = k.constraint_schema AND u.constraint_name = k.constraint_name
    WHERE k.constraint_type = 'UNIQUE' AND k.constraint_schema = :schema AND k.table_name = :table
    GROUP BY
		k.constraint_catalog
		,k.constraint_schema
	    ,k.table_name
    	,k.constraint_name
)
,unique_columns AS (
    SELECT
    	u.column_name
    	,string_agg(uc.column_names, '|') WITHIN GROUP (ORDER BY uc.column_names) AS unique_together
    FROM {syschema_prefix}information_schema.table_constraints k 
    LEFT OUTER JOIN {syschema_prefix}information_schema.constraint_column_usage u ON u.table_name = k.table_name AND u.constraint_catalog = k.constraint_catalog AND u.constraint_schema = k.constraint_schema AND u.constraint_name = k.constraint_name
    LEFT OUTER JOIN unique_constraints uc ON uc.constraint_catalog = k.constraint_catalog AND uc.constraint_schema = k.constraint_schema AND uc.table_name = k.table_name AND uc.constraint_name = k.constraint_name
    WHERE k.constraint_type = 'UNIQUE' AND k.constraint_schema = :schema AND k.table_name = :table
    GROUP BY
    	u.column_name
)
SELECT
    c.column_name AS name
    ,c.data_type + CASE 
	    WHEN c.character_maximum_length = -1 THEN '(max)'
	    WHEN c.character_maximum_length IS NOT NULL AND c.data_type IN ('text', 'ntext') THEN ''
	    WHEN c.character_maximum_length IS NOT NULL THEN concat('(',c.character_maximum_length,')')
	    WHEN c.numeric_precision IS NOT NULL AND c.data_type NOT IN ('bigint', 'int', 'smallint', 'tinyint', 'real', 'float') THEN concat('(',c.numeric_precision,CASE WHEN c.numeric_scale IS NOT NULL THEN concat(',', c.numeric_scale) ELSE '' END,')')
	    WHEN c.datetime_precision IS NOT NULL AND c.data_type != 'datetime' THEN concat('(',c.datetime_precision,')')
    	ELSE ''
    END + CASE WHEN c.collation_name IS NOT NULL THEN concat(' COLLATE ', c.collation_name) ELSE '' END AS sql_type
    ,CAST(CASE WHEN c.is_nullable = 'YES' THEN 1 ELSE 0 END AS bit) AS "null"
    ,CAST(CASE WHEN p.column_name IS NOT NULL THEN 1 ELSE 0 END AS bit) AS primary_key
    ,u.unique_together
    ,CAST(CASE WHEN i.column_name IS NOT NULL THEN 1 ELSE 0 END AS bit) AS "identity"
FROM {syschema_prefix}information_schema.columns c
LEFT OUTER JOIN pk_columns p ON p.column_name = c.column_name
LEFT OUTER JOIN identity_columns i ON i.column_name = c.column_name
LEFT OUTER JOIN unique_columns u ON u.column_name = c.column_name
WHERE c.table_schema = :schema AND c.table_name = :table
ORDER BY c.ordinal_position
"""
            
            return self.get_dicts(sql, {'schema': schema or self.default_schema, 'table': table}, cursor=cursor)


except ImportError:

    class SqlServerAdapter(DbAdapter):
        """
        Database adapter for Microsoft SQL Server (using `pyodbc` driver).
        """
                
        scheme = 'sqlserver' # or sqlservers (if encrypted)
        default_port = 1433
        default_schema = 'dbo'
        sql_placeholder = '?'
        sql_named_placeholder = ':%s'
        only_positional_params = True

        @classmethod
        def is_available(cls):
            return False
