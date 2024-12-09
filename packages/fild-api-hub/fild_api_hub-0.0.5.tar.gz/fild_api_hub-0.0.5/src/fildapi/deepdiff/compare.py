from io import StringIO

from pprint import pprint

from fildapi.deepdiff.deepdiff import DeepDiff


def wrap_error_message(target_name, actual, expected, diff):
    """
      Wraps deepdiff error message to highlight actual and expected values.

    !!!IMPORTANT!!!:
      Use DeepDiff constructor with expected dict as first argument to keep
    message consistent.

      Usage Example:
      deep_diff = DeepDiff(expected_data, actual_data)
      printed_deep_diff = StringIO()
      pprint(deep_diff, indent=2, stream=printed_deep_diff)
      assert deep_diff == {}, wrap_error_message(
          target_name=u'data',
          actual=actual_data,
          expected=expected_data,
          diff=printed_deep_diff.getvalue()
      )
    """
    return (
        f'\nUnexpected {target_name} received\n\tActual:   {actual}\n\t'
        f'Expected: {expected},\n\tDiff: \n{diff}'
    ).replace(
        'oldvalue', 'expected value'
    ).replace(
        'newvalue', 'actual value'
    ).replace(
        'oldtype', 'expected type'
    ).replace(
        'newtype', 'actual type'
    )


def compare_data(actual_data, expected_data, ignore_order=False, rules=None,
                 forbid_unapplied_rules=True, target_name='data'):
    deep_diff = DeepDiff(
        expected_data, actual_data, ignore_order=ignore_order, rules=rules,
        forbid_unapplied_rules=forbid_unapplied_rules
    )
    printed_deep_diff = StringIO()
    pprint(deep_diff, indent=2, stream=printed_deep_diff)

    assert not deep_diff, wrap_error_message(
        target_name=target_name,
        actual=actual_data,
        expected=expected_data,
        diff=printed_deep_diff.getvalue()
    )
