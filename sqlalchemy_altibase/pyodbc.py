# altibase/pyodbc.py
# Copyright (C) 2005-2020 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

"""
.. dialect:: altibase+pyodbc
    :name: PyODBC
    :dbapi: pyodbc
    :connectstring: altibase+pyodbc://<username>:<password>@<dsnname>?server=<server> & port=<port> & database=<database_name>
    :url: http://pypi.python.org/pypi/pyodbc/

Unicode Support
---------------

The pyodbc driver currently supports usage of these Altibase types with
Unicode or multibyte strings::

    CHAR
    NCHAR
    NVARCHAR
    TEXT
    VARCHAR

Currently *not* supported are::

    UNICHAR
    UNITEXT
    UNIVARCHAR

"""  # noqa

import decimal

import odbcinst
import pyodbc
from sqlalchemy import types as sqltypes, util
from sqlalchemy.connectors.pyodbc import PyODBCConnector
from sqlalchemy.exc import DBAPIError

from .base import AltibaseDialect, AltibaseExecutionContext


def get_odbc_info(engine):
    """retrieve ODBC configuration information for troubleshooting purposes"""
    info = odbcinst.j()
    try:
        cnxn = engine.raw_connection()
        info["SQL_DRIVER_NAME"] = cnxn.getinfo(pyodbc.SQL_DRIVER_NAME)
        info["SQL_DRIVER_VER"] = cnxn.getinfo(pyodbc.SQL_DRIVER_VER)
        info["SQL_DBMS_VER"] = cnxn.getinfo(pyodbc.SQL_DBMS_VER)
    except DBAPIError:
        pass
    return info


class _SybNumeric_pyodbc(sqltypes.Numeric):
    """Turns Decimals with adjusted() < -6 into floats.

    It's not yet known how to get decimals with many
    significant digits or very large adjusted() into Altibase
    via pyodbc.

    """

    def bind_processor(self, dialect):
        super_process = super(_SybNumeric_pyodbc, self).bind_processor(dialect)

        def process(value):
            if self.asdecimal and isinstance(value, decimal.Decimal):
                if value.adjusted() < -6:
                    return float(value)

            if super_process:
                return super_process(value)
            else:
                return value

        return process


class AltibaseExecutionContext_pyodbc(AltibaseExecutionContext):
    def set_ddl_autocommit(self, connection, value):
        if value:
            connection.autocommit = True
        else:
            connection.autocommit = False


class AltibaseDialect_pyodbc(PyODBCConnector, AltibaseDialect):
    execution_ctx_cls = AltibaseExecutionContext_pyodbc

    supports_statement_cache = True  # for SQLA 1.4.5+

    colspecs = {sqltypes.Numeric: _SybNumeric_pyodbc}

    def __init__(self, fast_executemany=False, **params):
        super(AltibaseDialect_pyodbc, self).__init__(**params)
        self.fast_executemany = fast_executemany

    @classmethod
    def import_dbapi(cls):
        import pyodbc as module

        return module

    def on_connect(self):
        super_ = super(AltibaseDialect_pyodbc, self).on_connect()

        def on_connect(conn):
            if super_ is not None:
                super_(conn)

        return on_connect

    def do_executemany(self, cursor, statement, parameters, context=None):
        if self.fast_executemany:
            cursor.fast_executemany = True
        super(AltibaseDialect_pyodbc, self).do_executemany(cursor, statement, parameters, context=context)

    def create_connect_args(self, url):
        opts = url.translate_connect_args(username="user")
        opts.update(url.query)

        keys = opts
        query = url.query

        connect_args = {}
        for param in ("ansi", "unicode_results", "autocommit"):
            if param in keys:
                connect_args[param] = util.asbool(keys.pop(param))

        if "odbc_connect" in keys:
            connectors = [util.unquote_plus(keys.pop("odbc_connect"))]
        else:

            def check_quote(token):
                if ";" in str(token) or str(token).startswith("{"):
                    token = "{%s}" % token.replace("}", "}}")
                return token

            keys = dict((k, check_quote(v)) for k, v in keys.items())

            dsn_connection = "dsn" in keys or ("host" in keys and "database" not in keys)
            if dsn_connection:
                connectors = ["dsn=%s" % (keys.pop("host", "") or keys.pop("dsn", ""))]
            else:
                port = ""
                if "port" in keys and "port" not in query:
                    port = "%d" % int(keys.pop("port"))

                connectors = []
                driver = keys.pop("driver", self.pyodbc_driver_name)
                if driver is None and keys:
                    # note if keys is empty, this is a totally blank URL
                    util.warn(
                        "No driver name specified; " "this is expected by PyODBC when using " "DSN-less connections"
                    )
                else:
                    connectors.append("DRIVER=%s" % driver)

                user = keys.pop("user", None)
                if user:
                    connectors.append("User=%s" % user)
                    pwd = keys.pop("password", "")
                    if pwd:
                        connectors.append("Password=%s" % pwd)

                connectors.extend(["Server=%s" % keys.pop("host", ""), "PORT=%s" % port])

            connectors.extend(["%s=%s" % (k, v) for k, v in keys.items()])

        return [[";".join(connectors)], connect_args]


dialect = AltibaseDialect_pyodbc
