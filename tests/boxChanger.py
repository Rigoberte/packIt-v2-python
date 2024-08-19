import datetime as dt

from boxesTable import BoxesTable
from auditTrailTable import AuditTrailTable
from user import User

class BoxChanger:
    def __init__(self, auditTrailTable: AuditTrailTable, boxesTable: BoxesTable):
        self.auditTrailTable = auditTrailTable
        self.boxesTable = boxesTable

    def update_box_status(self, box_id: str, new_status: str, user: User, date_time: dt.datetime):
        self.boxesTable.update_box_status(box_id, new_status)

        user.add_username_into_record_for_new_entry_of_audit_trail(
            self.auditTrailTable, box_id, "Box status changed", "N/A", "N/A", date_time
            )