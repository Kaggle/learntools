import re

from nb_utils import line_macros

"""
TODO: Separation of concerns between LessonPreprocessor and MacroProcessor is
muddled. LessonPreprocessor currently owns logic for expander macros. 
"""

class RmCellException(Exception):
    pass

class MacroProcessor(object):

    def __init__(self, cfg):
        self.cfg = cfg

    def process_cell(self, cell):
        src = cell['source']
        try:
            self.apply_cell_macros(src)
        except RmCellException:
            return None # Indicator to remove this cell from nb
        src = self.apply_line_macros(src)
        cell['source'] = src
        return cell

    def apply_cell_macros(self, src):
        cell_macro_pattern = r'#%%(.+)%%\s*$'
        topline = src.split('\n')[0]
        match = re.match(cell_macro_pattern, topline)
        if match:
            name, args = self._parse_inner_macro_string(match.group(1))
            if name == 'RM':
                raise RmCellException
            elif name == 'RM_IF':
                assert len(args) == 1
                if args[0]:
                    raise RmCellException
            else:
                assert False, "Unrecognized cell-level macro name: {}".format(name)


    def apply_line_macros(self, src):
        # NB: + is greedy, so macro names can still include underscores.
        # (Might need to restrict inner match character set to avoid false
        # positives)
        line_macro_pattern = r'\s*#_(.+)_\s*$'
        lines = src.split('\n')
        i = 0
        newlines = []
        while i < len(lines):
            l = lines[i]
            match = re.match(line_macro_pattern, l)
            if match:
                assert i+1 < len(lines), ("Macro {} has no following line to "
                        "act on").format(l)
                nextline = lines[i+1]
                macro_name, args = self._parse_inner_macro_string(match.group(1))
                fn = getattr(line_macros, macro_name)
                res = fn(nextline, *args)
                if res is not None:
                    newlines.append(res)
                # Jump ahead by 2 (moving past the macro line, and the following
                # line that it transformed)
                i += 2
            else:
                newlines.append(l)
                i += 1
        return '\n'.join(newlines)


    def _parse_inner_macro_string(self, macro):
        args = []
        if macro.endswith(')'):
            macro, argstr = macro[:-1].split('(')
            # XXX: I guess this is assuming <= 1 arg? Which hasn't been violated so far.
            args = [argstr.strip()] if argstr.strip() else []
        return macro, self._transform_macro_args(args)

    def _transform_macro_args(self, args):
        def transform(arg):
            if arg == 'PROD':
                return not self.cfg.get('testing', False)
            if arg == 'DAILY':
                return self.cfg.get('daily', False)
            if arg == 'NOTDAILY':
                return not self.cfg.get('daily', False)
            else:
                return arg
        return list(map(transform, args))



# Not used?
def _delete_macro_line(src, match):
    a, b = match.spam()

    try:
        line_start = src.rindex('\n', a) + 1
    except IndexError:
        # The macro was on the first line of the cell
        line_start = 0
    line_end = src.find('\n', b)
    # Remove up to and including the newline
    return src[:line_start] + src[line_end+1:]
