import datetime as dt

from auditTrailTable import AuditTrailTable
from boxesTable import BoxesTable
from boxChanger import BoxChanger
from boxesBrowser import BoxesBrowser
from user import User
from boxAssembler import BoxAssembler

class Model:
    def __init__(self):
        self.auditTrailTable = AuditTrailTable()
        self.boxesTable = BoxesTable()
        self.boxChanger = BoxChanger(self.auditTrailTable, self.boxesTable)
        self.boxAssembler = BoxAssembler(self.auditTrailTable, self.boxesTable)
        self.boxesBrowser = BoxesBrowser(self.boxesTable)
        
    def create_box(self, box_type: str, description: str, position: str, user: User, datetime: dt.datetime = dt.datetime.now()) -> None:
        self.boxAssembler.create_box(box_type, description, position, user, datetime)

    def update_box_status(self, box_id: str, new_status: str, user: User, date_time: dt.datetime):
        self.boxChanger.update_box_status(box_id, new_status, user, date_time)

    def has_box_with_id(self, box_id: str) -> bool:
        return self.boxesBrowser.has_box_with_id(box_id)
    
    def filter_boxes_with(self, partial_box_id: str = '', box_type: str  = '', partial_box_description: str  = '', partial_box_position: str  = '', positionStatus: str = ''):
        return self.boxesBrowser.filter_boxes_with(partial_box_id, box_type, partial_box_description, partial_box_position, positionStatus)