import sys
import re
import logging

import nbformat as nbf
from nbconvert.preprocessors import Preprocessor
import traitlets
from box import Box

DEBUG = 1
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)


def load_lessons(lesson_dicts):
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

    lessons_metadata = traitlets.List().tag(config=True)
    
    def preprocess(self, nb, resources):
        lt_meta = nb['metadata']['learntools_metadata']
        lesson_ix = lt_meta['lesson_index']
        lessons = load_lessons(self.lessons_metadata)
        self.lessons = lessons
        self.lesson = lessons[lesson_ix]
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
                newsrc += src[i:a] + self.expand_macro(macro)
            except Exception as e:
                print("Error parsing macro match {}".format(match))
                raise e
            i = b
        newsrc += src[i:]
        cell['source'] = newsrc
        return cell

    def expand_macro(self, macro):
        args = []
        if macro.endswith(')'):
            macro, argstr = macro[:-1].split('(')
            args = [argstr.strip()] if argstr.strip() else []
        macro_method = getattr(self, macro)
        return macro_method(*args)

    def EXERCISE_FORKING_URL(self):
        return self.lesson.exercise_forking_url

    def YOURTURN(self, topic):
        return """# Your turn!

Head over to [the Exercises notebook]({}) to get some hands-on practice working with {}.""".format(FORK_URL, topic)

    def EXERCISE_SETUP(self):
        pass

    def TUTORIAL_URL(self, lesson_num=None):
        if lesson_num is None:
            lesson = self.lesson
        else:
            lesson_idx = int(lesson_num) - 1
            lesson = self.lessons[lesson_idx]
        return lesson.tutorial_url

    def EXERCISE_URL(self, lesson_num):
        # TODO: unify this + EXERCISE_FORKING_URL (have that be this with default arg)
        lesson_idx = int(lesson_num) - 1
        lesson = self.lessons[lesson_idx]
        return lesson.exercise_forking_url

    def EXERCISE_PREAMBLE(self):
        return """These exercises accompany the tutorial on [{}]({}).""".format(
                self.lesson.topic, self.lesson.tutorial_url,
                )

    def END_OF_EXERCISE(self):
        # Don't use this macro for the very last exercise
        next = self.lesson.next
        return """If you have any questions, be sure to post them on the [forums](https://www.kaggle.com/learn-forum).

Remember that your notebook is private by default, and in order to share it with other people or ask for help with it, you'll need to make it public. First, you'll need to save a version of your notebook that shows your current work by hitting the "Commit & Run" button. (Your work is saved automatically, but versioning your work lets you go back and look at what it was like at the point you saved it. It also let's you share a nice compiled notebook instead of just the raw code.) Then, once your notebook is finished running, you can go to the Settings tab in the panel to the left (you may have to expand it by hitting the [<] button next to the "Commit & Run" button) and setting the "Visibility" dropdown to "Public".

When you're ready to continue, [click here]({}) to continue on to the next tutorial on {}.""".format(
        next.tutorial_url, next.topic,
        )


