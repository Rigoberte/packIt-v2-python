import pytest
import datetime

from user import User

def create_a_user(username: str="username", name: str="name",
                lastname: str="lastname", email: str="email",
                userDepartment: str="userDepartment", facility: str="facility",
                lastPasswordChangeDate=datetime.datetime(2024, 1, 1)) -> User:
    return User(username, name, lastname, email, userDepartment, facility, lastPasswordChangeDate)

def test00_create_a_user():
    test_user = create_a_user()
    assert test_user is not None

def test01_new_users_starts_with_username():
    test_user = create_a_user(username="username1")
    assert test_user.has_username("username1")

def test02_new_users_deny_another_username():
    test_user = create_a_user(username="username1")
    assert not test_user.has_username("username2")

def test03_new_users_with_empty_username():
    with pytest.raises(ValueError , match="Username must be a non-empty string"):
        create_a_user(username="")

def test04_new_users_are_active():
    test_user = create_a_user()
    assert test_user.has_user_status("active")

def test05_new_users_are_not_inactive():
    test_user = create_a_user()
    assert not test_user.has_user_status("inactive")

def test06_new_users_assert_name_is_valid():
    test_user = create_a_user(name="name1")
    assert test_user.has_name("name1")

def test07_new_users_deny_another_name():
    test_user = create_a_user(name="name1")
    assert not test_user.has_name("name2")

def test08_new_users_with_empty_name():
    with pytest.raises(ValueError , match="Name must be a non-empty string"):
        create_a_user(name="")

def test09_new_users_assert_lastname_is_valid():
    test_user = create_a_user(lastname="lastname1")
    assert test_user.has_lastname("lastname1")

def test10_new_users_deny_another_lastname():
    test_user = create_a_user(lastname="lastname1")
    assert not test_user.has_lastname("lastname2")

def test11_new_users_with_empty_lastname():
    with pytest.raises(ValueError , match="Lastname must be a non-empty string"):
        create_a_user(lastname="")

def test12_new_users_assert_email_is_valid():
    test_user = create_a_user(email="email1")
    assert test_user.has_email("email1")

def test13_new_users_deny_another_email():
    test_user = create_a_user(email="email1")
    assert not test_user.has_email("email2")

def test14_new_users_with_empty_email():
    with pytest.raises(ValueError , match="Email must be a non-empty string"):
        create_a_user(email="")

def test15_new_users_starts_with_zero_failed_login_attempts():
    test_user = create_a_user()
    assert test_user.has_failed_login_attempts(0)

def test16_new_users_starts_with_zero_failed_login_attempts_deny_another():
    test_user = create_a_user()
    assert not test_user.has_failed_login_attempts(1)

def test17_new_users_assert_user_department_is_valid():
    test_user = create_a_user(userDepartment="userDepartment1")
    assert test_user.has_department("userDepartment1")

def test18_new_users_deny_another_user_department():
    test_user = create_a_user(userDepartment="userDepartment1")
    assert not test_user.has_department("userDepartment2")

def test19_new_users_with_empty_user_department():
    with pytest.raises(ValueError , match="User Department must be a non-empty string"):
        create_a_user(userDepartment="")

def test20_new_users_assert_facility_is_valid():
    test_user = create_a_user(facility="facility1")
    assert test_user.has_facility("facility1")

def test21_new_users_deny_another_facility():
    test_user = create_a_user(facility="facility1")
    assert not test_user.has_facility("facility2")

def test22_new_users_with_empty_facility():
    with pytest.raises(ValueError , match="Facility must be a non-empty string"):
        create_a_user(facility="")

def test23_increase_failed_login_attempts():
    test_user = create_a_user()
    test_user.increase_failed_login_attempts()
    assert test_user.has_failed_login_attempts(1)
    test_user.increase_failed_login_attempts()
    assert test_user.has_failed_login_attempts(2)

def test24_reset_failed_login_attempts():
    test_user = create_a_user()
    test_user.increase_failed_login_attempts()
    test_user.increase_failed_login_attempts()
    test_user.reset_failed_login_attempts()
    assert test_user.has_failed_login_attempts(0)

def test25_new_users_starts_with_last_password_change_date():
    test_user = create_a_user(lastPasswordChangeDate=datetime.datetime(2024, 1, 1))
    assert test_user.has_last_password_change_date(datetime.datetime(2024, 1, 1))

def test26_new_users_starts_with_last_password_change_date_deny_another():
    test_user = create_a_user(lastPasswordChangeDate=datetime.datetime(2024, 1, 1))
    assert not test_user.has_last_password_change_date(datetime.datetime(2024, 1, 2))

def test27_new_users_starts_with_empty_last_password_change_date():
    with pytest.raises(ValueError , match="Last Password Change Date must be a datetime value"):
        create_a_user(lastPasswordChangeDate="")

def test28_when_reset_failed_login_attempts_lastPasswordChangeDate_is_updated():
    test_user = create_a_user()
    test_user.reset_failed_login_attempts()
    assert test_user.has_last_password_change_date(datetime.datetime.today())

def test29_change_user_status_from_active_to_inactive():
    test_user = create_a_user()
    test_user.change_user_status("inactive")
    assert test_user.has_user_status("inactive")

def test30_change_user_status_from_active_to_inactive_deny_another():
    test_user = create_a_user()
    test_user.change_user_status("inactive")
    test_user.change_user_status("active")
    assert test_user.has_user_status("active")

def test31_change_user_status_to_unknown_status():
    test_user = create_a_user()
    with pytest.raises(ValueError , match="User Status must be either 'active' or 'inactive'."):
        test_user.change_user_status("unknown")

def test32_change_user_status_to_empty_status():
    test_user = create_a_user()
    with pytest.raises(ValueError , match="User Status must be either 'active' or 'inactive'."):
        test_user.change_user_status("")

def test33_change_user_status_to_none_status():
    test_user = create_a_user()
    with pytest.raises(ValueError , match="User Status must be either 'active' or 'inactive'."):
        test_user.change_user_status(None)

def test34_change_user_department():
    test_user = create_a_user()
    test_user.change_user_department("newUserDepartment")
    assert test_user.has_department("newUserDepartment")

def test35_change_user_department_to_empty_department():
    test_user = create_a_user()
    with pytest.raises(ValueError , match="User Department must be a non-empty string"):
        test_user.change_user_department("")

def test36_change_facility():
    test_user = create_a_user()
    test_user.change_facility("newFacility")
    assert test_user.has_facility("newFacility")

def test37_change_facility_to_empty_facility():
    test_user = create_a_user()
    with pytest.raises(ValueError , match="Facility must be a non-empty string"):
        test_user.change_facility("")