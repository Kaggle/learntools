import re
import logging
import os
import subprocess

import nbformat
from nbconvert.preprocessors import Preprocessor

DEBUG = 0
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)

IGNORE_UNKNOWN_MACROS = 0

class UnrecognizedMacroException(Exception):
    pass

def get_git_branch():
    """Return the current git branch as a string"""
    return subprocess.check_output(["git", "symbolic-ref", "--short", "HEAD"])\
            .decode('utf8').strip()

class LearnLessonPreprocessor(Preprocessor):
    
    # NB: This is the only overridden Preprocessor method. All other methods are custom.
    def preprocess(self, nb, resources):
        # See render.py for how resources as populated.
        self.track = resources['track_meta']
        # May be None for notebooks with type='extra'
        self.lesson = resources['lesson']
        # Corresponds to track_config.yaml
        track_cfg = resources['track_cfg']
        nb_meta = resources['nb_meta']

        for i, cell in enumerate(nb.cells):
            nb.cells[i] = self.process_cell(cell)
        # NB: There may be some cases where we need to access learntools in a tutorial
        # or ancillary notebook as well. Could encode this in track_meta, or if we wanted
        # to be really clever, could look for learntools imports in code cells.
        if track_cfg.get('development', False) and nb_meta.type == 'exercise':
            self.pip_install_lt_hack(nb)
        return nb, resources
    
    def pip_install_lt_hack(self, nb):
        """pip install learntools @ the present branch when running on Kernels"""
        branch = get_git_branch()
        pkg = 'git+https://github.com/Kaggle/learntools.git@{}'.format(branch)
        self.pip_install_hack(nb, [pkg])

    def pip_install_hack(self, nb, pkgs):
        """Insert some cells at the top of this notebook that pip install the given
        packages to /kaggle/working, then add that directory to sys.path.
        """
        if not pkgs:
            return
        extra_cells = []
        for pkg in pkgs:
            extra_cells.append(self.pip_install_cell(pkg))

        # NB: Workaround for 'read-only file sytem' issue when pip installing.
        # Hopefully at some point this becomes easier.
        syspath_lines = [
                'import sys\n',
                "sys.path.append('/kaggle/working')",
        ]
        syspath_cell = self.make_code_cell(source=syspath_lines)
        extra_cells.append(syspath_cell)
        nb.cells = extra_cells + nb.cells

    @classmethod
    def pip_install_cell(cls, pkg_spec):
        cmd = '!pip install -U -t /kaggle/working/ {}'.format(pkg_spec)
        return cls.make_code_cell(source=[cmd])

    @staticmethod
    def make_code_cell(**kwargs):
        defaults = dict(
                cell_type="code",
                execution_count=None,
                metadata={},
                source=[],
                outputs=[],
                )
        defaults.update(kwargs)
        return nbformat.from_dict(defaults)

    def process_cell(self, cell):
        # Find all things that look like macros
        pattern = r'#\$([^$]+)\$'
        src = cell['source']
        macros = re.finditer(pattern, src)
        newsrc = ''
        i = 0
        for match in macros:
            logging.debug(match)
            a, b = match.span()
            macro = match.group(1)
            try:
                expansion = self.expand_macro(macro, cell)
            except UnrecognizedMacroException as e:
                if IGNORE_UNKNOWN_MACROS:
                    expansion = None
                    logging.warn("Unrecognized macro: {}".format(macro))
                else:
                    raise e
            except Exception as e:
                print("Error parsing macro match {}".format(match))
                raise e
            newsrc += src[i:a]
            # Some macros might actually expand to nothing (e.g. if their purpose is to mutate cell metadata)
            if expansion:
                newsrc += expansion
            i = b
        newsrc += src[i:]
        cell['source'] = newsrc
        return cell

    def expand_macro(self, macro, cell):
        """Expand the given macro string (or apply it to the given cell, if 
        it's side-effecty), by looking up and calling the corresponding 
        LessonPreprocessor method.
        """
        # TODO: The fact that some macros expand to some text, and some just have 
        # some effect on their cell leads to some awkwardness. Could be nice to 
        # delineate syntactically. e.g. #$HIDE!$
        args = []
        if macro.endswith(')'):
            macro, argstr = macro[:-1].split('(')
            args = [argstr.strip()] if argstr.strip() else []
        macro_method = getattr(self, macro, None)
        if macro_method is None:
            raise UnrecognizedMacroException("Don't know how to handle the macro with name: {}".format(macro))
        return macro_method(*args, cell=cell)

    def EXERCISE_FORKING_URL(self, **kwargs):
        return self.lesson.exercise.forking_url

    def HIDE_INPUT(self, cell):
        cell['metadata']['_kg_hide-input'] = True
    
    def HIDE_OUTPUT(self, cell):
        cell['metadata']['_kg_hide-output'] = True

    def HIDE(self, cell):
        self.HIDE_INPUT(cell)
        self.HIDE_OUTPUT(cell)

    def YOURTURN(self, **kwargs):
        """Some boilerplate text to be used at the end of a tutorial notebook, to
        lead into the corresponding exercise.
        """
        return """# Your turn!

Head over to [the Exercises notebook]({}) to get some hands-on practice working with {}.""".format(
        self.lesson.exercise.forking_url, self.lesson.topic,
        )

    def EXERCISE_SETUP(self, **kwargs):
        # Standard setup code. Not currently used. Maybe should be.
        pass

    def TUTORIAL_URL(self, lesson_num=None, **kwargs):
        if lesson_num is None:
            lesson = self.lesson
        else:
            lesson_idx = int(lesson_num) - 1
            lesson = self.track.lessons[lesson_idx]
        return lesson.tutorial.url

    def EXERCISE_URL(self, lesson_num, **kwargs):
        # TODO: unify this + EXERCISE_FORKING_URL (have that be this with default arg)
        lesson_idx = int(lesson_num) - 1
        lesson = self.track.lessons[lesson_idx]
        return lesson.exercise.forking_url

    def EXERCISE_PREAMBLE(self, **kwargs):
        return """These exercises accompany the tutorial on [{}]({}).""".format(
                self.lesson.topic, self.lesson.tutorial.url,
                )

    def END_OF_EXERCISE(self, forum_cta=1, **kwargs):
        # Don't use this macro for the very last exercise
        next = self.lesson.next
        res = ''
        if int(forum_cta):
            res += "If you have any questions, be sure to post them on the [forums](https://www.kaggle.com/learn-forum).\n\n"

        res += """Remember that your notebook is private by default, and in order to share it with other people or ask for help with it, you'll need to make it public. First, you'll need to save a version of your notebook that shows your current work by hitting the "Commit & Run" button. (Your work is saved automatically, but versioning your work lets you go back and look at what it was like at the point you saved it. It also let's you share a nice compiled notebook instead of just the raw code.) Then, once your notebook is finished running, you can go to the Settings tab in the panel to the left (you may have to expand it by hitting the [<] button next to the "Commit & Run" button) and setting the "Visibility" dropdown to "Public".

# Keep Going

When you're ready to continue, [click here]({}) to continue on to the next tutorial on {}.""".format(
        next.tutorial.url, next.topic,
        )
        return res

        # Alternative formulation (used on days 5 and 6 of Python challenge):
        # Want feedback on your code? To share it with others or ask for help, you'll need to make it public. Save a version of your notebook that shows your current work by hitting the "Commit & Run" button. Once your notebook is finished running, go to the Settings tab in the panel to the left (you may have to expand it by hitting the [<] button next to the "Commit & Run" button) and set the "Visibility" dropdown to "Public".



