import pytest
import datetime as dt
import pandas as pd

from boxChanger import BoxChanger
from boxesTable import BoxesTable
from boxAssembler import BoxAssembler
from auditTrailTable import AuditTrailTable
from user import User

def create_BoxChanger(auditTrailTable, boxesTable) -> BoxChanger:
    return BoxChanger(auditTrailTable, boxesTable)

def create_BoxAssembler(auditTrailTable, boxesTable) -> BoxAssembler:
    return BoxAssembler(auditTrailTable, boxesTable)

def setUp():
    boxesTable = BoxesTable()
    auditTrailTable = AuditTrailTable()
    boxChanger = create_BoxChanger(auditTrailTable, boxesTable)
    boxAssembler = create_BoxAssembler(auditTrailTable, boxesTable)
    user = User("username", "name", "lastname", "email", "userDepartment", "facility", dt.datetime.now())

    return boxesTable, auditTrailTable, boxChanger, boxAssembler, user

def test00_createBoxChanger():
    _, _,boxChanger, _, _ = setUp()
    assert boxChanger is not None

def test01_update_a_box_status():
    boxesTable, auditTrailTable, boxChanger, boxAssembler, user = setUp()

    boxAssembler.create_box("Box Type", "Box description", "Box Position", user, dt.datetime.now())

    boxChanger.update_box_status("AAAAAAA", "INACTIVE", user, dt.datetime.now())

    assert boxesTable.check_box_status("AAAAAAA", "INACTIVE")

def test02_update_a_box_status_of_a_non_existing_box():
    boxesTable, auditTrailTable, boxChanger, boxAssembler, user = setUp()

    boxAssembler.create_box("Box Type", "Box description", "Box Position", user, dt.datetime.now())

    with pytest.raises(ValueError, match="Box with ID AAAAAAB not found."):
        boxChanger.update_box_status("AAAAAAB", "INACTIVE", user, dt.datetime.now())

    assert auditTrailTable.has_entry_count(1)

def test03_update_a_box_status_to_empty_string():
    boxesTable, auditTrailTable, boxChanger, boxAssembler, user = setUp()

    boxAssembler.create_box("Box Type", "Box description", "Box Position", user, dt.datetime.now())

    with pytest.raises(ValueError, match="Unknown position status."):
        boxChanger.update_box_status("AAAAAAA", "", user, dt.datetime.now())

    assert auditTrailTable.has_entry_count(1)

def test04_update_a_box_status_to_invalid_status():
    boxesTable, auditTrailTable, boxChanger, boxAssembler, user = setUp()

    boxAssembler.create_box("Box Type", "Box description", "Box Position", user, dt.datetime.now())

    with pytest.raises(ValueError, match="Unknown position status."):
        boxChanger.update_box_status("AAAAAAA", "INVALID", user, dt.datetime.now())

    assert auditTrailTable.has_entry_count(1)

def test05_when_box_status_is_changed_audit_trail_is_updated():
    boxesTable, auditTrailTable, boxChanger, boxAssembler, user = setUp()

    date_time_of_creation = dt.datetime.now()
    boxAssembler.create_box("Box Type", "Box description", "Box Position", user, date_time_of_creation)

    date_time_of_update = dt.datetime.now()

    boxChanger.update_box_status("AAAAAAA", "INACTIVE", user, date_time_of_update)

    expected_audit_trail = pd.DataFrame({
        'boxID': ['AAAAAAA', 'AAAAAAA'],
        'action': ['Create box', 'Box status changed'],
        'from_position': ['N/A', 'N/A'],
        'to_position': ['Box Position', 'N/A'],
        'username': ['username', 'username'],
        'date_time': [date_time_of_creation, date_time_of_update]
        })

    assert auditTrailTable.has_entries(expected_audit_trail)