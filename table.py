from storage import JSONStorage


class Document(dict):
    def __init_(self, value, doc_id):
        super().__init__(value)
        self._doc_id = doc_id

class Table:
    document_class = Document
    document_id_class = int

    def __init__(self, storage:JSONStorage, name:str) -> None:
        self._storage = storage
        self._name = name
        self._next_id = None

    def _read_table(self):
        tables = self._storage.read()
        if tables is None:
            return {}
        
        try:
            table = tables[self._name]
        except:
            return {}
        
        return table


if __name__=="__main__":
    test_storage = JSONStorage("./example.json")
    table1 = Table(test_storage, "table1")

    print(table1._read_table())