# altibase/base.py
# Copyright (C) 2010-2020 the SQLAlchemy authors and contributors
# <see AUTHORS file>
# get_select_precolumns(), limit_clause() implementation
# copyright (C) 2007 Fisch Asset Management
# AG http://www.fam.ch, with coding by Alexander Houben
# alexander.houben@thor-solutions.ch
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

"""

.. dialect:: altibase
    :name: Altibase
"""
from sqlalchemy.dialects.oracle import base as oracle_base
from sqlalchemy.engine import default, reflection
from sqlalchemy.sql import sqltypes, text
from sqlalchemy.types import (
    BIGINT,
    BLOB,
    CHAR,
    CLOB,
    DATE,
    DECIMAL,
    FLOAT,
    INTEGER,
    NCHAR,
    SMALLINT,
    VARCHAR,
)
from sqlalchemy.util import py2k, warn

RESERVED_WORDS = set(
    [
        "_PROWID",
        "FIFO",
        "PRIMARY",
        "ACCESS",
        "FIXED",
        "PRIOR",
        "ADD",
        "FLASHBACK",
        "PROCEDURE",
        "AFTER",
        "FLUSH",
        "PURGE",
        "AGER",
        "FLUSHER",
        "QUEUE",
        "ALL",
        "FOLLOWING",
        "RAISE",
        "ALTER",
        "FOR",
        "READ",
        "AND",
        "FOREIGN",
        "REBUILD",
        "ANY",
        "FROM",
        "RECOVER",
        "APPLY",
        "FULL",
        "REMOVE",
        "ARCHIVE",
        "FUNCTION",
        "RENAME",
        "ARCHIVELOG",
        "GOTO",
        "REPLACE",
        "AS",
        "GRANT",
        "RETURN",
        "ASC",
        "GROUP",
        "RETURNING",
        "AT",
        "HAVING",
        "REVOKE",
        "AUDIT",
        "IF",
        "RIGHT",
        "AUTOEXTEND",
        "IN",
        "ROLLBACK",
        "BACKUP",
        "INDEX",
        "ROLLUP",
        "BEFORE",
        "INITRANS",
        "ROW",
        "BEGIN",
        "INNER",
        "ROWCOUNT",
        "BETWEEN",
        "INSERT",
        "ROWNUM",
        "BODY",
        "INSTEAD",
        "ROWTYPE",
        "BULK",
        "INTERSECT",
        "SAVEPOINT",
        "BY",
        "INTO",
        "SEGMENT",
        "CASCADE",
        "IS",
        "SELECT",
        "CASE",
        "ISOLATION",
        "SEQUENCE",
        "CAST",
        "JOIN",
        "SESSION",
        "CHECKPOINT",
        "KEY",
        "SET",
        "CLOSE",
        "LANGUAGE",
        "SHARD",
        "COALESCE",
        "LATERAL",
        "SOME",
        "COLUMN",
        "LEFT",
        "SPLIT",
        "COMMENT",
        "LESS",
        "SQLCODE",
        "COMMIT",
        "LEVEL",
        "SQLERRM",
        "COMPILE",
        "LIBRARY",
        "START",
        "COMPRESS",
        "LIFO",
        "STEP",
        "COMPRESSED",
        "LIKE",
        "STORAGE",
        "CONJOIN",
        "LIMIT",
        "STORE",
        "CONNECT",
        "LINK",
        "SYNONYM",
        "CONSTANT",
        "LINKER",
        "TABLE",
        "CONSTRAINTS",
        "LOB",
        "THAN",
        "CONTINUE",
        "LOCAL",
        "THEN",
        "CREATE",
        "LOCK",
        "TIMESTAMPADD",
        "CROSS",
        "LOGANCHOR",
        "TO",
        "CUBE",
        "LOGGING",
        "TOP",
        "CURSOR",
        "LOOP",
        "TRIGGER",
        "CYCLE",
        "MAXROWS",
        "TRUE",
        "DATABASE",
        "MAXTRANS",
        "TRUNCATE",
        "DECLARE",
        "MERGE",
        "TYPE",
        "DECRYPT",
        "MINUS",
        "TYPESET",
        "DEFAULT",
        "MODE",
        "UNION",
        "DELAUDIT",
        "MODIFY",
        "UNIQUE",
        "DELETE",
        "MOVE",
        "UNLOCK",
        "DEQUEUE",
        "MOVEMENT",
        "UNPIVOT",
        "DESC",
        "NEW",
        "UNTIL",
        "DETERMINISTIC",
        "NOAUDIT",
        "UPDATE",
        "DIRECTORY",
        "NOCOPY",
        "USING",
        "DISABLE",
        "NOCYCLE",
        "VALUES",
        "DISASTER",
        "NOLOGGING",
        "VARIABLE",
        "DISCONNECT",
        "NOT",
        "VC2COLL",
        "DISJOIN",
        "NULL",
        "VIEW",
        "DISTINCT",
        "NULLS",
        "VOLATILE",
        "DROP",
        "OF",
        "WAIT",
        "EACH",
        "OFF",
        "WHEN",
        "ELSE",
        "OFFLINE",
        "WHENEVER",
        "ELSEIF",
        "OLD",
        "WHERE",
        "ELSIF",
        "ON",
        "WHILE",
        "ENABLE",
        "ONLINE",
        "WITH",
        "END",
        "OPEN",
        "WITHIN",
        "ENQUEUE",
        "OR",
        "WORK",
        "ESCAPE",
        "ORDER",
        "WRAPPED",
        "EXCEPTION",
        "OTHERS",
        "WRITE",
        "EXEC",
        "OUT",
        "EXECUTE",
        "OUTER",
        "EXISTS",
        "OVER",
        "EXIT",
        "PACKAGE",
        "EXTENT",
        "PARALLEL",
        "EXTENTSIZE",
        "PARTITION",
        "FALSE",
        "PIVOT",
        "FETCH",
        "PRECEDING",
    ]
)


