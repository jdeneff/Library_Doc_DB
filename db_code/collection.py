import json
import os
from storage import JSONStorage

class Document(dict):
    """A document in the collection with an id and data in a dictionary"""
    def __init__(self, doc_id:int, data:dict):
        super().__init__(data)
        self.doc_id = doc_id
    
    def __str__(self):
        full_data = {self.doc_id:self}
        pretty = json.dumps(full_data, indent=2)
        return pretty


class Collection:
    def __init__(self, file_path:str):
        self.file_path = file_path
        self.storage = JSONStorage()
        
        # If the collection file does not exist, create it
        if not self.storage.exists(self.file_path):
            self.storage.jsonfile_create({}, self.file_path)
            self.docs = {}     # Empty docs dictionary
            self.next_id = 1   # ID numbers start at 1

        # If the collection file does exist, read it in
        else:
            raw_docs:dict = self.storage.read(self.file_path)
            self.docs:dict = {int(doc_id):doc for doc_id, doc in raw_docs.items()}
            # Calculate next ID number
            if self.docs == {}:
                self.next_id = 1
            else:
                max_id = max(int(i) for i in self.docs.keys())
                self.next_id = max_id + 1

    
    def insert(self, doc:dict):
        """Add a dictionary document to the collection with the next integer document id"""
        # Check document type, should only be document data in a dict
        if not isinstance(doc, dict):
            raise TypeError('Document is not a dict')
        
        # Get next document id and double check it doesn't already exist
        doc_id = self._get_next_id()
        if doc_id in self.docs.keys():
            raise ValueError(f'Document with ID {str(doc_id)} already exists')
        
        # Update internal dictionary and write to file
        self.docs[doc_id] = doc
        self.storage.write(self.docs, self.file_path)
        
    
    def get_doc(self, doc_id:int):
        """Get a single document based on its document id"""
        # First deal with given ID, if any
        if doc_id not in self.docs.keys():
            raise Exception(f'Document with ID {str(doc_id)} is not found')
        else:
            return Document(doc_id, self.docs[doc_id])
        
    def get_all(self):
        """Get a list of all document objects in the database"""
        docs = []
        for doc_id, doc in self.docs.items():
            docs.append(Document(doc_id, doc))
        return docs
    
    def search(self, s_key, s_value):
        """Get a list of all documents matching a given key-value pair"""  
        docs = []
        for doc_id, doc in self.docs.items():
            # Check if the doc has s_key, and if s_key if paired with s_value
            if doc.get(s_key, None) == s_value:
                docs.append(Document(doc_id, doc))
        return docs

    def get_ids(self):
        """Get a list of all document ids in the collection"""
        docs = []
        for key in self.docs.keys(): docs.append(key)
        return docs

    def update(self, doc_id:int, newdocs:dict):
        """Update a single dictionary document based on its document id using a dictionary of new or updated key value pairs"""
        # Generic updater function to be called by the collection update function
        def updater(coll:dict):
            doc:dict = coll[doc_id]
            for key, item in newdocs.items(): doc[key] = item
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
        if self.next_id is not None:
            next_id = self.next_id
            self.next_id += 1
            return next_id
        # If the file is just opened and is empty, start at 1
        if self.docs == {}:
            next_id = 1
        # If the file is just opened and has docs, find the highest key and use the next one
        else:
            max_id = max(int(i) for i in self.docs.keys())
            next_id = max_id + 1
        self.next_id = next_id +1
        return next_id
    
    def _update_collection(self, updater):
        # Update internally held dictionary
        updater(self.docs)
        # Serialize internal dictionary as json then write to the collection file
        self.storage.write(self.docs, self.file_path)

if __name__ == "__main__":
    test_coll = Collection('./test_coll.json')
    
    doc_one = {'one':'one', 'two':2, 'three':'trois'}
    doc_two = {'testing':'one, two, three'}

    test_query = test_coll.get(5)
    print(test_query)