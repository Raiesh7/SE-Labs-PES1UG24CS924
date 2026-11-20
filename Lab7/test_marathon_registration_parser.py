from hypothesis import given, strategies as st

from marathon_registration_parser import (
    average_split,
    format_bib_name,
    parse_finish_time,
)


@given(st.one_of(st.text(), st.none()))
def test_format_bib_name_no_crash(value):
    try:
        result = format_bib_name(value)
    except Exception as error:
        raise AssertionError("format_bib_name raised an exception") from error
    assert result is None or isinstance(result, str)
    if isinstance(result, str):
        assert len(result) <= 12


@given(st.one_of(st.text(), st.none()))
def test_parse_finish_time_no_crash(value):
    try:
        result = parse_finish_time(value)
    except Exception as error:
        raise AssertionError("parse_finish_time raised an exception") from error
    assert result is None or (
        isinstance(result, int) and result >= 0
    )


@given(st.one_of(st.text(), st.none()))
def test_average_split_no_crash(value):
    try:
        result = average_split(value)
    except Exception as error:
        raise AssertionError("average_split raised an exception") from error
    assert result is None or (
        isinstance(result, (int, float)) and result >= 0
    )
