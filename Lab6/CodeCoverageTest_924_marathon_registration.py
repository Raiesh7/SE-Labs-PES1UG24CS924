import pytest

from marathon_registration import entry_fee, finisher_status, start_wave


@pytest.mark.parametrize(
    ("race", "age", "early_bird", "tshirt", "expected"),
    [
        ("5k", 12, False, False, 500),
        ("5k", 11, False, False, None),
        ("10k", 30, True, False, 600),
        ("half", 17, False, False, None),
        ("full", 17, False, False, None),
        ("full", 65, True, True, 975),
        ("bad", 30, False, False, None),
    ],
)
def test_entry_fee_values(race, age, early_bird, tshirt, expected):
    if expected is None:
        with pytest.raises(ValueError):
            entry_fee(race, age, early_bird, tshirt)
    else:
        assert entry_fee(race, age, early_bird, tshirt) == expected


@pytest.mark.parametrize(
    ("time", "race", "expected"),
    [
        (None, "full", "D"),
        (180, "full", "A"),
        (200, "full", "B"),
        (300, "full", "C"),
        (90, "10k", "A"),
        (100, "5k", "B"),
        (150, "half", "C"),
    ],
)
def test_start_wave(time, race, expected):
    assert start_wave(time, race) == expected


@pytest.mark.parametrize(
    ("elapsed", "race", "missed", "expected"),
    [
        (400, "full", 1, "DSQ"),
        (360, "full", 0, "finisher"),
        (361, "full", 0, "DNF"),
        (180, "half", 0, "finisher"),
        (181, "half", 0, "DNF"),
        (90, "5k", 0, "finisher"),
        (91, "10k", 0, "DNF"),
    ],
)
def test_finisher_status(elapsed, race, missed, expected):
    assert finisher_status(elapsed, race, missed) == expected
