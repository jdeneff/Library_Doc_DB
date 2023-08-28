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
            self._storage.jsonfile_create(
                {
                "collections":{}
                },
                self._file_path
            )
        # If the database file does exist, read it and create the collection objects for it
        else:
            data = self._storage.read(self._file_path)
            self._coll_paths:dict = data["collections"]
            for coll_id, coll_path in self._coll_paths.items():
                collection = Collection(coll_path, self._storage)
                self._collections[str(coll_id)] = collection
    
    def add_collection(self, coll_name):
        if coll_name not in self._coll_paths.keys():
            dir_path = os.path.dirname(self._file_path)
            coll_path = os.path.join(dir_path, f"{coll_name}.json")
            if not self._storage.exists(coll_path):
                self._storage.jsonfile_create({}, coll_path)
                self._coll_paths[coll_name] = coll_path
                self._collections[coll_name] = Collection(coll_path, self._storage)
            else:
                print("File already exists")
        else:
            print("Collection already exists")

    def read_collections(self):
        pass

    def drop_collection(self):
        pass

    def drop_all_collections(self):
        pass


if __name__ == "__main__":
    pass