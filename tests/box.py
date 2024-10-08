from documentsTable import DocumentsTable

class Box():
    def __init__(self, boxID: str, aType: str, aDescription: str, aPosition: str) -> None:
        self.__asserts_for_non_empty_string__("Box ID", boxID)
        self.__assert_type_is_valid__(aType)
        self.__assert_description_is_valid__(aDescription)
        self.__assert_position_is_valid__(aPosition)

        self.boxID = boxID
        self.type = aType
        self.boxStatus = "Y"
        self.description = aDescription
        self.position = aPosition
        self.positionStatus = "ACTIVE"
        self.inventoryTable = DocumentsTable()

    def has_boxID(self, aBoxID: str) -> bool:
        return self.boxID == aBoxID
    
    def has_box_status(self, aStatus: str) -> bool:
        return self.boxStatus == aStatus
    
    def has_type(self, aType: str) -> bool:
        return self.type == aType
    
    def has_description(self, aDescription: str) -> bool:
        return self.description == aDescription
    
    def has_position(self, aPosition: str) -> bool:
        return self.position == aPosition
    
    def has_position_status(self, aPositionStatus: str) -> bool:
        return self.positionStatus == aPositionStatus
    
    def change_box_status(self, aNewStatus: str) -> None:
        if aNewStatus != "ACTIVE" and aNewStatus != "INACTIVE":
            raise ValueError("Unknown box status.")

        self.boxStatus = aNewStatus

    def change_position(self, aNewPosition: str) -> None:
        self.__assert_position_is_valid__(aNewPosition)

        self.position = aNewPosition

    def change_position_status(self, aNewPositionStatus: str) -> None:
        if aNewPositionStatus != "ACTIVE" and aNewPositionStatus != "INACTIVE":
            raise ValueError("Unknown position status.")

        self.positionStatus = aNewPositionStatus

    def has_inventory(self, anInventory: set) -> bool:
        return self.inventoryTable.check_inventory_of_box(anInventory, self.boxID)
    
    def add_to_inventory(self, aDocument: str) -> None:
        self.__asserts_for_non_empty_string__("Document", aDocument)

        self.inventoryTable.add_entry(aDocument, self.boxID)

    def remove_from_inventory(self, aDocument: str) -> None:
        self.inventoryTable.remove_entry(aDocument)

    def has_inventory_size(self, expected_count) -> bool:
        return self.inventoryTable.has_entry_count(expected_count)

    def add_box_to_box_table(self, aBoxesTable) -> None:
        aBoxesTable.add_entry(self.boxID, self.boxStatus, self.type, self.description, self.position, self.positionStatus)

    def __asserts_for_non_empty_string__(self, aValueName: str, aValue) -> None:
        if type(aValue) is not str:
            raise ValueError(aValueName + " must be string.")
        
        if aValue == "":
            raise ValueError(aValueName + " must be a non-empty string.")
    
    def __assert_type_is_valid__(self, aType) -> None:
        self.__asserts_for_non_empty_string__("Type", aType)
        
    def __assert_description_is_valid__(self, aDescription) -> None:
        self.__asserts_for_non_empty_string__("Description", aDescription)
        
    def __assert_position_is_valid__(self, aPosition) -> None:
        self.__asserts_for_non_empty_string__("Position", aPosition)