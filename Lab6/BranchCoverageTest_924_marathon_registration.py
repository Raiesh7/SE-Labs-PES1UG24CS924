import pytest

from marathon_registration import entry_fee, finisher_status, start_wave


def test_entry_fee_unknown_race():
    with pytest.raises(ValueError, match="unknown race"):
        entry_fee("marathon", 30, False, False)


@pytest.mark.parametrize("age", [11, 12])
def test_entry_fee_too_young(age):
    if age < 12:
        with pytest.raises(ValueError, match="too young"):
            entry_fee("5k", age, False, False)
    else:
        assert entry_fee("5k", age, False, False) == 500


def test_entry_fee_long_race_too_young():
    with pytest.raises(ValueError, match="too young"):
        entry_fee("half", 17, False, False)


@pytest.mark.parametrize(
    ("race", "age", "early_bird", "tshirt", "expected"),
    [
        ("5k", 30, True, False, 375),
        ("10k", 30, False, True, 1100),
        ("full", 65, True, True, 975),
        ("half", 18, False, False, 1200),
    ],
)
def test_entry_fee_branches(race, age, early_bird, tshirt, expected):
    assert entry_fee(race, age, early_bird, tshirt) == expected


@pytest.mark.parametrize(
    ("time", "race", "expected"),
    [
        (None, "5k", "D"),
        (180, "full", "A"),
        (240, "full", "B"),
        (241, "full", "C"),
        (90, "5k", "A"),
        (120, "5k", "B"),
        (121, "10k", "C"),
    ],
)
def test_start_wave_branches(time, race, expected):
    assert start_wave(time, race) == expected


@pytest.mark.parametrize(
    ("elapsed", "race", "missed", "expected"),
    [
        (400, "5k", 1, "DSQ"),
        (360, "full", 0, "finisher"),
        (361, "full", 0, "DNF"),
        (180, "half", 0, "finisher"),
        (181, "half", 0, "DNF"),
        (90, "5k", 0, "finisher"),
        (91, "5k", 0, "DNF"),
    ],
)
def test_finisher_status_branches(elapsed, race, missed, expected):
    assert finisher_status(elapsed, race, missed) == expected
