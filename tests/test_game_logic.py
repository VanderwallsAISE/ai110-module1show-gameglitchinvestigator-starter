"""
Pytest suite for the Game Glitch Investigator fixes.

Each test below maps to a specific bug that was fixed during the assignment.
The tests only exercise the importable game logic in ``logic_utils.py``; the
Streamlit-only fixes (attempts counter init, New Game state reset) live in
``app.py`` session state and are verified manually in the app.

NOTE: ``check_guess`` returns a ``(outcome, message)`` tuple, so these tests
unpack/inspect both halves. (The original starter tests asserted against a bare
string, which no longer matches the function's return value.)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    validate_in_range,
    check_guess,
)


# ---------------------------------------------------------------------------
# BUG 1: Hard difficulty range
# "Fix hard difficulty range" (86377c7)
# Hard mode used range 1-50, which was SMALLER than Normal (1-100), making Hard
# easier instead of harder. It should now be the widest range.
# ---------------------------------------------------------------------------

def test_hard_range_is_now_correct():
    # Hard should be 1-200 after the fix (was 1-50).
    assert get_range_for_difficulty("Hard") == (1, 200)


def test_hard_is_harder_than_normal():
    # The core symptom: Hard's range must be larger than Normal's.
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high


# ---------------------------------------------------------------------------
# BUG 2: Difficulty range display
# "Fix difficulty range display" (e0335df)
# The displayed range was hardcoded to "1 and 100" regardless of difficulty.
# The fix makes the app read the bounds from get_range_for_difficulty, so each
# difficulty must return its own distinct, correct range.
# ---------------------------------------------------------------------------

def test_easy_range():
    assert get_range_for_difficulty("Easy") == (1, 20)


def test_normal_range():
    assert get_range_for_difficulty("Normal") == (1, 100)


def test_unknown_difficulty_falls_back_to_default():
    # Anything unrecognized defaults to the Normal range.
    assert get_range_for_difficulty("Impossible") == (1, 100)


def test_each_difficulty_has_a_distinct_range():
    # The display bug showed the same range for everything; ranges must differ.
    ranges = {
        get_range_for_difficulty("Easy"),
        get_range_for_difficulty("Normal"),
        get_range_for_difficulty("Hard"),
    }
    assert len(ranges) == 3


# ---------------------------------------------------------------------------
# BUG 3: Reversed hint messages
# "Fix reversed hint messages" (3c348db)
# A guess that was too high told the player to "GO HIGHER" and vice-versa.
# Now the outcome AND the directional hint must agree.
# ---------------------------------------------------------------------------

def test_too_high_tells_player_to_go_lower():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message.upper()
    assert "HIGHER" not in message.upper()


def test_too_low_tells_player_to_go_higher():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message.upper()
    assert "LOWER" not in message.upper()


def test_winning_guess():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


# ---------------------------------------------------------------------------
# BUG 4: Secret coerced to a string every other attempt
# "Fix game logic bugs" (b41f201)
# The old code turned the secret into a string on alternating attempts, so
# numeric comparison silently broke. check_guess must now compare numerically
# and return consistent results for the same inputs.
# ---------------------------------------------------------------------------

def test_check_guess_returns_outcome_message_tuple():
    result = check_guess(10, 20)
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_check_guess_is_consistent_across_calls():
    # The string-coercion glitch made results depend on attempt parity.
    # The same (guess, secret) must always yield the same outcome.
    first = check_guess(75, 50)
    second = check_guess(75, 50)
    assert first == second
    assert first[0] == "Too High"


def test_check_guess_uses_numeric_not_lexical_comparison():
    # Lexically "100" < "20", but numerically 100 > 20. The fix must compare
    # as numbers, so guessing 100 when the secret is 20 is "Too High".
    outcome, _ = check_guess(100, 20)
    assert outcome == "Too High"


# ---------------------------------------------------------------------------
# BUG 5: Invalid guesses counted as attempts
# "Prevent invalid guesses from counting as attempts" (4703d4a)
# Non-numeric / empty input used to be accepted. parse_guess must reject bad
# input (so app.py can skip incrementing attempts) and accept valid numbers.
# ---------------------------------------------------------------------------

def test_parse_guess_rejects_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err


def test_parse_guess_rejects_none():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None
    assert err


def test_parse_guess_rejects_non_numeric():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err


def test_parse_guess_accepts_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_guess_accepts_and_truncates_float_input():
    ok, value, err = parse_guess("42.9")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_guess_returns_int_not_raw_string():
    # The fix appends the parsed int to history (not the raw string).
    ok, value, _ = parse_guess("7")
    assert ok is True
    assert isinstance(value, int)


# ---------------------------------------------------------------------------
# CHALLENGE 1: Out-of-range validation
# A guess below the selected low value or above the selected high value must
# be rejected with an error so app.py can show it and skip counting the
# attempt. validate_in_range(guess, low, high) returns (ok, error_message).
# ---------------------------------------------------------------------------

def test_in_range_guess_is_accepted():
    ok, err = validate_in_range(50, 1, 100)
    assert ok is True
    assert err is None


def test_guess_below_low_is_rejected():
    ok, err = validate_in_range(0, 1, 100)
    assert ok is False
    assert err


def test_guess_above_high_is_rejected():
    ok, err = validate_in_range(101, 1, 100)
    assert ok is False
    assert err


def test_low_boundary_is_inclusive():
    # The low bound itself is a valid guess.
    ok, err = validate_in_range(1, 1, 100)
    assert ok is True
    assert err is None


def test_high_boundary_is_inclusive():
    # The high bound itself is a valid guess.
    ok, err = validate_in_range(100, 1, 100)
    assert ok is True
    assert err is None


def test_negative_guess_is_rejected_when_range_is_positive():
    ok, err = validate_in_range(-5, 1, 20)
    assert ok is False
    assert err


def test_very_large_guess_is_rejected():
    ok, err = validate_in_range(10_000_000, 1, 200)
    assert ok is False
    assert err


@pytest.mark.parametrize("guess", [-1000, -1, 0, 201, 1000, 999_999_999])
def test_out_of_range_guesses_are_all_rejected(guess):
    ok, err = validate_in_range(guess, 1, 200)
    assert ok is False
    assert err


@pytest.mark.parametrize("guess", [1, 2, 100, 199, 200])
def test_in_range_guesses_are_all_accepted(guess):
    ok, err = validate_in_range(guess, 1, 200)
    assert ok is True
    assert err is None


# ---------------------------------------------------------------------------
# CHALLENGE 1 (cont.): parse_guess edge cases
# Empty input, non-numeric input, decimals, negative numbers, and very large
# values must all be handled without crashing.
# ---------------------------------------------------------------------------

def test_parse_guess_rejects_whitespace_as_non_numeric():
    ok, value, err = parse_guess("   ")
    assert ok is False
    assert value is None
    assert err


@pytest.mark.parametrize("raw", ["abc", "12abc", "$10", "one", "5,000", "1e5x"])
def test_parse_guess_rejects_various_non_numeric_input(raw):
    ok, value, err = parse_guess(raw)
    assert ok is False
    assert value is None
    assert err


def test_parse_guess_accepts_negative_integer():
    ok, value, err = parse_guess("-7")
    assert ok is True
    assert value == -7
    assert err is None


def test_parse_guess_truncates_negative_decimal_toward_zero():
    # int(float("-3.9")) == -3 (truncation toward zero, not floor).
    ok, value, err = parse_guess("-3.9")
    assert ok is True
    assert value == -3
    assert err is None


@pytest.mark.parametrize(
    "raw, expected",
    [("0.0", 0), ("3.14", 3), ("99.999", 99), ("-0.5", 0)],
)
def test_parse_guess_truncates_decimals(raw, expected):
    ok, value, err = parse_guess(raw)
    assert ok is True
    assert value == expected
    assert err is None


def test_parse_guess_accepts_very_large_value():
    ok, value, err = parse_guess("100000000000000000000")
    assert ok is True
    assert value == 100000000000000000000
    assert err is None


def test_parse_then_validate_rejects_large_value_without_counting():
    # End-to-end of the Challenge 1 flow: a huge but numeric guess parses
    # fine, then fails the range check (so app.py won't count the attempt).
    ok, value, err = parse_guess("1000000")
    assert ok is True
    in_range, range_err = validate_in_range(value, 1, 200)
    assert in_range is False
    assert range_err
