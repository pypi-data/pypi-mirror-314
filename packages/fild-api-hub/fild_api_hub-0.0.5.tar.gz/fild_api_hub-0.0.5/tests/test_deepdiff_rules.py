import re

from datetime import datetime, timedelta

import pytest
from fild.sdk.dates import to_format
from fild.sdk.fakeable import Fakeable, fake_string_attr

from fildapi.deepdiff import (
    compare_data, dates_equal_with_delta_3s, equal_with_accuracy_4,
    formatted_dates_equal_with_delta, has_some_value, has_new_value,
    is_valid_uuid, sorted_lists_equal, timestamp_equal_with_delta_3s,
)


def test_has_some_value():
    compare_data(
        expected_data={'one': 1},
        actual_data={'one': 2},
        rules={'one': has_some_value}
    )


def test_has_new_value():
    compare_data(
        expected_data={'one': 1},
        actual_data={'one': 2},
        rules={'one': has_new_value}
    )


def test_is_valid_uuid():
    compare_data(
        expected_data={'one': fake_string_attr(Fakeable.Uuid)},
        actual_data={'one': fake_string_attr(Fakeable.Uuid)},
        rules={'one': is_valid_uuid}
    )


def test_is_valid_uuid_failure():
    uuid = fake_string_attr(Fakeable.Uuid)
    error_message = re.escape(
        '\nUnexpected data received'
        '\n\tActual:   {\'one\': \'test\'}'
        '\n\tExpected: {\'one\': \'' + uuid + '\'},'
        '\n\tDiff: \n{ \'rules_violated\': { "root[\'one\']": '
        '{ \'actual value\': \'test\','
        '\n                                       \'expected value\': '
        '\'' + uuid + '\',\n                                       '
        '\'rule\': \'is_valid_uuid\'}}}\n'
    )

    with pytest.raises(AssertionError, match=error_message):
        compare_data(
            expected_data={'one': uuid},
            actual_data={'one': 'test'},
            rules={'one': is_valid_uuid}
        )


def test_timestamp_equals_with_delta():
    compare_data(
        expected_data={'one': datetime.utcnow()},
        actual_data={'one': datetime.utcnow()},
        rules={'one': timestamp_equal_with_delta_3s}
    )


def test_sorted_list_equal():
    compare_data(
        expected_data={'one': [1, 2, 3]},
        actual_data={'one': [3, 1, 2]},
        rules={'one': sorted_lists_equal}
    )


def test_dates_equal_with_delta():
    compare_data(
        expected_data={'one': '2027-10-15'},
        actual_data={'one': '2027-10-15'},
        rules={'one': dates_equal_with_delta_3s}
    )


def test_floats_equal():
    compare_data(
        expected_data={'one': 12.2145012},
        actual_data={'one': 12.21451921},
        rules={'one': equal_with_accuracy_4}
    )


def test_formatted_dates_with_delta():
    expected = datetime.utcnow()
    actual = expected + timedelta(seconds=2)
    compare_data(
        expected_data={'one': to_format(expected)},
        actual_data={'one': to_format(actual)},
        rules={'one': formatted_dates_equal_with_delta}
    )
