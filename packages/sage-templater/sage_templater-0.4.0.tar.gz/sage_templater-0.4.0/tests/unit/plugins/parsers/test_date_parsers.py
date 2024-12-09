from datetime import datetime

import pytest

from sage_templater.plugins.parsers.date_parsers import parse_date


class TestDateParsers:

    @pytest.mark.parametrize("str_date, expected_date", [
        ("2022-01-02", datetime(2022, 1, 2)),
        ("2022-1-2", datetime(2022, 1, 2)),
        ("2/1/2022", datetime(2022, 1, 2)),
        ("2-1-2022", datetime(2022, 1, 2)),
        ("18/05/2021", datetime(2021, 5, 18)),
        ("18-05-2021", datetime(2021, 5, 18)),
        ("18/05/21", datetime(2021, 5, 18)),
        ("18-05-21", datetime(2021, 5, 18)),
    ])
    def test_parse_date(self, str_date, expected_date):
        date = parse_date(str_date)
        assert date == expected_date

    @pytest.mark.parametrize("str_date", [
        "20282-01-02",
        "19/19/2022",
    ])
    def test_parse_date_invalid(self, str_date):
        date = parse_date(str_date)
        assert date is None
