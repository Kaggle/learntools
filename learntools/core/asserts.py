
def assert_has_columns(df, cols):
    for col in cols:
        assert col in df.columns, "Expected df to have column {}".format(col)

def assert_isinstance(cls, **named_things):
    for name, val in named_things.items():
        assert isinstance(val, cls), "Expected {} to have type `{!r}` but had type `{!r}`".format(name, cls, type(val))
