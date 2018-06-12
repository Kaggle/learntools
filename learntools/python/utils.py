def backtickify(s):
    return '`{}`'.format(s)

def bind_exercises(g, exercises, start=1):
    for i, ex in enumerate(exercises):
        qno = i + start
        varname = 'q{}'.format(qno)
        assert varname not in g
        g[varname] = ex
        yield varname

# TODO: replicated in FnExercise
def format_args(fn, args):
    # I guess technically not portable to other python implementations...
    c = fn.__code__
    params = c.co_varnames[:c.co_argcount]
    #assert len(args) == len(params)
    return ', '.join([
        '`{}={}`'.format(param, repr(arg))
        for (param, arg) in zip(params, args)
        ])
