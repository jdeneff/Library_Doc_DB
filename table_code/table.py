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

    def insert(self, document:dict):
        table = self._read_table()
        doc_id = self._get_next_id()
        
        def updater(table:dict):
            table[doc_id] = document
        self._update_table(updater)
    
    def update(self, doc_id, data):
        table = self._read_table()
        

    def _update_table(self, update_func):
        tables = self._storage.read()
        if tables is None:
            tables = {}

        try:
            raw_table = tables[self._name]
        except KeyError:
            raw_table = {}

        table = {self.document_id_class(doc_id): doc for doc_id, doc in raw_table.items()}
        update_func(table)

        tables[self._name] = {str(doc_id):doc for doc_id, doc in table.items()}
        self._storage.write(tables)


    def _read_table(self):
        tables = self._storage.read()
        if tables is None:
            return {}
        try:
            table = tables[self._name]
        except:
            return {}
        return table

    def _get_next_id(self):
        table = self._read_table()

        if not table:
            next_id = 1
            return next_id
        else:
            max_id = max(self.document_id_class(i) for i in table.keys())
            next_id = max_id + 1
            return next_id

if __name__=="__main__":
    test_storage = JSONStorage("./blank.json")
    table1 = Table(test_storage, "table1")

    print(table1._read_table())
    print(table1._get_next_id())

    table1.insert({
            "doc": 2,
            "value": "blue"
        })
    
    print(table1._read_table())