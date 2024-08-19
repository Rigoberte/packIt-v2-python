import pandas as pd

class DocumentsTable:
    def __init__(self):
        self.documentsTable = pd.DataFrame(columns=['documentID', 'document_status', 'boxID']) 

    # Evaluation methods
    def has_entry_count(self, expected_count):
        return len(self.documentsTable) == expected_count
    
    def has_entries(self, expected_entries):
        return self.documentsTable.equals(expected_entries)
    
    def check_inventory_of_box(self, inventory, boxID):
        return set(self.documentsTable[
            (self.documentsTable.boxID == boxID) & 
            (self.documentsTable.document_status == '1')
            ].documentID.to_list()) == inventory
    
    # Command methods
    def add_entry(self, documentID, boxID):
        self.__assert_is_not_empty_string__('documentID', documentID)
        self.__assert_is_not_empty_string__('boxID', boxID)

        if documentID in self.documentsTable[
            (self.documentsTable.documentID == documentID) & 
            (self.documentsTable.document_status == '1')
            ].documentID.to_list():
            return

        entry = pd.DataFrame({'documentID': [documentID], 
                            'document_status': ['1'], 
                            'boxID': [boxID]})

        self.documentsTable = pd.concat([self.documentsTable, entry], ignore_index=True)

    def remove_entry(self, documentID):
        self.documentsTable = self.documentsTable[self.documentsTable.documentID != documentID]

    def find_document(self, documentID):
        return self.documentsTable[self.documentsTable.documentID == documentID]

    # Private methods
    def __assert_is_not_empty_string__(self, item_name, item):
        if type(item) is not str:
            raise ValueError(item_name + " must be string.")

        if item == '':
            raise ValueError(f'{item_name.capitalize()} must be a non-empty string.')