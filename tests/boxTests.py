import pytest

from box import Box

def create_a_box(type: str = "aType", description: str = "aDescription", position: str = "aPosition") -> Box:
    return Box(type, description, position)

def test00_create_a_box() -> None:
    box = create_a_box()
    assert box is not None

def test01_new_boxes_has_initial_boxID() -> None:
    box = create_a_box()
    assert box.has_boxID('AAAAAAA')

def test02_new_boxes_starts_with_status_active() -> None:
    box = create_a_box()
    assert box.has_box_status('active')

def test03_new_boxes_starts_with_its_type() -> None:
    box = create_a_box('aType')
    assert box.has_type('aType')

def test04_new_boxes_starts_with_its_type_deny_other_types() -> None:
    box = create_a_box('aType')
    assert not box.has_type('anotherType')
    assert not box.has_type('')

def test05_new_boxes_cannot_starts_with_empty_type() -> None:
    with pytest.raises(ValueError, match="Type must be a non-empty string."):
        create_a_box('')

def test06_new_boxes_cannot_starts_with_non_string_type() -> None:
    with pytest.raises(ValueError, match="Type must be string."):
        create_a_box(1)

def test07_new_boxes_starts_with_its_description() -> None:
    box = create_a_box('aType', 'aDescription')
    assert box.has_description('aDescription')

def test08_new_boxes_starts_with_its_description_deny_other_descriptions() -> None:
    box = create_a_box('aType', 'aDescription')
    assert not box.has_description('anotherDescription')
    assert not box.has_description('')

def test09_new_boxes_cannot_starts_with_empty_description() -> None:
    with pytest.raises(ValueError, match="Description must be a non-empty string."):
        create_a_box('aType', '')

def test10_new_boxes_cannot_starts_with_non_string_description() -> None:
    with pytest.raises(ValueError, match="Description must be string."):
        create_a_box('aType', 1)

def test11_new_boxes_starts_on_its_position() -> None:
    box = create_a_box(position='aPosition')
    assert box.has_position('aPosition')

def test12_new_boxes_starts_on_its_position_deny_other_positions() -> None:
    box = create_a_box(position='aPosition')
    assert not box.has_position('anotherPosition')
    assert not box.has_position('')

def test13_new_boxes_starts_on_its_position_deny_empty_position() -> None:
    with pytest.raises(ValueError, match="Position must be a non-empty string."):
        create_a_box(position='')

def test14_new_boxes_starts_on_its_position_deny_non_string_position() -> None:
    with pytest.raises(ValueError, match="Position must be string."):
        create_a_box(position=1)

def test15_new_boxes_starts_with_active_position_status() -> None:
    box = create_a_box()
    assert box.has_position_status('active')

def test16_change_box_status_to_inactive() -> None:
    box = create_a_box()
    box.change_box_status('inactive')
    assert box.has_box_status('inactive')
    assert not box.has_box_status('active')

def test17_change_box_status_to_active() -> None:
    box = create_a_box()
    box.change_box_status('inactive')
    box.change_box_status('active')
    assert box.has_box_status('active')
    assert not box.has_box_status('inactive')

def test18_change_box_status_to_unknown_status() -> None:
    box = create_a_box()
    with pytest.raises(ValueError, match="Unknown box status."):
        box.change_box_status('unknown')

def test19_change_box_position() -> None:
    box = create_a_box()
    box.change_position('newPosition')
    assert box.has_position('newPosition')
    assert not box.has_position('aPosition')

def test20_change_box_position_to_empty_string() -> None:
    box = create_a_box()
    with pytest.raises(ValueError, match="Position must be a non-empty string."):
        box.change_position('')

def test21_change_box_position_to_non_string() -> None:
    box = create_a_box()
    with pytest.raises(ValueError, match="Position must be string."):
        box.change_position(1)

def test22_change_box_position_status() -> None:
    box = create_a_box()
    box.change_position_status('inactive')
    assert box.has_position_status('inactive')
    assert not box.has_position_status('active')

def test23_change_box_position_status_to_active() -> None:
    box = create_a_box()
    box.change_position_status('inactive')
    box.change_position_status('active')
    assert box.has_position_status('active')
    assert not box.has_position_status('inactive')

def test24_change_box_position_status_to_unknown_status() -> None:
    box = create_a_box()
    with pytest.raises(ValueError, match="Unknown position status."):
        box.change_position_status('unknown')