import pytest
import datetime as dt
import pandas as pd

from user import User
from auditTrailTable import AuditTrailTable
from boxAssembler import BoxAssembler
from boxesTable import BoxesTable

def create_box_assembler() -> BoxAssembler:
    return BoxAssembler(create_an_audit_trail(), create_boxes_table())

def create_an_audit_trail() -> AuditTrailTable:
    return AuditTrailTable()

def create_boxes_table() -> BoxesTable:
    return BoxesTable()

def create_user() -> User:
    return User('Username', 'Name', 'Lastname', 'Email', 'Department', 'Facility', dt.datetime.today())

def test00_create_box_assembler():
    box_assembler = create_box_assembler()
    assert box_assembler is not None

def test01_starts_with_no_boxes():
    box_assembler = create_box_assembler()
    assert box_assembler.has_box_count(0)

def test02_add_box():
    box_assembler = create_box_assembler()
    box_assembler.create_box('Type', 'Description', 'Position', create_user())
    assert box_assembler.has_box_count(1)

    box_assembler.create_box('Type', 'Description', 'Position', create_user())
    assert box_assembler.has_box_count(2)
    
def test03_add_one_box_deny_another_count():
    box_assembler = create_box_assembler()
    box_assembler.create_box('Type', 'Description', 'Position', create_user())
    assert not box_assembler.has_box_count(0)

def test04_add_one_box_check_last_box_id():
    box_assembler = create_box_assembler()
    box_assembler.create_box('Type', 'Description', 'Position', create_user())
    assert box_assembler.has_as_last_box_id('AAAAAAA')

def test05_add_one_box_check_last_box_id_deny_another():
    box_assembler = create_box_assembler()
    box_assembler.create_box('Type', 'Description', 'Position', create_user())
    assert not box_assembler.has_as_last_box_id('AAAAAAB')

def test06_add_multiple_boxes_check_last_box_id():
    box_assembler = create_box_assembler()
    box_assembler.create_box('Type', 'Description', 'Position', create_user())
    box_assembler.create_box('Type', 'Description', 'Position', create_user())
    
    assert box_assembler.has_as_last_box_id('AAAAAAB')
    assert not box_assembler.has_as_last_box_id('AAAAAAA')

    for i in range(25):
        box_assembler.create_box('Type', 'Description', 'Position', create_user())

    assert box_assembler.has_as_last_box_id('AAAAABA')

def test07_when_starts_audit_trail_is_empty():
    box_assembler = create_box_assembler()
    assert box_assembler.has_audit_trail_count(0)

def test08_add_box_adds_audit_trail_entry():
    box_assembler = create_box_assembler()
    box_assembler.create_box('Type', 'Description', 'Position', create_user())
    assert box_assembler.has_audit_trail_count(1)

def test09_add_box_append_correct_record_to_audit_trail():
    datetime_value = dt.datetime.now()

    audit_trail = create_an_audit_trail()
    box_assembler = BoxAssembler(audit_trail, create_boxes_table())
    box_assembler.create_box('Type', 'Description', 'Position', create_user(), datetime_value)

    correct_result = pd.DataFrame(
        {'item': ['AAAAAAA'], 
        'action': ['Create box'], 
        'from_position': ['N/A'], 
        'to_position': ['Position'], 
        'user': ['Username'], 
        'date_time': [datetime_value]}
        )

    assert audit_trail.has_entries(correct_result)

def test10_add_box_append_an_incorrect_record_to_audit_trail():
    datetime_value = dt.datetime.now()

    audit_trail = create_an_audit_trail()
    box_assembler = BoxAssembler(audit_trail, create_boxes_table())
    box_assembler.create_box('Type', 'Description', 'Position', create_user(), datetime_value)

    incorrect_result = pd.DataFrame(
        {'item': ['AAAAAAA'], 
        'action': ['Create box'], 
        'from_position': ['N/A'], 
        'to_position': ['Position'], 
        'user': ['Username'], 
        'date_time': [datetime_value + dt.timedelta(seconds=1)]}
        )

    assert not audit_trail.has_entries(incorrect_result)

def test11_add_box_append_multiples_records_to_audit_trail():
    datetime_value = dt.datetime.now()

    audit_trail = create_an_audit_trail()
    box_assembler = BoxAssembler(audit_trail, create_boxes_table())
    box_assembler.create_box('Type', 'Description', 'Position', create_user(), datetime_value)
    box_assembler.create_box('Type', 'Description', 'Position', create_user(), datetime_value + dt.timedelta(seconds=1))

    correct_result = pd.DataFrame(
        {'item': ['AAAAAAA', 'AAAAAAB'], 
        'action': ['Create box', 'Create box'], 
        'from_position': ['N/A', 'N/A'], 
        'to_position': ['Position', 'Position'], 
        'user': ['Username', 'Username'], 
        'date_time': [datetime_value, datetime_value + dt.timedelta(seconds=1)]}
        )

    assert audit_trail.has_entries(correct_result)

def test12_when_tries_to_create_an_invalid_box_do_not_increase_box_count():
    box_assembler = create_box_assembler()
    box_assembler.create_box('Type', 'Description', 'Position', create_user())
    
    try:
        box_assembler.create_box('', 'Description', 'Position', create_user())
    except ValueError:
        assert box_assembler.has_box_count(1)

    try:
        box_assembler.create_box('Type', '', 'Position', create_user())
    except ValueError:
        assert box_assembler.has_box_count(1)

    try:
        box_assembler.create_box('Type', 'Description', '', create_user())
    except ValueError:
        assert box_assembler.has_box_count(1)