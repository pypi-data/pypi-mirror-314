import re

import pytest

from fild_compare import compare_data


def test_compare_data_matching():
    compare_data(expected_data={'test': 1}, actual_data={'test': 1})


def test_compare_data_not_matching():
    expected_exception = re.escape(
        "\nUnexpected data received\n\t"
        "Actual: {'test': 2}\n\t"
        "Expected: {'test': 1},\n\t"
        "Diff: \n{\'value_changed\': "
        "{\'root[test]\': {\'actual value\': 2, \'expected value\': 1}}}\n"
    )
    with pytest.raises(AssertionError, match=expected_exception):
        compare_data(expected_data={'test': 1}, actual_data={'test': 2})
