"""
Common operations on databases.
"""
from __future__ import annotations

from urllib.parse import urlparse

from zut.db.base import DbAdapter, DbResult, DbDumper, _get_connection_from_wrapper
from zut.db.sqlserver import SqlServerAdapter
from zut.db.mariadb import MariaDbAdapter
from zut.db.postgresql import PostgreSqlAdapter
from zut.db.postgresqlold import PostgreSqlOldAdapter
from zut.db.sqlite import SqliteAdapter


def get_db_adapter(origin, *, autocommit=True) -> DbAdapter:
    """
    Create a new adapter (if origin is not already one).
    - `autocommit`: commit transactions automatically (applies only for connections created by the adapter).
    """
    if isinstance(origin, str):
        adapter = get_db_adapter_from_url(origin, autocommit=autocommit)
        if adapter is None:
            raise ValueError(f"Invalid db url: {origin}")
        return adapter
    
    elif isinstance(origin, dict) and 'ENGINE' in origin: # Django
        engine = origin['ENGINE']
        if engine in {"django.db.backends.postgresql", "django.contrib.gis.db.backends.postgis"}:
            if PostgreSqlAdapter.is_available():
                return PostgreSqlAdapter(origin, autocommit=autocommit)
            elif PostgreSqlOldAdapter.is_available():
                return PostgreSqlOldAdapter(origin, autocommit=autocommit)
            else:
                raise ValueError(f"PostgreSqlAdapter and PostgreSqlOldAdapter not available (psycopg missing)")
        elif engine in {"django.db.backends.mysql", "django.contrib.gis.db.backends.mysql"}:
            return MariaDbAdapter(origin, autocommit=autocommit)
        elif engine in {"django.db.backends.sqlite3", "django.db.backends.spatialite"}:
            return SqliteAdapter(origin, autocommit=autocommit)
        elif engine in {"mssql"}:
            return SqlServerAdapter(origin, autocommit=autocommit)
        else:
            raise ValueError(f"Invalid db: unsupported django db engine: {engine}")
        
    elif isinstance(origin, DbAdapter):
        return origin
    
    else:
        adapter = get_db_adapter_from_connection(origin)
        if adapter is None:
            raise ValueError(f"Invalid db: unsupported origin type: {type(origin)}")
        return adapter


def get_db_adapter_from_url(url: str, *, autocommit=True) -> DbAdapter|None:
    if not isinstance(url, str):
        return None

    r = urlparse(url)
    if r.scheme in {'postgresql', 'postgres', 'pg'}:
        if PostgreSqlAdapter.is_available():
            adapter_cls = PostgreSqlAdapter
        elif PostgreSqlOldAdapter.is_available():
            adapter_cls = PostgreSqlOldAdapter
        else:
            raise ValueError(f"PostgreSqlAdapter and PostgreSqlOldAdapter not available (psycopg missing)")
    elif r.scheme in {'mariadb', 'mysql'}:
        adapter_cls = MariaDbAdapter
    elif r.scheme in {'sqlite', 'sqlite3'}:
        adapter_cls = SqliteAdapter
    elif r.scheme in {'sqlserver', 'sqlservers', 'mssql', 'mssqls'}:
        adapter_cls = SqlServerAdapter
    else:
        return None
    
    if not adapter_cls.is_available():
        raise ValueError(f"Cannot use db {r.scheme} ({adapter_cls.__name__} not available)")
    
    return adapter_cls(r, autocommit=autocommit)


def get_db_adapter_from_connection(connection) -> DbAdapter|None:
    # NOTE: autocommit is already configured for the connection
    connection = _get_connection_from_wrapper(connection)

    type_fullname: str = type(connection).__module__ + '.' + type(connection).__qualname__
    if type_fullname == 'psycopg2.extension.connection':
        adapter_cls = PostgreSqlOldAdapter
    elif type_fullname == 'psycopg.Connection':
        adapter_cls = PostgreSqlAdapter
    elif type_fullname == 'MySQLdb.connections.Connection':
        adapter_cls = MariaDbAdapter
    elif type_fullname == 'sqlite3.Connection':
        adapter_cls = MariaDbAdapter
    elif type_fullname == 'pyodbc.Connection':
        adapter_cls = SqlServerAdapter
    else:
        return None
    
    if not adapter_cls.is_available():
        raise ValueError(f"Cannot use db ({adapter_cls.__name__} not available)")
    
    return adapter_cls(connection)


__all__ = (
    'DbAdapter', 'DbResult', 'DbDumper', 'PostgreSqlAdapter', 'PostgreSqlOldAdapter', 'MariaDbAdapter', 'SqliteAdapter', 'SqlServerAdapter',
    'get_db_adapter', 'get_db_adapter_from_url', 'get_db_adapter_from_connection',
)