class _AltibaseUnitypeMixin(object):
    """these types appear to return a buffer object."""

    def result_processor(self, dialect, coltype):
        def process(value):
            if value is not None:
                return str(value)  # decode("ucs-2")
            else:
                return None

        return process


class BYTE(sqltypes.TypeEngine):
    __visit_name__ = "BYTE"


class BIT(sqltypes.BINARY):
    __visit_name__ = "BIT"


class VARBIT(sqltypes.BINARY):
    __visit_name__ = "VARBIT"


class NIBBLE(sqltypes.TypeEngine):
    __visit_name__ = "NIBBLE"


class GEOMETRY(sqltypes.TypeEngine):
    __visit_name__ = "GEOMETRY"


class AltibaseTypeCompiler(oracle_base.OracleTypeCompiler):
    def visit_BYTE(self, type_, **kw):
        return "BYTE"

    def visit_BIT(self, type_, **kw):
        return "BIT"

    def visit_VARBIT(self, type_, **kw):
        return "VARBIT(%d)" % type_.length

    def visit_NIBBLE(self, type_, **kw):
        return "NIBBLE"

    def visit_GEOMETRY(self, type_, **kw):
        return "GEOMETRY"


ischema_names = {
    "CHAR": CHAR,
    "VARCHAR": VARCHAR,
    "VARCHAR2": VARCHAR,
    "NCHAR": NCHAR,
    "CLOB": CLOB,
    "BLOB": BLOB,
    "NUMBER": oracle_base.NUMBER,
    "FLOAT": FLOAT,
    "REAL": oracle_base.BINARY_FLOAT,
    "DOUBLE": oracle_base.BINARY_DOUBLE,
    "DECIMAL": DECIMAL,
    "BIGINT": BIGINT,
    "INTEGER": INTEGER,
    "SMALLINT": SMALLINT,
    "DATE": DATE,
    "BYTE": BYTE,
    "NIBBLE": NIBBLE,
    "BIT": BIT,
    "VARBIT": VARBIT,
    "GEOMETRY": GEOMETRY,
}


