from learntools.core.multiproblem import MultipartProblem

def backtickify(s):
    return '`{}`'.format(s)

# TODO: Maybe this factory should be a class method of ProblemView or something?
def instantiate_probview(prob_cls):
    # TODO: Bleh, circular import...
    from learntools.core import problem_view as pv
    from learntools.core.globals_binder import binder
    # NB: May eventually have some subclasses for this?
    viewer_cls = pv.ProblemView
    prob = prob_cls()
    view = viewer_cls(prob, binder.readonly_globals())
    # XXX: Circular reference. :/
    # Consider using weakref (https://docs.python.org/3/library/weakref.html)
    # Also, would just have preferred a cleaner separation between these abstractions...
    prob._view = view
    return view


def bind_exercises(g, exercises, start=1, var_format='q{n}'):
    for i, prob_cls in enumerate(exercises):
        # A value of None is a placeholder. Reserve the corresponding question number, but don't create any corresponding Problem obj.
        if prob_cls is None:
            continue
        qno = i + start
        varname = var_format.format(n=qno)
        assert varname not in g
        # TODO: Probably cleaner to just pass these as sublists, rather than having
        # the MultipartProblem class start in some nascent state and get 'activated' here
        if isinstance(prob_cls, MultipartProblem):
            mpp = prob_cls
            g[varname] = mpp
            mpp._varname = varname
            for i, prob_cls in enumerate(mpp.problems):
                prob = instantiate_probview(prob_cls)
                letter = chr(ord('a')+i)
                setattr(mpp, letter, prob)
                mpp._prob_map[letter] = prob
        else:
            pv = instantiate_probview(prob_cls)
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
