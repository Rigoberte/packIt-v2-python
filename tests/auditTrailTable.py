import pandas as pd
import datetime as dt

class AuditTrailTable:
    def __init__(self):
        self.entries = pd.DataFrame(columns=['item', 'action', 'from_position', 'to_position', 'user', 'date_time']) 

    def add_entry(self, item, action, from_position, to_position, user, date_time):
        self.__assert_is_not_empty_string__('item', item)
        self.__assert_is_not_empty_string__('action', action)
        self.__assert_is_not_empty_string__('from_position', from_position)
        self.__assert_is_not_empty_string__('to_position', to_position)
        self.__assert_is_not_empty_string__('user', user)
        self.__assert_is_a_datetime_value__(date_time)

        entry = pd.DataFrame({
                'item': [item],
                'action': [action],
                'from_position': [from_position],
                'to_position': [to_position],
                'user': [user],
                'date_time': [date_time]
                })

        self.entries = pd.concat([self.entries, entry], ignore_index=True)

    def has_entry_count(self, expected_count):
        return len(self.entries) == expected_count
    
    def has_entries(self, expected_entries):
        return self.entries.equals(expected_entries)
    
    def __assert_is_not_empty_string__(self, item_name, item):
        if type(item) is not str:
            raise ValueError(item_name + " must be string.")

        if item == '':
            raise ValueError(f'{item_name.capitalize()} must be a non-empty string.')
        
    def __assert_is_a_datetime_value__(self, date_time):
        if not isinstance(date_time, dt.datetime):
            raise ValueError('Date time must be a datetime object.')