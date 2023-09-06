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
    
    def get_docs(
            self,
            doc_id:int = None,
            doc_ids:list[int] = None,
            cond:dict = None
            ):
        """Get a list of all documents matching an id, list of ids, or condition"""
        # Empty initial document list
        doc_list = []

        # If one id was provided, return that document in a list
        if doc_id is not None:
            try:
                data = self.docs[doc_id]
            except KeyError:
                print(f'Document with ID {str(doc_id)} is not found')
            else:
                doc_list.append(Document(doc_id, data))
            return doc_list
        
        # If many ids were provided, return all documents for them in a list
        elif doc_ids is not None:
            for _doc_id in doc_ids:
                try:
                    data = self.docs[_doc_id]
                except ValueError:
                    print(f'Document with ID {str(_doc_id)} is not found')
                else:
                    doc_list.append(Document(_doc_id, data))
            return doc_list
        
        # If a condition was provided, return documents matching that condition in a list
        elif cond is not None:
            s_key, s_value = cond.popitem()
            for _doc_id, data in self.docs.items():
                if data.get(s_key, None) == s_value:
                    doc_list.append(Document(_doc_id, data))
            return doc_list
        
        # Otherwise return all documents in a list
        else:
            for _doc_id, data in self.docs.items():
                doc_list.append(Document(_doc_id, data))
            return doc_list

    def get_ids(self, cond:dict = None):
        """Get a list of all document ids in the collection"""
        id_list = []

        # If a condition was provided, return document ids matching that condition in a list
        if cond is not None:
            s_key, s_value = cond.popitem()
            for doc_id, data in self.docs.items():
                if data.get(s_key, None) == s_value:
                    id_list.append(doc_id)
            return id_list
        
        # Otherwise return all document ids in a list
        else:
            for doc_id in self.docs.keys(): 
                id_list.append(doc_id)
            return id_list

    def update(
            self,
            changes:dict,
            doc_id:int = None,
            doc_ids:list[int] = None,
            cond:dict = None
            ):
        """Update one or more documents based on document ids or a search using a dictionary of new or updated key value pairs"""
        update_count = 0

        # If an ID is given, check if it exists then update if it does
        if doc_id is not None:
            if doc_id not in self.docs.keys():
                print(f'Document with ID {str(doc_id)} is not found')
                return 0
            data = self.docs[doc_id]
            for key, value in changes.items():
                data[key] = value
            self.docs[doc_id] = data
            update_count += 1
        
        # If an ID list is given, check that they all exist, then update if they do
        elif doc_ids is not None:
            for _doc_id in doc_ids:
                if _doc_id not in self.docs.keys():
                    print(f'Document with ID {str(_doc_id)} is not found')
                    return 0
            for _doc_id in doc_ids:
                data = self.docs[_doc_id]
                for key, value in changes.items():
                    data[key] = value
                self.docs[_doc_id] = data
                update_count += 1

        # If a condition is given, find the IDs that fit it then update those
        elif cond is not None:
            _doc_ids = self.get_ids(cond)
            if len(_doc_ids) == 0:
                print("No documents found")
                return 0
            else:
                for _doc_id in _doc_ids:
                    data = self.docs[_doc_id]
                    for key, value in changes.items():
                        data[key] = value
                    self.docs[_doc_id] = data
                    update_count += 1
        
        # If nothing was given inform the user then exit
        else:
            print("No criteria provided")
            return 0

        # If none of the conditions returned 0, write the internal dictionary to file then return the number of updated docs
        self.storage.write(self.docs, self.file_path)
        return update_count

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

    test_one = test_coll.get_docs(doc_id=1)
    test_two = test_coll.get_docs(doc_ids=[1,3,4])
    test_three = test_coll.get_docs(cond={'two':2})
    test_four = test_coll.get_docs()
    print("one")
    for doc in test_one:
        print(doc)

    print("\ntwo")
    for doc in test_two:
        print(doc)
    print("\nthree")
    for doc in test_three:
        print(doc)
    print("\nfour")
    for doc in test_four:
        print(doc)