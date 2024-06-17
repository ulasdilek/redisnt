# Redisn't

This is —or at least will be— a simple key-value store that hopefully _imitates_ [Redis](https://redis.io/)

## How to

Using a Python virtual environment is recommended, although not necessary. [Here is how.](https://www.dataquest.io/blog/a-complete-guide-to-python-virtual-environments/)

Install the required modules:
```pip install -r requirements.txt```

Run the program:
```python main.py```

To access the list of commands, type `help` in the prompt.

## Features

- Create a key-value store
- Save a store to disk
- Load a store from disk
- Delete a store
- Clear a store
- Add a key-value pair
- Get a value by key
- Set a value by key
- Delete a key-value pair
- List all keys

> I know it isn't much, but it's honest work :D

# Changelog

**17.06.2024** -> There is now a CLI based on [cmd2](https://github.com/python-cmd2/cmd2). It interacts with the `StoreManager` to manage multiple key-value stores. But I might scratch that idea and just have a single `KVStore`.