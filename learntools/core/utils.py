

def backtickify(s):
    return '`{}`'.format(s)

def _instantiate_probview(prob_cls):
    # TODO: Bleh, circular import...
    from learntools.core import problem_view as pv
    from learntools.core.globals_binder import binder
    # NB: May eventually have some subclasses for this?
    viewer_cls = pv.ProblemView
    prob = prob_cls()
    view = viewer_cls(prob, binder.readonly_globals())
    return view


def bind_exercises(g, exercises, start=1, var_format='q{n}'):
    for i, prob_cls in enumerate(exercises):
        qno = i + start
        varname = var_format.format(n=qno)
        assert varname not in g
        pv = _instantiate_probview(prob_cls)
        g[varname] = pv
        yield varname

def format_args(fn, args):
    # I guess technically not portable to other python implementations...
    c = fn.__code__
    params = c.co_varnames[:c.co_argcount]
    #assert len(args) == len(params)
    return ', '.join([
        '`{}={}`'.format(param, repr(arg))
        for (param, arg) in zip(params, args)
        ])
