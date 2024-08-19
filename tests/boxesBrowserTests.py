import pytest
import datetime as dt
import pandas as pd

from boxesTable import BoxesTable
from boxAssembler import BoxAssembler
from boxesBrowser import BoxesBrowser
from auditTrailTable import AuditTrailTable
from user import User

def create_a_boxes_table() -> BoxesTable:
    return BoxesTable()

def create_a_boxes_browser(boxesTable: BoxesTable) -> BoxesBrowser:
    return BoxesBrowser(boxesTable)

def create_a_box_assembler(boxesTable: BoxesTable) -> BoxAssembler:
    return BoxAssembler(AuditTrailTable(), boxesTable)

def setUp():
    boxesTable = create_a_boxes_table()
    boxesBrowser = create_a_boxes_browser(boxesTable)
    boxAssembler = create_a_box_assembler(boxesTable)
    user = User('username', 'name', 'last name', 'email', 'department', 'facility', dt.datetime.now())
    
    return boxesBrowser, boxAssembler, user

def test00_create_boxesBrowser() -> None:
    boxes_browser, _, _ = setUp()
    assert boxes_browser is not None

def test01_not_found_a_not_created_box() -> None:
    boxes_browser, _, _ = setUp()
    
    assert not boxes_browser.has_box_with_id('AAAAAAA')

def test02_found_a_created_box() -> None:
    boxes_browser, box_assembler, user = setUp()
    box_assembler.create_box('Box Type', 'Box Description', 'Box Position', user, dt.datetime.now())
    
    assert boxes_browser.has_box_with_id('AAAAAAA')

def test03_filter_boxes_with_partial_box_id() -> None:
    boxes_browser, box_assembler, user = setUp()
    box_assembler.create_box('Box Type', 'Box Description', 'Box Position', user, dt.datetime.now())
    box_assembler.create_box('Box Type', 'Box Description', 'Box Position', user, dt.datetime.now())
    
    expected = pd.DataFrame({'boxID': ['AAAAAAB'],
                            'box_status': ['Y'],
                            'box_type': ['Box Type'],
                            'box_description': ['Box Description'],
                            'box_position': ['Box Position'],
                            'position_status': ['ACTIVE']})
    
    assert boxes_browser.filter_boxes_with(partial_box_id='AAB').equals(expected)

def test04_filter_boxes_with_box_type() -> None:
    boxes_browser, box_assembler, user = setUp()
    box_assembler.create_box('Box Type', 'Box Description', 'Box Position', user, dt.datetime.now())
    box_assembler.create_box('Box Tyype', 'Box Description', 'Box Position', user, dt.datetime.now())
    
    expected = pd.DataFrame({'boxID': ['AAAAAAA'],
                            'box_status': ['Y'],
                            'box_type': ['Box Type'],
                            'box_description': ['Box Description'],
                            'box_position': ['Box Position'],
                            'position_status': ['ACTIVE']})
    
    assert boxes_browser.filter_boxes_with(box_type='Box Type').equals(expected)

def test05_filter_boxes_with_partial_box_description() -> None:
    boxes_browser, box_assembler, user = setUp()
    box_assembler.create_box('Box Type', 'Box Description', 'Box Position', user, dt.datetime.now())
    box_assembler.create_box('Box Type', 'Box Description 2', 'Box Position', user, dt.datetime.now())
    
    expected = pd.DataFrame({'boxID': ['AAAAAAA', 'AAAAAAB'],
                            'box_status': ['Y', 'Y'],
                            'box_type': ['Box Type', 'Box Type'],
                            'box_description': ['Box Description', 'Box Description 2'],
                            'box_position': ['Box Position', 'Box Position'],
                            'position_status': ['ACTIVE', 'ACTIVE']})
    
    assert boxes_browser.filter_boxes_with(partial_box_description='Descript').equals(expected)

def test06_filter_boxes_with_partial_box_position() -> None:
    boxes_browser, box_assembler, user = setUp()
    box_assembler.create_box('Box Type', 'Box Description', 'Box Position', user, dt.datetime.now())
    box_assembler.create_box('Box Type', 'Box Description', 'Box Position 2', user, dt.datetime.now())
    
    expected = pd.DataFrame({'boxID': ['AAAAAAA', 'AAAAAAB'],
                            'box_status': ['Y', 'Y'],
                            'box_type': ['Box Type', 'Box Type'],
                            'box_description': ['Box Description', 'Box Description'],
                            'box_position': ['Box Position', 'Box Position 2'],
                            'position_status': ['ACTIVE', 'ACTIVE']})
    
    assert boxes_browser.filter_boxes_with(partial_box_position='Position').equals(expected)

def test07_filter_boxes_with_position_status() -> None:
    boxes_browser, box_assembler, user = setUp()
    box_assembler.create_box('Box Type', 'Box Description', 'Box Position', user, dt.datetime.now())
    box_assembler.create_box('Box Type', 'Box Description', 'Box Position', user, dt.datetime.now())
    
    expected = pd.DataFrame(columns=['boxID', 'box_status', 'box_type', 'box_description', 'box_position', 'position_status'])

    assert boxes_browser.filter_boxes_with(positionStatus='INACTIVE').equals(expected)

def test08_filter_boxes_with_all_criteria() -> None:
    boxes_browser, box_assembler, user = setUp()
    box_assembler.create_box('Box Tyype', 'Box Description', 'Box Position', user, dt.datetime.now())
    box_assembler.create_box('Box Type', 'Box Description 2', 'Box Position', user, dt.datetime.now())
    box_assembler.create_box('Box Type', 'Box Description', 'Box Position 2', user, dt.datetime.now())
    box_assembler.create_box('Box Type', 'Box Description 2', 'Box Position 2', user, dt.datetime.now())
    
    expected = pd.DataFrame({'boxID': ['AAAAAAB'],
                            'box_status': ['Y'],
                            'box_type': ['Box Type'],
                            'box_description': ['Box Description 2'],
                            'box_position': ['Box Position'],
                            'position_status': ['ACTIVE']})
    
    assert boxes_browser.filter_boxes_with(partial_box_id='AAB', box_type='Box Type', partial_box_description='Descript', partial_box_position='Position').equals(expected)