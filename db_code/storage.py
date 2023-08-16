import os
import json

class JSONStorage:
    def __init__(self):
        pass

    def db_create(self, name:str, path:str):
        """
        Create an index file for a database if it does not exist yet
        """
        if not os.path.exists(path):
            base = {
                "name":name,
                "index":{}
            }
            ser_base = json.dumps(base)
            with open(path, "a") as f:
                f.write(ser_base)
        else:
            print(f"Error writing file to {path}")

    def db_delete(self, path:str):
        if os.path.exists(path):
            os.remove(path)
        else:
            print("Database not found")

    def coll_create(self, path:str):
        """
        Create a collection json file if it does not exist yet
        """
        if not os.path.exists(path):
            with open(path, "a") as f:
                f.write("{}")
        else:
            print(f"Error writing file to {path}")
    
    def coll_delete(self, path:str):
        if os.path.exists(path):
            os.remove(path)
        else:
            print("Collection not found")

    def read(self, path:str):
        # Read in from start of file, error if file is blank or not json formatted
        if os.path.exists(path):
            with open(path, "r+") as f:
                data = json.load(f)
            return data
        else:
            print("File not found")

    def write(self, path:str, data:dict):
        serialized = json.dumps(data, indent=4)
        if os.path.exists(path):
            with open(path, "r+") as f:
                f.seek(0)
                f.write(serialized)
                f.truncate()


if __name__=="__main__":
    tstor = JSONStorage()
    tstor.db_delete("./index.json")