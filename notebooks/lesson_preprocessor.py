import sys
import re
import logging
import os

import nbformat as nbf
from nbconvert.preprocessors import Preprocessor
import traitlets
from box import Box
import utils

DEBUG = 0
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)

IGNORE_UNKNOWN_MACROS = 0

class UnrecognizedMacroException(Exception):
    pass

def wrap_lessons(lesson_dicts):
    """Given a list of lesson dicts (as set in nbconvert_config.py), return a list
    of Lesson objects wrapping those dicts.
    """
    res = [Lesson(d, i) for i, d in enumerate(lesson_dicts)]
    for i, lesson in enumerate(res):
        if i > 0:
            lesson._prev = res[i-1]
            lesson.first = False
        else:
            lesson.first = True
        if i < len(res)-1:
            lesson._next = res[i+1]
            lesson.last = False
        else:
            lesson.last = True
    return res

class Lesson:
    def __init__(self, d, idx):
        self.num = idx+1
        for k, v in d.items():
            if isinstance(v, dict):
                v = Box(v)
            setattr(self, k, v)

    @property
    def exercise_forking_url(self):
        return 'https://www.kaggle.com/kernels/fork/{}'.format(self.exercise.scriptid)

    @property
    def tutorial_url(self):
        return 'https://www.kaggle.com/{}'.format(self.tutorial.slug)

    @property
    def next(self):
        if self.last:
            raise ValueError("Lesson number {} is the last. No next lesson.".format(self.num))
        return self._next
    @property
    def prev(self):
        if self.first:
            raise ValueError("Lesson number {} is the first. No prev lesson.".format(self.num))
        return self._prev

class LearnLessonPreprocessor(Preprocessor):

    # This gets set directly (to a list of lesson dicts) in track's 
    # nbconvert_config.py file. This code is insane.
    # TODO: deprecate me
    lessons_metadata = traitlets.List().tag(config=True)
    
    # NB: This is the only overridden Preprocessor method. All other methods are custom.
    def preprocess(self, nb, resources):
        # NB: resources is dict-like with keys:
        #   - config_dir
        #   - output_files_dir, output_extension
        #   - metadata, inner dict-like w/ keys name, path, modified_date
        #   - unique_key
        path = resources['metadata']['path']
        suff = '/partials'
        assert path.endswith(suff), path
        track_path = path[:-len(suff)]
        track = utils.get_track_meta(track_path)
        self.track = track
        nb_fname = resources['metadata']['name'] + '.ipynb'
        nb_meta = track.get_notebook(nb_fname)
        # TODO: May need to catch an exception here in case of nbs that have no associated lesson
        self.lesson = nb_meta.lesson

        # NB: Previously aborted at this point if this notebook didn't belong to a lesson.
        for i, cell in enumerate(nb.cells):
            nb.cells[i] = self.process_cell(cell)
        return nb, resources

    def process_cell(self, cell):
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

        # Alternative formulation (used on days 5 and 6):
        # Want feedback on your code? To share it with others or ask for help, you'll need to make it public. Save a version of your notebook that shows your current work by hitting the "Commit & Run" button. Once your notebook is finished running, go to the Settings tab in the panel to the left (you may have to expand it by hitting the [<] button next to the "Commit & Run" button) and set the "Visibility" dropdown to "Public".



