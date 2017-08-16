
"""This module parses the analyst estimates (e.g. Revenue = 7.2B) from strings
to floats."""

import re


def parse_number(string):
    """Converts a number in the form of 1.2B or 1.2M into a float."""
    digits = _parse_digits(string)
    letter = _parse_letter(string)
    if letter == 'B':
        number = digits * 1E9
    else:
        number = digits * 1E6
    return number


def parse_percent(string):
    """Converts a percentage into a float."""
    return _parse_digits(string)


def _parse_digits(string):
    pattern = re.compile('[0-9]*\.?[0-9]+')
    match = pattern.search(string)
    digits = float(match.group())
    return digits


def _parse_letter(string):
    pattern = re.compile('[A-Z]')
    match = pattern.search(string)
    letter = match.group()
    return letter


def _test():
    print(parse_number('123.45B'))
    print(parse_number('123.45M'))
    print(parse_number('123B'))
    print(parse_number('123M'))
    print(parse_number('1B'))
    print(parse_number('1M'))
    print(parse_percent('11.07%'))


if __name__ == "__main__":
    _test()
