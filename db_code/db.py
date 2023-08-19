import os
from storage import JSONStorage

class DocDB:
    def __init__(self) -> None:
        self._storage = JSONStorage()
        self._name = None

        self._file_name = None
        self._dir_name = None

        self._next_id = None
        self._collections = {}
    
    def create(self, name:str, dir_name:str):
        """Create a new database json file using the base format"""
        base = {
            "name":name,
            "collections":{},
            "indices":{}
        }

        file_name = name + "_db.json"
        if not self._storage.exists(dir_name, file_name):
            self._name = name
            self._dir_name = dir_name
            self._file_name = file_name
            self._storage.jsonfile_create(base, self._dir_name, self._file_name)
        else:
            print("File already exists with that name")
    
    def open(self, path:str):
        dir_name, file_name = os.path.split(path)
        if self._storage.exists(dir_name, file_name):
            data = self._storage.read(dir_name, file_name)
            if data is not None:
                self._name = data["name"]
                self._collections = data["collections"]
                self._dir_name = dir_name
                self._file_name = file_name
            else:
                print("Something went wrong loading the data")
        else:
            print("File does not exist")
    
if __name__ == "__main__":
    db = DocDB()
    db.create("test", "./")
    db2 = DocDB()
    db2.open("./test_db.json")