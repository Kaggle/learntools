import logging

# This method captures a reference to the globals dict so it can be seen by checking code

class Binder:
    
    def __init__(self):
        self.bound = False
        self.g = None

    def bind(self, global_vars):
        if self.bound:
            if id(global_vars) == id(self.g):
                logging.warn("Ignoring repeated attempt to bind to globals")
            else:
                raise Exception("Attempted to bind different vars to already-bound binder")
        else:
            self.g = global_vars
            self.bound = True

    def readonly_globals(self):
        return ReadOnlyGlobals(self.g)

class ReadOnlyGlobals:
    """Readonly wrapper around captured globals dict, plus some convenience methods.
    """

    def __init__(self, g):
        self.g = g

    def __getitem__(self, key):
        # TODO: maybe wrap KeyError in some custom exception? 
        # Or maybe there should be two ways of looking up a key, one of which has
        # the semantics "if this key is missing, the user did something terribly wrong"
        return self.g[key]

    def __contains__(self, key):
        return key in self.g

    def keys(self):
        return self.g.keys()

    def lookup(self, keys):
        return [self.g[k] for k in keys]

    # No __setitem__ 

binder = Binder()
