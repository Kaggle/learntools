
def assert_has_columns(df, cols, name=None):
    for col in cols:
        assert col in df.columns, "Expected dataframe{} to have column {}".format(
                '' if name is None else ' `{}`'.format(name), col
                )

def assert_isinstance(cls, **named_things):
    for name, val in named_things.items():
        assert isinstance(val, cls), "Expected {} to have type `{!r}` but had type `{!r}`".format(name, cls, type(val))

def assert_len(thing, exp_len, name):
    actual = len(thing)
    assert actual == exp_len, "Expected {} to have length {}, but was {}".format(
            name, exp_len, actual,
            )