class AltibaseInspector(reflection.Inspector):
    def __init__(self, conn):
        reflection.Inspector.__init__(self, conn)


class AltibaseExecutionContext(oracle_base.OracleExecutionContext):
    pass


class AltibaseSQLCompiler(oracle_base.OracleCompiler):
    def limit_clause(self, select, **kw):
        if select._limit_clause is None and select._offset_clause is None:
            return ""
        elif select._offset_clause is not None:
            if select._limit_clause is None:
                return " \n LIMIT %s, %s" % (
                    self.process(select._offset_clause, **kw),
                    "18446744073709551615",
                )
            else:
                return " \n LIMIT %s, %s" % (
                    self.process(select._offset_clause, **kw),
                    self.process(select._limit_clause, **kw),
                )
        else:
            # No offset provided, so just use the limit
            return " \n LIMIT %s" % (self.process(select._limit_clause, **kw),)

    def translate_select_structure(self, select_stmt, **kwargs):
        return select_stmt  # skip


class AltibaseDDLCompiler(oracle_base.OracleDDLCompiler):
    pass


class AltibaseIdentifierPreparer(oracle_base.OracleIdentifierPreparer):
    # override LEGAL_CHARACTERS to add `#` for issue #1
    reserved_words = {x.lower() for x in RESERVED_WORDS}


