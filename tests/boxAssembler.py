import datetime as dt

from box import Box
from user import User
from auditTrailTable import AuditTrailTable
from boxesTable import BoxesTable

class BoxAssembler:
    def __init__(self, audit_trail: AuditTrailTable, boxesTable: BoxesTable):
        self.audit_trail = audit_trail
        self.boxes = boxesTable
        self.counter_of_boxes = 0

    # Evaluation methods
    def has_box_count(self, count: int) -> bool:
        return self.counter_of_boxes == count
    
    def has_as_last_box_id(self, box_id: str) -> bool:
        return self.boxes.has_as_last_box_id(box_id)
    
    def has_audit_trail_count(self, count: int) -> bool:
        return self.audit_trail.has_entry_count(count)

    # Command methods
    def create_box(self, box_type: str, description: str, position: str, user: User, datetime: dt.datetime = dt.datetime.now()) -> None:
        boxID = self.__get_next_box_id__()
        box = Box(boxID, box_type, description, position)
        box.add_box_to_box_table(self.boxes)
        self.counter_of_boxes += 1

        user.add_username_into_record_for_new_entry_of_audit_trail(self.audit_trail, boxID, 'Create box', 'N/A', position, datetime)

    # Private methods
    def __get_code__(self, number: int):
        for i in range(7):
            number, remainder = divmod(number, 26)
            yield chr(65 + remainder)

    def __get_next_box_id__(self) -> str:
        return (''.join(self.__get_code__(self.counter_of_boxes)))[::-1]