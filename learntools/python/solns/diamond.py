def diamond(height):
    s = ''
    # The characters currently being used to build the left and right half of 
    # the diamond, respectively. (We need to escape the backslash with another
    # backslash so Python knows we mean a literal "\" character.)
    l, r = '/', '\\'
    # The "radius" of the diamond (used in lots of calculations)
    rad = height // 2
    for row in range(height):
        # The first time we pass the halfway mark, swap the left and right characters
        if row == rad:
            l, r = r, l
        if row < rad:
            # For the first row, use one left character and one right. For
            # the second row, use two of each, and so on...
            nchars = row+1
        else:
            # Until we go past the midpoint. Then we start counting back down to 1.
            nchars = height - row
        left = (l * nchars).rjust(rad)
        right = (r * nchars).ljust(rad)
        s += left + right + '\n'
    # Trim the last newline - we want every line to end with a newline character
    # *except* the last
    return s[:-1]
