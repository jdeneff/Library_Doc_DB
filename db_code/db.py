from storage import JSONStorage

class DocDB:
    def __init__(self, path:str) -> None:
        self._storage = JSONStorage(path)
        self._next_id = None
    
    def insert(self, data:dict):
        doc_id = self._get_next_id()
        def updater(db:dict):
            db[doc_id] = data

    def _get_next_id(self):
        db:dict = self._read_db()

        if self._next_id is not None:
            next_id = self._next_id
        elif db == {}:
            next_id = 1
        else:
            max_id = max(int(i) for i in db.keys())
            next_id = max_id + 1

        self._next_id = next_id +1
        return next_id
    
    def _update_shelf(self, updater):
        # Read in from JSON
        raw_db:dict = self._read_db()
        # Convert to form expected by db
        db = {int(doc_id):doc for doc_id, doc in raw_db.items()}
        # Update then convert back to form for JSON
        updater(db)
        new_db = {str(doc_id):doc for doc_id, doc in db.items()}
        # Write to storage file
        self._storage.write(db)

    def _read_db(self):
        return self._storage.read()
