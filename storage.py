import os
import json


def touch(path:str):
    """
    Create a file if it does not exist yet
    """
    if not os.path.exists(path):
        with open(path, "a"):
            pass


class JSONStorage:
    def __init__(self, path:str, access_mode="r+"):
        # Open for read/write, create file if it doesn't exist, 
        self._mode = access_mode
        touch(path)
        self._handle = open(path, self._mode)

    def read(self):
        # Read in from start of file, error if file is blank or not json formatted
        self._handle.seek(0)
        return json.load(self._handle)

    def write(self, data:dict):
        # Write from start of file using json formatter
        self._handle.seek(0)
        serialized = json.dumps(data, indent=4)
        self._handle.write(serialized)
        # Flush file buffer, then force write to ensure write worked without closing
        self._handle.flush()
        os.fsync(self._handle.fileno())
        # Truncate in case file got shorter
        self._handle.truncate()

    def close(self):
        self._handle.close()


if __name__=="__main__":
    test_stor = JSONStorage("./blank.json")
    print(test_stor.read())

    example = {
        "0":{
            "doc":0,
            "value": True
        },
        "1":{
            "doc":1,
            "value": False
        }
    }

    test_stor.write(example)

    print(test_stor.read())

    test_stor.close()