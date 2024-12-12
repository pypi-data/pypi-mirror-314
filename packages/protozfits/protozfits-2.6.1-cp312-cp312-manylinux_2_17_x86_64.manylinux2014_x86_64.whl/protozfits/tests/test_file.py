from importlib.resources import files
from pathlib import Path

from protozfits import File

test_data_dir = Path(files("protozfits") / "tests/resources")
example_file_path = str(test_data_dir / "example_10evts.fits.fz")


EVENTS_IN_EXAMPLE_FILE = 10
EXPECTED_NUMBER_OF_PIXELS = 1296
EXPECTED_NUMBER_OF_SAMPLES = 50
FIRST_EVENT_NUMBER = 97750287


def test_file_getitem_with_integer():
    f = File(example_file_path)
    event = f.Events[0]
    assert event.eventNumber == FIRST_EVENT_NUMBER


def test_file_getitem_with_slice():
    f = File(example_file_path)
    expected_event_numbers = [
        FIRST_EVENT_NUMBER + 1,
        FIRST_EVENT_NUMBER + 2,
    ]
    for i, event in enumerate(f.Events[1:3]):
        assert event.eventNumber == expected_event_numbers[i]


def test_file_getitem_with_iterable():
    f = File(example_file_path)
    expected_event_numbers = [
        FIRST_EVENT_NUMBER + 3,
        FIRST_EVENT_NUMBER + 7,
        FIRST_EVENT_NUMBER + 1,
    ]
    for i, event in enumerate(f.Events[[3, 7, 1]]):
        assert event.eventNumber == expected_event_numbers[i]


def test_file_getitem_with_range():
    f = File(example_file_path)
    interesting_event_ids = range(9, 1, -2)
    expected_event_numbers = [FIRST_EVENT_NUMBER + i for i in interesting_event_ids]
    for i, event in enumerate(f.Events[interesting_event_ids]):
        assert event.eventNumber == expected_event_numbers[i]
