from sqlalchemy.dialects import registry as _registry
from sqlalchemy.dialects.oracle.base import BINARY_DOUBLE, BINARY_FLOAT, NUMBER

from . import base  # noqa
from . import pyodbc  # noqa
from .base import (
    BIGINT,
    BIT,
    BLOB,
    BYTE,
    CHAR,
    CLOB,
    DATE,
    DECIMAL,
    FLOAT,
    GEOMETRY,
    INTEGER,
    NCHAR,
    NIBBLE,
    SMALLINT,
    VARBIT,
    VARCHAR,
)

# default (and only) dialect
base.dialect = dialect = pyodbc.dialect

_registry.register("altibase.pyodbc", "sqlalchemy_altibase.pyodbc", "AltibaseDialect_pyodbc")

__all__ = (
    "CHAR",
    "VARCHAR",
    "NCHAR",
    "CLOB",
    "BLOB",
    "NUMBER",
    "FLOAT",
    "BINARY_DOUBLE",
    "BINARY_FLOAT",
    "DECIMAL",
    "BIGINT",
    "INTEGER",
    "SMALLINT",
    "DATE",
    "BYTE",
    "NIBBLE",
    "BIT",
    "VARBIT",
    "GEOMETRY",
)
