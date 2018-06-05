import logging

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

binder = Binder()
