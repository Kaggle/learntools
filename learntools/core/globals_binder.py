import logging

# TODO XXX: Currently a pretty bad issue where globals binding doesn't work if you
# don't order imports and call to binder.bind() carefully. Should make sure that
# gets resolved. Soln might be to set binder.g to some mutable 'set-once' globals
# wrapper, so that if some obj binds to the result of binder.readonly_globals() before
# any calls to .bind(), they'll have a reference to (what eventually ends up being) the
# real deal. bleh.
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
