"""
A family of macros that take a line of text (and possibly some other arguments)
and return a transformed version to replace it with.
"""

import re

def RM(line):
    # Returning None meaning "delete this" is a little dangerous (it's easy to do
    # this accidentally by forgetting a return statement). Could also consider 
    # exception as control flow here.
    # (Also, it'd be convenient/intuitive for the default behaviour in the absence of a return
    # to be "do nothing")
    return None

def RM_IF(line, cond):
    if cond:
        return RM(line)
    return line

def COMMENT_IF(line, cond):
    if cond:
        return '#' + line
    return line

def UNCOMMENT(line):
    assert re.match(r'\s*#', line), "Can't uncomment line:{!r}".format(line)
    return line.replace('#', '', 1)


def UNCOMMENT_IF(line, cond):
    if cond:
        return UNCOMMENT(line)
    return line
