import re

import pytest

from fildapi.deepdiff import compare_data


def test_compare_data():
    error_message = re.escape(
        '\nUnexpected dictionaries received'
        '\n\tActual:   {1: \'two\'}'
        '\n\tExpected: {1: \'one\'},'
        '\n\tDiff: \n{\'values_changed\': {\'root[1]\': '
        '{\'actual value\': \'two\', \'expected value\': \'one\'}}}\n'
    )

    with pytest.raises(AssertionError, match=error_message):
        compare_data(
            expected_data={1: 'one'},
            actual_data={1: 'two'},
            target_name='dictionaries'
        )
