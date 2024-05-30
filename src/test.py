from kv_store import KVStore

name = "store name"
store = KVStore(name)

assert store.get_name() == name
assert store.size() == 0

store.add_item("key1", 56)

assert store.size() == 1

store.add_item("key2", 78)

assert store.size() == 2

item1 = store.get_item("key1")

assert item1 == 56

item2 = store.get_item("key2")

assert item2 == 78

old_item1 = store.set_item("key1", 100)
new_item1 = store.get_item("key1")

assert old_item1 != new_item1
assert new_item1 == 100

removed_item = store.remove_item("key1")

assert removed_item == new_item1
assert store.size() == 1

store.add_item(90, "value3")
assert store.size() == 2

store.clear()
assert store.size() == 0