from exercise import Exercise, FunctionExercise, ThoughtExperiment, colorify

class q1(Exercise):

    _hint = "Try using a third variable."
    _solution = """Use a third variable to temporarily store one of the old values. e.g.:

    tmp = a
    a = b
    b = tmp

If you've read lots of Python code, you might have seen the following trick to swap two variables in one line:

    a, b = b, a

We'll demystify this bit of Python magic later when we talk about **tuples**."""

    def store_original_ids(cls, ida, idb):
        cls.id_a = ida
        cls.id_b = idb

    def _do_check(cls, ida, idb):
        if ida == cls.id_b and idb == cls.id_a:
            return
        assert not (ida == cls.id_a and idb == cls.id_b), ("`a` and `b` still"
                " have their original values.")
        orig_ids = (cls.id_a, cls.id_b)
        assert ida in orig_ids, ("`a` was assigned something weird (its id has changed,"
                " but to something other than `b`'s id)")
        assert idb in orig_ids, ("`b` was assigned something weird (its id has changed,"
                " but to something other than `a`'s id)")
        assert ida != idb, "`b` and `a` are the same!"
        assert False, "This fails in a way we did not anticipate!"

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __str__(self):
        return "Rectangle with width of {} and height of {}".format(
                self.width, self.height)

    def __repr__(self):
        return '<{}>'.format(str(self))

example_rect = Rectangle(3, 5)

class q3(FunctionExercise):
    
    _test_cases = [
        (Rectangle(3, 5), 16),
        (Rectangle(1, 10), 22)
        ]

    # TODO: add scaffolding for multiple hints.
    _hints = [
            ("Use the `dir()` function on `example_rect` to see what attributes and"
                " methods Rectangle objects have available."),
            ("`dir(example_rect)` shows that Rectangle objects have attributes"
                " `width` and `height`. Use the dot syntax to access their values"
                " (e.g. try typing `example_rect.width` into the console)."),
            ]
    _hint = _hints[0] # XXX

    _solution = "`return 2 * rect.height + 2 * rect.width`"

class q4(Exercise):

    _solution = """Trick question! It's not possible. Why doesn't swapping `var1` and `var2` (like we did in problem 1) work inside the `swap` function? When we call `swap(a, b)`, we temporarily create new variables `var1` and `var2` inside the function, and assign them the *values* of `a` and `b` (i.e. the objects to which `a` and `b` refer). The swap function can't see anything about the pointers `a` and `b`. It only sees their values.  In fact, the `swap` function can't see any difference between being called like `swap(a, b)` or `swap(1, 0)`, or `swap(b+1, a-1)`.

What about swapping variables `a` and `b` inside the swap function (rather than using `var1` and `var2`)? First of all, that's cheating - we want our function to work for any pair of variables we pass in, not just ones called `a` and `b`.  But also, it doesn't even work! Variables assigned to inside a function are treated as "local", meaning they disappear when the function exits. This is true even if a variable of the same name exists outside the function (in the "global" scope)."""

    def _do_check(cls, a, b):
        assert a == 0 and b == 1, ("Expected `a` to be `0` and `b` to be `1`"
                " but got `a = {}`, `b = {}`").format(a, b)
        ch = colorify("**Cheater! J'accuse!**", '#cc3333')
        assert False, ("{}\nOkay, a and b have the right values, but I suspect"
                " you (maybe accidentally) cheated. Did you change any code other"
                " than the body of the `swap` function? (That's not allowed)\n"
                "<small>Did you use the `global` statement or the `globals()`"
                " function? If so, maybe you should be teaching this lesson."
                " (but also, your code will fail when we pass variables with"
                " names other than `a` and `b`).").format(ch)
