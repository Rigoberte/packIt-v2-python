import pytest
import pandas as pd
import datetime as dt

from auditTrailTable import AuditTrailTable

def create_an_audit_trail() -> AuditTrailTable:
    return AuditTrailTable()

def test00_create_audit_trail():
    audit_trail = create_an_audit_trail()
    assert audit_trail is not None

def test01_new_audit_trail_has_no_entries():
    audit_trail = create_an_audit_trail()
    assert audit_trail.has_entry_count(0)

def test02_add_entry_to_audit_trail_increases_count():
    audit_trail = create_an_audit_trail()
    datetime_value = dt.datetime.now()

    audit_trail.add_entry('item', 'action', 'from_position', 'to_position', 'user', datetime_value)
    assert audit_trail.has_entry_count(1)

    audit_trail.add_entry('item2', 'action', 'from_position', 'to_position', 'user', datetime_value)
    assert audit_trail.has_entry_count(2)

def test03_assert_entry_values():
    audit_trail = create_an_audit_trail()
    datetime_value = dt.datetime.now()

    audit_trail.add_entry('item1', 'action1', 'from_position1', 'to_position2', 'user1', datetime_value)
    audit_trail.add_entry('item2', 'action2', 'from_position1', 'to_position2', 'user1', datetime_value)
    audit_trail.add_entry('item3', 'action3', 'from_position1', 'to_position2', 'user1', datetime_value)

    result = pd.DataFrame(
        {'item': ['item1', 'item2', 'item3'], 
        'action': ['action1', 'action2', 'action3'], 
        'from_position': ['from_position1', 'from_position1', 'from_position1'], 
        'to_position': ['to_position2', 'to_position2', 'to_position2'], 
        'user': ['user1', 'user1', 'user1'], 
        'date_time': [datetime_value, datetime_value, datetime_value]})

    assert audit_trail.has_entries(result)

def test04_deny_other_entries():
    audit_trail = create_an_audit_trail()
    datetime_value = dt.datetime.now()

    audit_trail.add_entry('item1', 'action1', 'from_position1', 'to_position2', 'user1', datetime_value)
    audit_trail.add_entry('item2', 'action2', 'from_position1', 'to_position2', 'user1', datetime_value)
    audit_trail.add_entry('item3', 'action3', 'from_position1', 'to_position2', 'user1', datetime_value)

    different_result = pd.DataFrame(
        {'item': ['item1', 'item4', 'item3'], 
        'action': ['action1', 'action4', 'action3'], 
        'from_position': ['from_position1', 'from_position2', 'from_position1'], 
        'to_position': ['to_position2', 'to_position3', 'to_position2'], 
        'user': ['user1', 'user2', 'user1'], 
        'date_time': [datetime_value, datetime_value, datetime_value + dt.timedelta(days=1)]}
        )

    assert not audit_trail.has_entries(different_result)

def test05_add_entry_with_empty_item():
    audit_trail = create_an_audit_trail()
    with pytest.raises(ValueError, match='Item must be a non-empty string.'):
        audit_trail.add_entry('', 'action', 'from_position', 'to_position', 'user', 'date_time')

def test06_add_entry_with_empty_action():
    audit_trail = create_an_audit_trail()
    with pytest.raises(ValueError, match='Action must be a non-empty string.'):
        audit_trail.add_entry('item', '', 'from_position', 'to_position', 'user', 'date_time')

def test07_add_entry_with_empty_from_position():
    audit_trail = create_an_audit_trail()
    with pytest.raises(ValueError, match='From_position must be a non-empty string.'):
        audit_trail.add_entry('item', 'action', '', 'to_position', 'user', 'date_time')

def test08_add_entry_with_empty_to_position():
    audit_trail = create_an_audit_trail()
    with pytest.raises(ValueError, match='To_position must be a non-empty string.'):
        audit_trail.add_entry('item', 'action', 'from_position', '', 'user', 'date_time')

def test09_add_entry_with_empty_user():
    audit_trail = create_an_audit_trail()
    with pytest.raises(ValueError, match='User must be a non-empty string.'):
        audit_trail.add_entry('item', 'action', 'from_position', 'to_position', '', 'date_time')

def test10_add_entry_with_non_datetime_date_time():
    audit_trail = create_an_audit_trail()
    with pytest.raises(ValueError, match='Date time must be a datetime object.'):
        audit_trail.add_entry('item', 'action', 'from_position', 'to_position', 'user', 'date_time')