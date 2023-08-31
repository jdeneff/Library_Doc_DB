import os
import json

class JSONStorage:
    def __init__(self):
        pass

    def exists(self, file_path:str) -> bool:
        """Check if a file exists based on directory and file name"""
        if os.path.exists(file_path):
            return True
        else:
            return False

    def jsonfile_create(self, data:dict, file_path) -> bool:
        """Create a json file with some data if it does not exist already"""
        ser_data = json.dumps(data)
        if not os.path.exists(file_path):
            with open(file_path, "a") as f:
                f.write(ser_data)
            return True
        else:
            print(f"Error writing file to {file_path}")
            return False

    def read(self, file_path:str) -> dict:
        """Read from a json file and return an error if it does not exist or isn't json formatted"""
        if os.path.exists(file_path):
            with open(file_path, "r+") as f:
                try:
                    data = json.load(f)
                except:
                    print("Not json formatted")
                    return {}
            return data
        else:
            print("File not found")

    def write(self, data:dict, file_path) -> None:
        """Overwrite an existing json file then truncate to new length, if shorter than before"""
        serialized = json.dumps(data, indent=4)
        if os.path.exists(file_path):
            with open(file_path, "r+") as f:
                f.seek(0)
                f.write(serialized)
                f.truncate()


if __name__=="__main__":
    tstor = JSONStorage()
    tryto = tstor.jsonfile_create({},"./", "test.json")
    print(tryto)