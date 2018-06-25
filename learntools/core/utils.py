

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


# TODO: Could make exercises arg optional. If not explictly provided, go through
# all the received globals and take the ones that are Problem subclasses.
# (Actually, I think this won't work currently, since we import * from problem in
# exercise modules, so we would get all the abstract Problem subclasses. We'd need to
# explicitly mark them as abstract for this trick to be feasible. (import abc?))
def bind_exercises(g, exercises, start=1, var_format='q{n}'):
    for i, prob_cls in enumerate(exercises):
        qno = i + start
        varname = var_format.format(n=qno)
        assert varname not in g
        pv = _instantiate_probview(prob_cls)
        g[varname] = pv
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
