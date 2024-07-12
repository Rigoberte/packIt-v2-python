import datetime

class user:
    def __init__(self, username:str, name: str, lastname: str, email: str, userDepartment: str, facility: str, lastPasswordChangeDate: datetime.datetime) -> None:
        self.__assert_username_is_valid__(username)
        self.__assert_name_is_valid__(name)
        self.__assert_lastname_is_valid__(lastname)
        self.__assert_email_is_valid__(email)
        self.__asserts_userDepartment_is_valid__(userDepartment)
        self.__asserts_facility_is_valid__(facility)
        self.__asserts_last_password_change_date_is_valid__(lastPasswordChangeDate)
        
        self.username = username
        self.userStatus = "active"
        self.name = name
        self.lastname = lastname
        self.email = email
        self.failedLoginAttempts = 0
        self.lastPasswordChangeDate = lastPasswordChangeDate
        self.userDepartment = userDepartment
        self.facility = facility

    # Evaluate
    def has_username(self, username: str) -> bool:
        return self.username == username
    
    def has_user_status(self, status: str) -> bool:
        return self.userStatus == status
    
    def has_name(self, name: str) -> bool:
        return self.name == name
    
    def has_lastname(self, lastname: str) -> bool:
        return self.lastname == lastname
    
    def has_email(self, email: str) -> bool:
        return self.email == email
    
    def has_failed_login_attempts(self, attempts: int) -> bool:
        return self.failedLoginAttempts == attempts
    
    def has_department(self, department: str) -> bool:
        return self.userDepartment == department
    
    def has_facility(self, facility: str) -> bool:
        return self.facility == facility
    
    def has_last_password_change_date(self, date: datetime.datetime) -> bool:
        return self.lastPasswordChangeDate == date

    # Methods
    def increase_failed_login_attempts(self) -> None:
        self.failedLoginAttempts += 1

    def reset_failed_login_attempts(self) -> None:
        self.failedLoginAttempts = 0
        self.lastPasswordChangeDate = datetime.datetime.today()
    
    def change_user_status(self, status: str) -> None:
        if status != "active" and status != "inactive":
            raise ValueError("User Status must be either 'active' or 'inactive'.")

        self.userStatus = status

    def change_user_department(self, department: str) -> None:
        self.__asserts_userDepartment_is_valid__(department)
        self.userDepartment = department

    def change_facility(self, facility: str) -> None:
        self.__asserts_facility_is_valid__(facility)
        self.facility = facility

    def __asserts_for_non_empty_string__(self, aValueName: str, aValue) -> None:
        if aValue == "":
            raise ValueError(aValueName + " must be a non-empty string.")
        
    def __assert_username_is_valid__(self, aUsername: str) -> None:
        self.__asserts_for_non_empty_string__("Username", aUsername)

    def __assert_name_is_valid__(self, aName: str) -> None:
        self.__asserts_for_non_empty_string__("Name", aName)

    def __assert_lastname_is_valid__(self, aLastname: str) -> None:
        self.__asserts_for_non_empty_string__("Lastname", aLastname)

    def __assert_email_is_valid__(self, aEmail: str) -> None:
        self.__asserts_for_non_empty_string__("Email", aEmail)

    def __asserts_userDepartment_is_valid__(self, aUserDepartment: str) -> None:
        self.__asserts_for_non_empty_string__("User Department", aUserDepartment)

    def __asserts_facility_is_valid__(self, aFacility: str) -> None:
        self.__asserts_for_non_empty_string__("Facility", aFacility)

    def __asserts_last_password_change_date_is_valid__(self, aLastPasswordChangeDate: datetime.datetime) -> None:
        if aLastPasswordChangeDate == "":
            raise ValueError("Last Password Change Date must be a datetime value.")