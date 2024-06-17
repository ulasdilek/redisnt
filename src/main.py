import cmd2
from store_manager import StoreManager

class KV_CLI(cmd2.Cmd):
    # set the parsers
    new_parser = cmd2.Cmd2ArgumentParser()
    new_parser.add_argument("name", help="Name of the store")

    add_parser = cmd2.Cmd2ArgumentParser()
    add_parser.add_argument("key", help="Key to add")
    add_parser.add_argument("value", help="Value to add")
    
    set_parser = cmd2.Cmd2ArgumentParser()
    set_parser.add_argument("key", help="Key to set")
    set_parser.add_argument("value", help="Value to set")
    
    get_parser = cmd2.Cmd2ArgumentParser()
    get_parser.add_argument("key", help="Key to get")

    remove_parser = cmd2.Cmd2ArgumentParser()
    remove_parser.add_argument("key", help="Key to remove")

    quit_parser = cmd2.Cmd2ArgumentParser()
    quit_parser.add_argument('-f', '--force', action='store_true', help='Force save the store even if an error occurs')

    def __init__(self):
        super().__init__()
        self.store_manager = StoreManager()

    @cmd2.with_argparser(new_parser)
    @cmd2.with_category("Store Management Commands")
    def do_new(self, args):
        """Create a Key Value Store"""
        self.store_manager.new_store(args.name)
        self.poutput(f"Created store with name {args.name}")

    @cmd2.with_category("Store Management Commands")
    def do_list(self, args):
        """List the stores"""
        if self.store_manager.is_store_in_use():
            self.poutput(f"Store in use: {self.store_manager.get_name()}")
        else:
            self.poutput("No store in use.")
        stores = self.store_manager.list_stores()
        self.poutput(f"Stores ({len(stores)}):")
        for id, name in stores:
            self.poutput(f"- {id} : {name}")

    @cmd2.with_category("Store Management Commands")
    def do_load(self, args):
        """Load a store"""
        names = [name for id, name in self.store_manager.list_stores()]
        store_selection = self.select(names, "Select a store to load: ")
        self.store_manager.change_store_in_use(store_selection)
        self.poutput(f"Loaded store {store_selection}")

    @cmd2.with_category("Store Management Commands")
    def do_save(self, args):
        """Save the store in use"""
        self.store_manager.save_store_in_use()
        self.poutput(f"Saved store with id {self.store_manager.get_id()}")

    @cmd2.with_category("Store Management Commands")
    def do_release(self, args):
        """Release the store in use"""
        self.store_manager.release_store_in_use()
        self.poutput("Released store.")

    @cmd2.with_category("Store Management Commands")
    def do_delete(self, args):
        """Delete the store in use"""
        confirmation = self.select(["yes", "no"], f"Are you sure you want to delete the store {self.store_manager.get_name()}? ")
        if confirmation == "yes":
            self.store_manager.delete_store_in_use()
            self.poutput("Deleted store.")
        else:
            self.poutput("Store deletion cancelled.")

    @cmd2.with_argparser(add_parser)
    @cmd2.with_category("Key-Value Store Commands")
    def do_add(self, args):
        """Add a key-value pair"""
        if self.store_manager:
            self.store_manager.add_item(args.key, args.value)
            self.poutput(f"Added {args.key} with value {args.value}")
        else:
            self.poutput("No store in use. Use the 'new' command to create a store or 'load' command to choose from available stores.")

    @cmd2.with_argparser(set_parser)
    @cmd2.with_category("Key-Value Store Commands")
    def do_set(self, args):
        """Set a key-value pair"""
        if self.store_manager:
            self.store_manager.set_item(args.key, args.value)
            self.poutput(f"Set {args.key} to {args.value}")
        else:
            self.poutput("No store in use. Use the 'new' command to create a store or 'load' command to choose from available stores.")

    @cmd2.with_argparser(get_parser)
    @cmd2.with_category("Key-Value Store Commands")
    def do_get(self, args):
        """Get the value for a key"""
        if self.store_manager:
            self.poutput(self.store_manager.get_item(args.key))
        else:
            self.poutput("No store in use. Use the 'new' command to create a store or 'load' command to choose from available stores.")

    @cmd2.with_argparser(remove_parser)
    @cmd2.with_category("Key-Value Store Commands")
    def do_remove(self, args):
        """Remove a key-value pair"""
        if self.store_manager:
            self.store_manager.remove_item(args.key)
            self.poutput(f"Removed {args.key}")
        else:
            self.poutput("No store in use. Use the 'new' command to create a store or 'load' command to choose from available stores.")

    @cmd2.with_category("Key-Value Store Commands")
    def do_size(self, args):
        """Get the size of the store in use"""
        if self.store_manager:
            self.poutput(self.store_manager.get_size())
        else:
            self.poutput("No store in use. Use the 'new' command to create a store or 'load' command to choose from available stores.")

    @cmd2.with_category("Key-Value Store Commands")
    def do_keys(self, args):
        """Get the keys in the store in use"""
        if self.store_manager:
            keys = self.store_manager.get_keys()
            if len(keys) == 0:
                self.poutput("No keys in store.")
            for key in keys:
                self.poutput(f"- {key}")
        else:
            self.poutput("No store in use. Use the 'new' command to create a store or 'load' command to choose from available stores.")

    @cmd2.with_category("Key-Value Store Commands")
    def do_clear(self, args):
        """Clear the store in use"""
        if self.store_manager:
            self.store_manager.clear_store_in_use()
            self.poutput("Store cleared.")
        else:
            self.poutput("No store in use. Use the 'new' command to create a store or 'load' command to choose from available stores.")

    @cmd2.with_argparser(quit_parser)
    def do_quit(self, args):
        """Quit the application"""
        if not self.store_manager.is_store_in_use():
            self.poutput("Quitting the application.")
            return super().do_quit("")
        try:
            self.store_manager.save_store_in_use()
            self.poutput(f"Saved store with id {self.store_manager.get_id()}.")
            self.poutput("Quitting the application.")
            return super().do_quit("")
        except Exception as e:
            self.poutput(f"Error saving store: {e}")
            if args.force:
                self.poutput("Force quitting enabled. Quitting without saving.")
                return super().do_quit("")


if __name__ == "__main__":
    app = KV_CLI()
    app.cmdloop()