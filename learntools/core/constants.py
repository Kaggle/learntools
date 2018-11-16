
class PlaceholderValue(object):

    def __eq__(self, other):
        return isinstance(other, PlaceholderValue)

PLACEHOLDER = PlaceholderValue()