class AltibaseDialect(default.DefaultDialect):
    name = "altibase"
    supports_statement_cache = True
    supports_alter = True
    supports_unicode_statements = False
    supports_unicode_binds = False
    max_identifier_length = 128

    supports_simple_order_by_label = False
    cte_follows_insert = True

    supports_sequences = True
    sequences_optional = False
    postfetch_lastrowid = False

    default_paramstyle = "named"
    colspecs = oracle_base.colspecs
    ischema_names = ischema_names
    requires_name_normalize = True

    supports_comments = True

    supports_default_values = False
    supports_default_metavalue = True
    supports_empty_insert = False
    supports_identity_columns = True

    type_compiler = AltibaseTypeCompiler
    statement_compiler = AltibaseSQLCompiler
    ddl_compiler = AltibaseDDLCompiler
    preparer = AltibaseIdentifierPreparer
    inspector = AltibaseInspector
    oracle_dialect = oracle_base.OracleDialect

    def __init__(
        self,
        use_ansi=True,
        optimize_limits=False,
        use_binds_for_limits=None,
        use_nchar_for_unicode=False,
        exclude_schemaspaces=("PUBLIC", "SYSTEM_", "SYS"),
        **kwargs,
    ):
        default.DefaultDialect.__init__(self, **kwargs)
        self._use_nchar_for_unicode = use_nchar_for_unicode
        self.use_ansi = use_ansi
        self.optimize_limits = optimize_limits
        self.exclude_schemaspaces = exclude_schemaspaces

    def initialize(self, connection):
        super(AltibaseDialect, self).initialize(connection)

    @property
    def _supports_char_length(self):
        return True

    def _get_default_schema_name(self, connection):
        return self.normalize_name(connection.exec_driver_sql("SELECT DB_USERNAME FROM V$SESSION;").scalar())

    def has_table(self, connection, table_name, schema=None):
        self._ensure_has_table_connection(connection)

        if not schema:
            schema = self.default_schema_name

        cursor = connection.execute(
            text(
                "SELECT T.TABLE_NAME 'TABLE_NAME' "
                "FROM SYSTEM_.SYS_TABLES_ T, SYSTEM_.SYS_USERS_ U "
                "WHERE T.TABLE_TYPE = 'T' "
                "AND T.TABLE_NAME = :name "
                "AND T.USER_ID = U.USER_ID "
                "AND U.USER_NAME = :schema_name "
                "ORDER BY T.TABLE_NAME;"
            ),
            dict(
                name=self.denormalize_name(table_name),
                schema_name=self.denormalize_name(schema),
            ),
        )
        return cursor.first() is not None

    @reflection.cache
    def get_schema_names(self, connection, **kw):
        query = "SELECT user_name FROM SYSTEM_.SYS_USERS_ ORDER BY user_name;"
        cursor = connection.exec_driver_sql(query)
        return [self.normalize_name(row[0]) for row in cursor]

    @reflection.cache
    def get_table_names(self, connection, schema=None, **kw):
        schema = self.denormalize_name(schema or self.default_schema_name)

        # note that table_names() isn't loading DBLINKed or synonym'ed tables
        if schema is None:
            schema = self.default_schema_name

        query = "SELECT T.TABLE_NAME 'TABLE_NAME' FROM SYSTEM_.SYS_TABLES_ T, SYSTEM_.SYS_USERS_ U WHERE "
        if self.exclude_schemaspaces:
            query += "U.USER_NAME NOT IN (%s) AND " % (", ".join(["'%s'" % ts for ts in self.exclude_schemaspaces]))
        query += (
            "T.TABLE_TYPE = 'T' "
            "AND T.USER_ID = U.USER_ID "
            "AND U.USER_NAME = :schema_name "
            "ORDER BY T.TABLE_NAME;"
        )

        cursor = connection.execute(text(query), dict(schema_name=schema))

        return [self.normalize_name(row[0]) for row in cursor]

    @reflection.cache
    def get_columns(self, connection, table_name, schema=None, **kw):
        schema = self.denormalize_name(schema or self.default_schema_name)

        if schema is None:
            schema = self.default_schema_name

        query = """
            SELECT U.USER_NAME USER_NAME
            , T.TABLE_NAME TABLE_NAME
            , C.COLUMN_NAME COLUMN_NAME
            , DECODE(C.DATA_TYPE, 1, 'CHAR', 12, 'VARCHAR', -8, 'NCHAR', -9, 'NVARCHAR', 2, 'DECIMAL', 6, 'FLOAT', 8, 'DOUBLE', 7, 'REAL', -5, 'BIGINT', 4, 'INTEGER', 5, 'SMALLINT', 9, 'DATE', 30, 'BLOB', 40, 'CLOB', 20001, 'BYTE', 20002, 'NIBBLE', -7, 'BIT', -100, 'VARBIT', 10003, 'GEOMETRY') DATA_TYPE
            , CASE WHEN (C.DATA_TYPE != 2 OR C.DATA_TYPE != 6) THEN C.PRECISION END AS CHAR_LENGTH_COL
            , DECODE(C.IS_NULLABLE, 'F', 'N', 'T', 'Y') NULLABLE
            , C.DEFAULT_VAL DATA_DEFAULT
            , COM.COMMENTS COMMENTS
        FROM SYSTEM_.SYS_USERS_ U
            INNER JOIN SYSTEM_.SYS_TABLES_ T ON U.USER_ID = T.USER_ID
            INNER JOIN SYSTEM_.SYS_COLUMNS_ C ON T.TABLE_ID = C.TABLE_ID
            LEFT OUTER JOIN SYSTEM_.SYS_COMMENTS_ COM ON T.TABLE_NAME = COM.TABLE_NAME AND C.COLUMN_NAME = COM.COLUMN_NAME AND U.USER_NAME = COM.USER_NAME
        WHERE U.USER_NAME NOT IN ('PUBLIC', 'SYSTEM_', 'SYS')
        AND U.USER_NAME = :schema_name
        AND T.TABLE_NAME = :table_name
        ORDER BY U.USER_NAME, T.TABLE_NAME, C.COLUMN_ORDER ;
        """

        results = connection.execute(
            text(query),
            dict(
                table_name=self.denormalize_name(table_name),
                schema_name=self.denormalize_name(schema),
            ),
        )

        columns = []

        for user_name, table_name, column_name, data_type, char_length_col, nullable, data_default, comments in results:
            if data_type in ("CHAR", "VARCHAR", "NCHAR", "NVARCHAR"):
                data_type = self.ischema_names.get(data_type)(char_length_col)
            else:
                try:
                    data_type = self.ischema_names[data_type]
                except KeyError:
                    warn("Did not recognize type '%s' of column '%s'" % (data_type, column_name))
                    data_type = sqltypes.NULLTYPE

            column_dict = {
                "name": column_name,
                "type": data_type,
                "nullable": nullable == "Y",
                "default": data_default,
                "autoincrement": "auto",
                "comment": comments,
            }
            columns.append(column_dict)

        return columns

    @reflection.cache
    def get_table_comment(self, connection, table_name, schema=None, resolve_synonyms=False, dblink="", **kw):
        if not schema:
            schema = self.default_schema_name

        query = """
            SELECT COMMENTS
            FROM SYSTEM_.SYS_COMMENTS_
            WHERE TABLE_NAME = CAST(:table_name AS VARCHAR(128))
            AND USER_NAME = CAST(:schema_name AS VARCHAR(128))
            AND COLUMN_NAME IS NULL
        """

        c = connection.execute(
            text(query),
            dict(table_name=self.denormalize_name(table_name), schema_name=self.denormalize_name(schema)),
        )
        return {"text": c.scalar()}

    @reflection.cache
    def _get_constraint_data(self, connection, table_name, schema=None, dblink="", **kw):
        if schema is None:
            schema = self.default_schema_name

        query = """SELECT CONST.CONSTRAINT_NAME CONSTRAINT_NAME
            , DECODE(CONST.CONSTRAINT_TYPE, 0, 'FK', 1, 'NOT NULL', 2, 'UNIQUE', 3, 'PK', 4, 'NULL', 5, 'TIMESTAMP', 6, 'LOCAL UNIQUE', 7, 'CHECK') CONSTRAINT_TYPE
            , C.COLUMN_NAME COLUMN_NAME
            , T.TABLE_NAME TABLE_NAME
            , U.USER_NAME USER_NAME
            , C.COLUMN_ORDER COLUMN_POSITION
            , CONST.CHECK_CONDITION CHECK_CONDITION
            , DECODE(CONST.DELETE_RULE, 0, 'NO ACTION', 1, 'CASCADE', 2, 'SET NULL') DELETE_RULE
         FROM SYSTEM_.SYS_USERS_ U
            , SYSTEM_.SYS_TABLES_ T
              INNER JOIN SYSTEM_.SYS_COLUMNS_ C ON T.TABLE_ID = C.TABLE_ID
              LEFT OUTER JOIN SYSTEM_.SYS_CONSTRAINT_COLUMNS_ CONST_COL ON CONST_COL.COLUMN_ID = C.COLUMN_ID
              LEFT OUTER JOIN SYSTEM_.SYS_CONSTRAINTS_ CONST ON CONST.CONSTRAINT_ID = CONST_COL.CONSTRAINT_ID
        WHERE U.USER_ID = T.USER_ID
        AND U.USER_NAME = CAST(:user_name AS VARCHAR(128))
         AND T.TABLE_NAME = CAST(:table_name AS VARCHAR(128))
         ORDER BY CONST.CONSTRAINT_NAME, C.COLUMN_ORDER ;
         """

        rp = connection.execute(
            text(query), dict(table_name=self.denormalize_name(table_name), user_name=self.denormalize_name(schema))
        )
        constraint_data = rp.fetchall()
        return constraint_data

    @reflection.cache
    def get_pk_constraint(self, connection, table_name, schema=None, **kw):
        pkeys = []
        constraint_name = None

        constraint_data = self._get_constraint_data(
            connection,
            table_name,
            schema,
            kw.get("dblink", ""),
            info_cache=kw.get("info_cache"),
        )

        for spec in constraint_data:
            cons_name, cons_type, local_column = spec[0:3]

            if cons_type == "PK":
                if constraint_name is None:
                    constraint_name = self.normalize_name(cons_name)
                pkeys.append(local_column)

        return {"constrained_columns": pkeys, "name": constraint_name}

    @reflection.cache
    def get_foreign_keys(self, connection, table_name, schema=None, **kw):
        dblink = kw.get("dblink", "")

        constraint_data = self._get_constraint_data(
            connection,
            table_name,
            schema,
            dblink,
            info_cache=kw.get("info_cache"),
        )

        fkeys = []

        for spec in constraint_data:
            (
                cons_name,
                cons_type,
                local_column,
                remote_table,
                remote_column,
                remote_owner,
            ) = (
                spec[0:2] + tuple([self.normalize_name(x) for x in spec[2:5]]) + spec[5:6]
            )

            if cons_type == "FK":
                if remote_table is None:
                    warn(
                        (
                            "Got 'None' querying 'table_name' from "
                            "all_cons_columns%(dblink)s - does the user have "
                            "proper rights to the table?"
                        )
                        % {"dblink": dblink}
                    )
                    continue

                fkey_d = {
                    "name": cons_name,
                    "constrained_columns": [],
                    "referred_schema": remote_column,
                    "referred_table": remote_table,
                    "referred_columns": [],
                    "options": {},
                }

                fkeys.append(fkey_d)

        return fkeys

    @reflection.cache
    def get_view_names(self, connection, schema=None, **kw):
        schema = self.denormalize_name(schema or self.default_schema_name)

        query = text(
            """
            SELECT T.TABLE_NAME FROM SYSTEM_.SYS_TABLES_ T
       	        INNER JOIN SYSTEM_.SYS_USERS_ U ON U.USER_ID = T.USER_ID
       	        WHERE T.TABLE_TYPE = 'V'
       	        AND U.USER_NAME = :user_name
       	    """
        )

        cursor = connection.execute(query, dict(user_name=self.denormalize_name(schema)))
        return [self.normalize_name(row[0]) for row in cursor]

    @reflection.cache
    def get_view_definition(self, connection, view_name, schema=None, resolve_synonyms=False, dblink="", **kw):
        query = """
            SELECT P.PARSE FROM SYSTEM_.SYS_TABLES_ T
       	        INNER JOIN SYSTEM_.SYS_USERS_ U ON U.USER_ID = T.USER_ID
       	        INNER JOIN SYSTEM_.SYS_VIEW_PARSE_ P ON T.TABLE_ID = P.VIEW_ID
       	        WHERE T.TABLE_TYPE = 'V'
       	        AND T.TABLE_NAME = :view_name
               """

        params = {"view_name": self.denormalize_name(view_name)}

        if schema is not None:
            query += " AND U.USER_NAME = :user_name"
            params["user_name"] = self.denormalize_name(schema)

        query += " ORDER BY P.SEQ_NO ASC"

        rp = "".join(connection.execute(text(query), params).scalars().all())

        if rp:
            if py2k:
                rp = rp.decode(self.encoding)
            return rp
        else:
            return None


# If alembic is installed, register an alias in its dialect mapping.
try:
    import alembic.ddl.oracle
except ImportError:
    pass
else:

    class AltibaseDBImpl(alembic.ddl.oracle.OracleImpl):
        __dialect__ = "altibase"
        transactional_ddl = True

    # @compiles(alembic.ddl.postgresql.PostgresqlColumnType, "cockroachdb")
    # def visit_column_type(*args, **kwargs):
    #     return alembic.ddl.postgresql.visit_column_type(*args, **kwargs)
