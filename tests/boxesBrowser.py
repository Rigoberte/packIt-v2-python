from boxesTable import BoxesTable
import pandas as pd

class BoxesBrowser:
    def __init__(self, boxesTable: BoxesTable) -> None:
        self.boxesTable = boxesTable

    # Evaluation methods
    def has_box_with_id(self, box_id: str) -> bool:
        return self.boxesTable.has_box_with_id(box_id)
    
    # Command methods
    def filter_boxes_with(self,
                        partial_box_id: str = '',
                        box_type: str  = '',
                        partial_box_description: str  = '',
                        partial_box_position: str  = '',
                        positionStatus: str = ''
                        ) -> pd.DataFrame:
            
            return self.boxesTable.filter_boxes_with(partial_box_id, box_type, partial_box_description, partial_box_position, positionStatus)