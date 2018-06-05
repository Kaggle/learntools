
def bind_exercises(g, exercises, start=1):
    for i, ex in enumerate(exercises):
        qno = i + start
        varname = 'q{}'.format(qno)
        assert varname not in g
        g[varname] = ex
        yield varname
