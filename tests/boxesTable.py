import pandas as pd

class BoxesTable:
    def __init__(self):
        self.boxes = pd.DataFrame(columns=['boxID', 'box_status', 'box_type', 'box_description', 'box_position', 'position_status']) 

    def add_entry(self, boxID, boxStatus, boxType, boxDescription, boxPosition, positionStatus):
        self.__assert_is_not_empty_string__('boxID', boxID)
        self.__assert_is_not_empty_string__('Box Type', boxType)
        self.__assert_is_not_empty_string__('Box Description', boxDescription)
        self.__assert_is_not_empty_string__('Box Position', boxPosition)

        entry = pd.DataFrame({'boxID': [boxID], 
                            'box_status': [boxStatus], 
                            'box_type': [boxType], 
                            'box_description': [boxDescription], 
                            'box_position': [boxPosition], 
                            'position_status': [positionStatus]})

        self.boxes = pd.concat([self.boxes, entry], ignore_index=True)

    # Evaluation methods
    def has_entry_count(self, expected_count):
        return len(self.boxes) == expected_count
    
    def has_entries(self, expected_entries):
        return self.boxes.equals(expected_entries)
    
    def has_as_last_box_id(self, box_id: str) -> bool:
        if len(self.boxes) == 0:
            return False
        
        return self.boxes.iloc[-1]['boxID'] == box_id
    
    def has_box_with_id(self, box_id: str) -> bool:
        return box_id in self.boxes.boxID.to_list()
    
    def check_box_status(self, box_id: str, expected_status: str) -> bool:
        return self.boxes[self.boxes['boxID'] == box_id]['box_status'].values[0] == expected_status
    
    # Command methods
    def filter_boxes_with(self, 
                        partial_box_id: str = '',
                        box_type: str = '',
                        partial_box_description: str = '',
                        partial_box_position: str = '',
                        positionStatus: str = '') -> pd.DataFrame:
        filtered = self.boxes

        if partial_box_id != '':
            filtered = filtered[filtered['boxID'].str.contains(partial_box_id)]

        if box_type != '':
            filtered = filtered[filtered['box_type'] == box_type]

        if partial_box_description != '':
            filtered = filtered[filtered['box_description'].str.contains(partial_box_description)]

        if partial_box_position != '':
            filtered = filtered[filtered['box_position'].str.contains(partial_box_position)]

        if positionStatus != '':
            filtered = filtered[filtered['position_status'] == positionStatus]

        return filtered.reset_index(drop=True)
    
    def update_box_status(self, box_id: str, new_status: str):
        self.__assert_is_not_empty_string__('Box ID', box_id)

        if new_status != "ACTIVE" and new_status != "INACTIVE":
            raise ValueError("Unknown position status.")

        if self.boxes.loc[self.boxes['boxID'] == box_id, 'box_status'].empty:
            raise ValueError(f'Box with ID {box_id} not found.')
        
        self.boxes.loc[self.boxes['boxID'] == box_id, 'box_status'] = new_status

    # Private methods
    def __assert_is_not_empty_string__(self, item_name, item):
        if type(item) is not str:
            raise ValueError(item_name + " must be string.")

        if item == '':
            raise ValueError(f'{item_name.capitalize()} must be a non-empty string.')