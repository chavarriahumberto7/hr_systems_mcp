from datetime import datetime

VALID_JOB_LEVELS = {"Junior", "Mid", "Senior", "Executive"}
VALID_EMPLOYMENT_STATUSES = {"Active", "Terminated"}


def is_valid_date(value: str, fmt: str = "%Y-%m-%d") -> bool:
    try:
        datetime.strptime(value, fmt)
        return True
    except ValueError:
        return False
