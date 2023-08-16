import json
from storage import JSONStorage

class Collection:
    def __init__(self, name:str, path:str, storage:JSONStorage):
        self._name = name
        self._path = path
        self._storage = storage
        self._next_id = None

        raw_data:dict = self._storage.read(path)
        self.data = {int(doc_id):doc for doc_id, doc in raw_data.items()}
    
    def insert(self, doc:dict):
        """Add a dictionary document to the collection with the next integer document id"""
        doc_id = self._get_next_id()
        # Generic updater function to be called by the collection update function
        def updater(coll:dict):
            coll[doc_id] = doc
        self._update_collection(updater)
    
    def get(self, doc_id:int):
        """Get a single document based on its document id and return it as a dictionary"""
        if doc_id in self.data.keys():
            return self.data[doc_id]
        else:
            print("No such document")
        # Note, would be good to implement a document class to extend function

    def get_ids(self):
        """Get a list of all document ids in the collection"""
        docs = []
        for key in self.data.keys(): docs.append(key)
        return docs

    def update(self, doc_id:int, new_data:dict):
        """Update a single dictionary document based on its document id using a dictionary of new or updated key value pairs"""
        # Generic updater function to be called by the collection update function
        def updater(coll:dict):
            doc:dict = coll[doc_id]
            for key, item in new_data.items(): doc[key] = item
            coll[doc_id] = doc
        self._update_collection(updater)
    
    def delete(self, doc_id):
        """Delete a single dictionary document based on its document id"""
        # Generic updater function to be called by the collection update function
        def updater(coll:dict):
            coll.pop(doc_id)
        self._update_collection(updater)

    def _get_next_id(self):
        """Get the next document id for indexing"""
        # If the internal counter already has a next id, use that and then increment it
        if self._next_id is not None:
            next_id = self._next_id
            self._next_id += 1
            return next_id
        # If the file is just opened and is empty, start at 1
        if self.data == {}:
            next_id = 1
        # If the file is just opened and has data, find the highest key and use the next one
        else:
            max_id = max(int(i) for i in self.data.keys())
            next_id = max_id + 1
        self._next_id = next_id +1
        return next_id
    
    def _update_collection(self, updater:function):
        # Update internally held dictionary
        updater(self.data)
        # Serialize internal dictionary as json then write to the collection file
        serialized = json.dumps(self.data)
        self._storage.write(self._path, serialized)