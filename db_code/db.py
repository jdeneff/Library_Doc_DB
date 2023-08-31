import os
from storage import JSONStorage
from collection import Collection

class DocDB:
    def __init__(self, file_path:str):
        self._storage = JSONStorage()
        self._file_path = file_path
        self._coll_paths = {}   # Collection paths from file
        self._collections = {}  # Collection objects

        # If the database file does not exist, create it
        if not self._storage.exists(file_path):
            self._storage.jsonfile_create({}, self._file_path)

        # If the database file does exist, read it and create the collection objects for it
        else:
            self._coll_paths = self._storage.read(self._file_path)
            for coll_id, coll_path in self._coll_paths.items():
                collection = Collection(coll_path, self._storage)
                self._collections[str(coll_id)] = collection
    
    def add_collection(self, coll_name):
        """
        Create a single collection including the path reference, object, and file; then write the database.
        """
        if coll_name not in self._coll_paths.keys():
            dir_path = os.path.dirname(self._file_path)
            coll_path = os.path.join(dir_path, f"{coll_name}.json")
            if not self._storage.exists(coll_path):
                self._storage.jsonfile_create({}, coll_path)
                self._coll_paths[coll_name] = coll_path
                self._collections[coll_name] = Collection(coll_path, self._storage)
                self._storage.write(self._coll_paths, self._file_path)
            else:
                print("File already exists")
        else:
            print("Collection already exists")

    def drop_collection(self, coll_name:str):
        """
        Delete a single collection including the path reference, object, and file; then write the database.
        """
        if coll_name in self._coll_paths.keys():
            dir_path = os.path.dirname(self._file_path)
            coll_path = os.path.join(dir_path, f"{coll_name}.json")
            os.remove(coll_path)
            self._coll_paths.pop(coll_name)
            self._collections.pop(coll_name)
            self._storage.write(self._coll_paths, self._file_path)
        else:
            print("Collection not in database")

    def drop_all_collections(self):
        """
        Delete all collections in the database.
        """
        for coll_name in self._coll_paths.keys():
            self.drop_collection(coll_name)


if __name__ == "__main__":
    db = DocDB("test_new_db/test_db.json")
    # db.add_collection("one")
    # db.add_collection("two")
    print(db._coll_paths)
    print(db._collections)
    db.drop_collection("one")
    print(db._coll_paths)
    print(db._collections)