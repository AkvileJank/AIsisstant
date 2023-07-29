from datetime import datetime
import builtins
import pytest
from activity import Activity

def test_get_activity_date_task(monkeypatch):
    user_input = "2023-06-30"
    expected_date = datetime.strptime(user_input, "%Y-%m-%d").date()
    monkeypatch.setattr(builtins, 'input', lambda _: user_input)

    assert Activity.get_activity_date("task") == expected_date

def test_get_activity_date_event(monkeypatch):
    user_input = "2023-07-15"
    expected_date = datetime.strptime(user_input, "%Y-%m-%d").date()
    monkeypatch.setattr(builtins, 'input', lambda _: user_input)

    assert Activity.get_activity_date("event") == expected_date

def test_get_activity_date_invalid_format(monkeypatch):
    user_input = "not_date"
    monkeypatch.setattr(builtins, 'input', lambda _: user_input)

    with pytest.raises(ValueError):
        Activity.get_activity_date("invalid")
