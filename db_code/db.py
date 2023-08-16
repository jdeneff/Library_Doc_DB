from storage import JSONStorage

class DocDB:
    def __init__(self) -> None:
        self._storage = JSONStorage()
        self._name = None
        self._dir_path = None
        self._next_id = None
        self._index = {}
    
    def create(self, name:str, dir_path:str):
        # Need to make it error when the file already exists - use return from storage
        self._name = name
        self._dir_path = dir_path
        file_path = self._dir_path + "/" + self._name + "_index.json"
        self._storage.db_create(self._name, file_path)
    
    def open(self, path:str):
        # Need to make it error when the file is not found - use return from storage
        data = self._storage.read(path)
        self._name = data["name"]
        self._index = data["index"]
        self._dir_path = path[0:path.rfind("/")+1]
    
if __name__ == "__main__":
    db = DocDB()
    db.create("test", "C:/Users/Admin/Jacob_Docs")
    db_two = DocDB()
    db_two.open("C:/Users/Admin/Jacob_Docs/test_index.json")
    print(db_two._name)
    print(db_two._index)
    print(db_two._dir_path)