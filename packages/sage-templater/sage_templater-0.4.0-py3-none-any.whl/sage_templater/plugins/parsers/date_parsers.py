import re
from datetime import datetime

# Pre-compile the regular expressions and store them with their corresponding format strings
datetime_patterns = [
    (re.compile(r"(?P<year>[0-9]{4})-(?P<month>[\d]{1,2})-(?P<day>[\d]{1,2})"), "%Y-%m-%d"),
    (re.compile(r"(?P<day>[\d]{1,2})/(?P<month>[\d]{1,2})/(?P<year>[0-9]{4})"), "%d/%m/%Y"),
    (re.compile(r"(?P<day>[\d]{1,2})-(?P<month>[\d]{1,2})-(?P<year>[0-9]{4})"), "%d-%m-%Y"),
    (re.compile(r"(?P<day>[\d]{1,2})/(?P<month>[\d]{1,2})/(?P<year>[\d]{2})"), "%d/%m/%y"),
    (re.compile(r"(?P<day>[\d]{1,2})-(?P<month>[\d]{1,2})-(?P<year>[\d]{2})"), "%d-%m-%y"),
    (re.compile(r"(?P<year>[0-9]{4})-(?P<month>1[0-2]|0[1-9])-(?P<day>3[01]|[12][0-9]|0[1-9]) "
                r"(?P<hour>2[0-3]|[01][0-9]):(?P<min>[0-5][0-9]):(?P<sec>[0-5][0-9])"), "%Y-%m-%d %H:%M:%S"),
]


def parse_date(str_date: str, raise_error: bool = False,
               patterns=None) -> datetime | None:
    if patterns is None:
        patterns = datetime_patterns
    for pattern, format_str in patterns:
        match = pattern.match(str_date)
        if match:
            try:
                return datetime.strptime(str_date, format_str)
            except ValueError:
                if raise_error:
                    raise
                return None
    return None
