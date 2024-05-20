from sqlalchemy.testing.suite import (
    ComponentReflectionTest as _ComponentReflectionTest,
    CompoundSelectTest as _CompoundSelectTest,
    DateTest as _DateTest,
    DateTimeCoercedToDateTimeTest as _DateTimeCoercedToDateTimeTest,
    DateTimeMicrosecondsTest as _DateTimeMicrosecondsTest,
    DateTimeTest as _DateTimeTest,
    DeprecatedCompoundSelectTest as _DeprecatedCompoundSelectTest,
    DifficultParametersTest as _DifficultParametersTest,
    ExpandingBoundInTest as _ExpandingBoundInTest,
    HasIndexTest as _HasIndexTest,
    HasTableTest as _HasTableTest,
    InsertBehaviorTest as _InsertBehaviorTest,
    IntegerTest as _IntegerTest,
    TimeTest as _TimeTest,
    UnicodeVarcharTest as _UnicodeVarcharTest,
    testing,
)


class ComponentReflectionTest(_ComponentReflectionTest):
    @testing.skip("altibase")
    def test_get_indexes(self):
        # we don't handle exclusions
        return

    @testing.skip("altibase")
    def test_get_unique_constraints(self):
        # "Incorrect syntax near ','."
        # (... but the same query works okay from a DBeaver SQL Editor pane)
        return

    @testing.skip("altibase")
    def test_get_multi_columns(self):
        # (not yet supported)
        return

    @testing.skip("altibase")
    def test_get_multi_indexes(self):
        # (not yet supported)
        return

    @testing.skip("altibase")
    def test_get_multi_pk_constraint(self):
        # (not yet supported)
        return

    @testing.skip("altibase")
    def test_get_multi_unique_constraints(self):
        # (not yet supported)
        return

    @testing.skip("altibase")
    def test_metadata(self):
        return


class CompoundSelectTest(_CompoundSelectTest):
    @testing.skip("altibase")
    def test_distinct_selectable_in_unions(self):
        # "LIMIT clause is not allowed in UNION."
        return

    @testing.skip("altibase")
    def test_limit_offset_aliased_selectable_in_unions(self):
        # "An ORDER BY clause is not allowed in a derived table."
        return

    @testing.skip("altibase")
    def test_limit_offset_in_unions_from_alias(self):
        # "An ORDER BY clause is not allowed in a derived table."
        return

    @testing.skip("altibase")
    def test_limit_offset_selectable_in_unions(self):
        # "Incorrect syntax near the keyword 'ORDER'."
        return

    @testing.skip("altibase")
    def test_order_by_selectable_in_unions(self):
        # "LIMIT clause is not allowed in UNION."
        return


class DateTest(_DateTest):
    @testing.skip("altibase")
    def test_null_bound_comparison(self):
        # "The datatype of a parameter marker used in the dynamic
        #  prepare statement could not be resolved."
        return

    @testing.skip("altibase")
    def test_select_direct(self):
        return


class DateTimeCoercedToDateTimeTest(_DateTimeCoercedToDateTimeTest):
    @testing.skip("altibase")
    def test_null_bound_comparison(self):
        # "The datatype of a parameter marker used in the dynamic
        #  prepare statement could not be resolved."
        return

    @testing.skip("altibase")
    def test_select_direct(self):
        return


class DateTimeMicrosecondsTest(_DateTimeMicrosecondsTest):
    @testing.skip("altibase")
    def test_null_bound_comparison(self):
        # "The datatype of a parameter marker used in the dynamic
        #  prepare statement could not be resolved."
        return


class DateTimeTest(_DateTimeTest):
    @testing.skip("altibase")
    def test_null_bound_comparison(self):
        # "The datatype of a parameter marker used in the dynamic
        #  prepare statement could not be resolved."
        return

    @testing.skip("altibase")
    def test_select_direct(self):
        return


class DeprecatedCompoundSelectTest(_DeprecatedCompoundSelectTest):
    @testing.skip("altibase")
    def test_distinct_selectable_in_unions(self):
        # LIMIT clause is not allowed in UNION.
        return

    @testing.skip("altibase")
    def test_limit_offset_aliased_selectable_in_unions(self):
        # LIMIT clause is not allowed in UNION.
        return

    @testing.skip("altibase")
    def test_limit_offset_selectable_in_unions(self):
        # Incorrect syntax near the keyword 'ORDER'.
        return

    @testing.skip("altibase")
    def test_order_by_selectable_in_unions(self):
        # LIMIT clause is not allowed in UNION.
        return


class DifficultParametersTest(_DifficultParametersTest):
    @testing.skip("altibase")
    def test_round_trip_same_named_column(self):
        return


class ExpandingBoundInTest(_ExpandingBoundInTest):
    @testing.skip("altibase")
    def test_empty_set_against_string(self):
        # "Implicit conversion from datatype 'VARCHAR' to 'INT' is not allowed."
        return

    @testing.skip("altibase")
    def test_empty_set_against_string_negation(self):
        # "Implicit conversion from datatype 'VARCHAR' to 'INT' is not allowed."
        return

    @testing.skip("altibase")
    def test_null_in_empty_set_is_false(self):
        # "Incorrect syntax near the keyword 'NULL'."
        return


class HasIndexTest(_HasIndexTest):
    @testing.skip("altibase")
    def test_has_index(self):
        return


class HasTableTest(_HasTableTest):
    @testing.skip("altibase")
    def test_has_table_cache(self):
        return


class InsertBehaviorTest(_InsertBehaviorTest):
    @testing.skip("altibase")
    def test_empty_insert(self):
        # "Incorrect syntax near ')'."
        return

    @testing.skip("altibase")
    def test_empty_insert_multiple(self):
        # "Incorrect syntax near ')'."
        return

    @testing.skip("altibase")
    def test_limit_offset_selectable_in_unions(self):
        # "Incorrect syntax near the keyword 'ORDER'."
        return

    @testing.skip("altibase")
    def test_insert_from_select_with_defaults(self):
        # "Explicit value specified for identity field in table
        # 'includes_defaults' when 'SET IDENTITY_INSERT' is OFF."
        return


class IntegerTest(_IntegerTest):
    @testing.skip("altibase")
    def test_huge_int_auto_accommodation(self):
        return


class TimeTest(_TimeTest):
    @testing.skip("altibase")
    def test_select_direct(self):
        return


class QuotedNameArgumentTest:
    """Some of these tests can hang the test run."""


class UnicodeVarcharTest(_UnicodeVarcharTest):
    @testing.skip("altibase")
    def test_literal_non_ascii(self):
        # (test hangs)
        return

    @testing.skip("altibase")
    def test_literal_nonnative_text(self):
        # (test hangs)
        return


class UuidTest:
    """Some of these tests can hang the test run."""
