from storage import JSONStorage

class DocDB:
    def __init__(self, path:str) -> None:
        self._storage = JSONStorage(path)
        self._next_id = None
    
    def insert(self, data:dict):
        """
        Get a new document id then call the updater to add the new document in.
        Should I check for uniqueness of id or document?
        """
        doc_id = self._get_next_id()
        def updater(db:dict):
            db[doc_id] = data
        self._update_db(updater)

    def get(self, doc_id:int):
        db:dict = self._read_db()
        if str(doc_id) in db.keys():
            return db[str(doc_id)]
        else:
            print("No such document")
    
    def get_all(self):
        db:dict = self._read_db()
        docs = []
        for key in db.keys(): docs.append(key)
        return docs
    
    def update(self, doc_id:int, new_data:dict):
        def updater(db:dict):
            doc:dict = db[doc_id]
            for key, item in new_data.items(): doc[key] = item
            db[doc_id] = doc
        self._update_db(updater)

    def delete(self, doc_id):
        def updater(db:dict):
            db.pop(doc_id)
        self._update_db(updater)

    def _get_next_id(self):
        db:dict = self._read_db()

        if self._next_id is not None:
            next_id = self._next_id
            self._next_id = next_id +1
            return next_id
        
        if db == {}:
            next_id = 1
        else:
            max_id = max(int(i) for i in db.keys())
            next_id = max_id + 1
        self._next_id = next_id +1
        return next_id
    
    def _update_db(self, updater):
        # Read in from JSON
        raw_db:dict = self._read_db()
        # Convert to form expected by db
        db = {int(doc_id):doc for doc_id, doc in raw_db.items()}
        # Update then convert back to form for JSON
        updater(db)
        new_db = {str(doc_id):doc for doc_id, doc in db.items()}
        # Write to storage file
        self._storage.write(new_db)

    def _read_db(self):
        return self._storage.read()
