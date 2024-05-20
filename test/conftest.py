import pytest
from sqlalchemy.dialects import registry

registry.register("altibase.pyodbc", "sqlalchemy_altibase.pyodbc", "AltibaseDialect_pyodbc")

pytest.register_assert_rewrite("sqlalchemy.testing.assertions")
