
class NotAttempted(Exception):
    pass

class Incorrect(Exception):
    pass

class UserlandExceptionIncorrect(Incorrect):
    def __init__(self, exception, args):
        self.wrapped_exception = exception
        self.msg  = ("When calling your function with arguments `{!r}`, Python"
                " raised the following exception:\n{}").format(args, exception)
    def __str__(self):
        return self.msg

class Uncheckable(Exception):
    pass
