from io import StringIO

from pprint import pprint

from fild_compare.diff import Diff


def compare_data(actual_data, expected_data, rules=None,
                 forbid_unapplied_rules=True, target_name='data'):
    deep_diff = Diff(expected_data, actual_data, rules=rules,
                     forbid_unapplied_rules=forbid_unapplied_rules)
    printed_deep_diff = StringIO()
    pprint(deep_diff, indent=2, stream=printed_deep_diff)

    assert not deep_diff, (
        f'\nUnexpected {target_name} received'
        f'\n\tActual: {actual_data}'
        f'\n\tExpected: {expected_data},'
        f'\n\tDiff: \n{printed_deep_diff.getvalue()}'
    )
