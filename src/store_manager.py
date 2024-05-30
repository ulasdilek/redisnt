import os
from kv_store import KVStore

class StoreManager:
    BASE_PATH = "data/stores"

    def __init__ (self):
        if not os.path.exists(StoreManager.BASE_PATH):
            os.makedirs(StoreManager.BASE_PATH, exist_ok=True)
        self.__stores = {} # dict { id: name }
        self.__store_in_use = None

    
    def __check_store_in_use(self):
        if self.__store_in_use is None:
            raise Exception("No store in use.")


    def new_store(self, name:str):
        if name is None:
            raise Exception("Name must not be None.")
        
        self.__store_in_use = KVStore(name)
        self.__stores[self.__store_in_use.get_id()] = name


    def load_stores(self):
        # iterate .json files in BASE_PATH
        for file in os.listdir(StoreManager.BASE_PATH):
            if file.endswith(".json"):
                id = file.split(".")[0]
                name = KVStore.retreive_name(os.path.join(StoreManager.BASE_PATH, file))
                self.__stores[id] = name


    def save_store_in_use(self):
        self.__check_store_in_use()
        path = os.path.join(StoreManager.BASE_PATH, str(self.__store_in_use.get_id()) + ".json")
        self.__store_in_use.save_storage(path)


    def release_store_in_use(self):
        self.__store_in_use = None


    def change_store_in_use(self, name:str, id:str = None):
        if id is not None:
            if id in self.__stores:
                self.__store_in_use = KVStore.from_file(os.path.join(StoreManager.BASE_PATH, id + ".json"))
            else:
                raise Exception(f"No store with id {id} found.")
        else:
            ids = [key for key, value in self.__stores.items() if value == name]
            if len(ids) == 0:
                raise Exception(f"No store with name {name} found.")
            elif len(ids) > 1:
                raise Exception(f"Multiple stores with name {name} found.")
            
            self.__store_in_use = KVStore.from_file(os.path.join(StoreManager.BASE_PATH, ids[0] + ".json"))

            
    def delete_store_in_use(self):
        self.__check_store_in_use()
        self.__store_in_use.clear()
        path = os.path.join(StoreManager.BASE_PATH, str(self.__store_in_use.get_id()) + ".json")
        os.remove(path)
        self.__stores.pop(self.__store_in_use.get_id())
        self.__store_in_use = None


    def add_item(self, key:str, value):
        self.__check_store_in_use()
        self.__store_in_use.add_item(key, value)


    def remove_item(self, key:str) -> object:
        self.__check_store_in_use()
        return self.__store_in_use.remove_item(key)
    

    def get_item(self, key:str) -> object:
        self.__check_store_in_use()
        return self.__store_in_use.get_item(key)
    

    def set_item(self, key:str, value) -> object:
        self.__check_store_in_use()
        return self.__store_in_use.set_item(key, value)
    

    def clear_store_in_use(self):
        self.__check_store_in_use()
        self.__store_in_use.clear()


    def get_size(self) -> int:
        self.__check_store_in_use()
        return self.__store_in_use.size()
    

    def get_name(self) -> str:
        self.__check_store_in_use()
        return self.__store_in_use.get_name()
    

    def get_id(self) -> str:
        self.__check_store_in_use()
        return self.__store_in_use.get_id()
    

    def get_store_count(self) -> int:
        return len(self.__stores)
    
    
    def get_names(self) -> list:
        return list(self.__stores.values())
    

    def get_ids(self) -> list:
        return list(self.__stores.keys())
    

    def get_stores(self) -> dict:
        return self.__stores