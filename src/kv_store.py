import os
import json
import uuid

class KVStore:
    

    def __init__(self, name:str = None, id:uuid = None, storage:dict = None):
        self.__name = name
        if id is None:
            self.__id = uuid.uuid4()
            self.__storage = {}
            self.__keys = []
            self.__values = []
        else:
            self.__id = id
            self.__storage = storage
            self.__keys = list(storage.keys())
            self.__values = list(storage.values())


    @classmethod
    def new_instance(cls, name:str):
        if name is None:
            raise Exception("Name must not be None.")
        return cls(name=name)


    @classmethod
    def from_file(cls, path:str):
        if path is None:
            raise Exception("Path must not be None.")
        if os.path.exists(path) and os.path.isfile(path):
            with open(path, "r") as file:
                data = json.load(file)
                return cls(name=data["name"], id=uuid.UUID(data["id"]), storage=data["storage"])
        else:
            raise FileNotFoundError(f"No such file or directory: '{path}'")
        
    
    @classmethod
    def retreive_name(cls, path:str) -> str:
        if path is None:
            raise Exception("Path must not be None.")
        if os.path.exists(path) and os.path.isfile(path):
            with open(path, "r") as file:
                data = json.load(file)
                return data["name"]
        else:
            raise FileNotFoundError(f"No such file or directory: '{path}'")
        
    
    def get_keys(self) -> list:
        return self.__keys


    def add_item(self, key:str, value):
        if key is None and value is None:
            raise Exception("Key and value must not be None.")
        elif key is None:
            raise Exception("Key must not be None.")
        elif value is None:
            raise Exception("Value must not be None.")
        
        if key in self.__keys:
            raise Exception(f"Key {key} is already in use.")
        
        self.__storage[key] = value
        self.__keys.append(key)
        self.__values.append(value)


    def remove_item(self, key:str) -> object:
        if key is None:
            raise Exception("Key must not be None.")
        
        if key not in self.__keys:
            raise Exception(f"Key {key} is not in use.")
        
        value = self.__storage.pop(key)
        self.__keys.remove(key)
        self.__values.remove(value)
        return value


    def get_item(self, key:str) -> object:
        if key is None:
            raise Exception("Key must not be None.")
        
        if key not in self.__keys:
            raise Exception(f"Key {key} is not in use.")
        
        return self.__storage[key]


    def set_item(self, key:str, value) -> object:
        if key is None and value is None:
            raise Exception("Key and value must not be None.")
        elif key is None:
            raise Exception("Key must not be None.")
        elif value is None:
            raise Exception("Value must not be None.")
        
        if key not in self.__keys:
            raise Exception(f"Key {key} is not in use.")
        
        old_value = self.__storage[key]
        self.__storage[key] = value
        self.__values.remove(old_value)
        self.__values.append(value)

        return old_value
    

    def clear(self):
        self.__storage.clear()
        self.__keys.clear()
        self.__values.clear()
    

    def size(self) -> list:
        return len(self.__keys)
    

    def get_name(self) -> str:
        return self.__name
    

    def get_id(self) -> uuid.UUID:
        return self.__id
    

    def save_storage(self, path:str) -> str:
        if path is None:
            raise Exception("Path must not be None.")
        
        if not os.path.isdir(path):
            raise Exception("Path must be a directory.")
        
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        
        file_path = os.path.join(path, f"{self.__id}.json")
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump({
                "name": self.__name,
                "id": str(self.__id),
                "storage": self.__storage
            }, file, indent=4)

        return file_path