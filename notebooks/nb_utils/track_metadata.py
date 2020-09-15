import os
import logging

import titlecase

def slug_munge(s):
    # NB: This was hacked together ad-hoc and probably still has some holes where it doesn't agree with Kernels logic.
    forbidden_chars = r'(),:&'
    lookup = {ord(c): None for c in forbidden_chars}
    s = s.translate(lookup).lower()
    tokens = s.split()
    return '-'.join(tokens)

def slugify(title, author):
    return author + '/' + slug_munge(title)

class TrackMeta(object):
    """Wrapper around the metadata lists/dictionaries defined per-track in track_meta.py
    This class (and the Lesson/Notebook classes it wraps its members in) do the following:
    - fill in default values
    - validate
    - add some derived properties and a bit of logic

    The most important properties of a TrackMeta object are:
    - lessons: a list of Lesson objects
    - notebooks: a list of Notebook objects
    """

    def __init__(self, track, lessons_meta, nbs_meta, cfg):
        self.track = track
        self.course_name = track['course_name']
        self.course_url = track['course_url']
        self.course_forum_url = track['course_forum_url']

        self.lessons = [Lesson(**lmeta) for lmeta in lessons_meta]
        # Add convenience next/prev pointers to lessons
        for lesson, next_lesson in zip(self.lessons, self.lessons[1:]):
            # TODO: Add next/prev getters to raise custom message for attempts
            # to access next of last lesson etc. for clarity
            lesson.next = next_lesson
            next_lesson.prev = lesson
        # Set first/last flags
        self.lessons[0].first = True
        self.lessons[-1].last = True
        self.notebooks = []
        author = cfg.get('author', track['author_username'])
        enable_gpu = track.get('enable_gpu', False)
        for nb_meta in nbs_meta:
            nb_meta = nb_meta.copy()
            nb_meta.setdefault('author', author)
            nb_meta.setdefault('enable_gpu', enable_gpu)
            lesson_idx = nb_meta.pop('lesson_idx', None)
            if lesson_idx is not None:
                lesson = self.lessons[lesson_idx]
                nb_meta['lesson'] = lesson
            nb = Notebook(cfg, **nb_meta)
            self.notebooks.append(nb)
            type = nb_meta['type']
            if type in ('tutorial', 'exercise'):
                assert not hasattr(lesson, type), "Can't have two {}s in one lesson".format(type)
                setattr(lesson, type, nb)
        self._set_scriptids(cfg)
        self._resolve_kernel_deps()

    @classmethod
    def from_module(cls, module, cfg):
        return cls(module.track, module.lessons, module.notebooks, cfg)

    def get_notebook(self, fname):
        """Look up a Notebook object by its filename."""
        matches = [nb for nb in self.notebooks if nb.filename == fname]
        assert len(matches) <= 1, fname
        return matches[0]

    def _set_scriptids(self, cfg):
        """Each yaml config file may give rise to a separate set of kernels, hence
        for tracks with multiple configs, exercise scriptids may be specified in
        the config file.
        """
        try:
            ids = cfg['exercise_scriptids']
        except KeyError:
            # Specifying scriptids is optional.
            return
        # Should be one id per lesson (1 exercise per lesson)
        assert len(ids) <= len(self.lessons)
        if len(ids) < len(self.lessons):
            tail = len(self.lessons) - len(ids)
            logging.warn("Config with tag {} specified {} exercise scriptids, but has {}"
                    " lessons. Ignoring last {} lesson{}".format(
                        cfg['tag'], len(ids), len(self.lessons), tail, '' if tail==1 else 's'
                        ))
        for lesson, scriptid in zip(self.lessons, ids):
            # Some ids may be set to None, in which case we do nothing for that lesson.
            # (Typically this means there is no exercise nb for that lesson)
            if scriptid is None:
                continue
            ex = lesson.exercise
            ex.scriptid = scriptid

    def _resolve_kernel_deps(self):
        """Resolve any inter-kernel data dependencies which are encoded using
        notebook filenames to their corresponding slugs.
        """
        for nb in self.notebooks:
            for i, dep in enumerate(nb.kernel_sources):
                if dep.endswith('.ipynb'):
                    referent = self.get_notebook(dep)
                    nb.kernel_sources[i] = referent.slug


class Lesson(object):
    """Instance variables:
    - topic
    - first: bool
    - last: bool
    - tutorial: Notebook
    - exercise: Notebook

    Note that the last two attributes are set outside the constructor and may
    be ommitted (sometimes a lesson is just a tutorial with no exercise or vice
    versa)
    """
    def __init__(self, topic):
        self.topic = topic
        self.first = False
        self.last = False

class Notebook(object):

    def __init__(self, cfg, filename, type, author=None, title=None, lesson=None,
            slug=None, scriptid=1, kernel_sources=(), dataset_sources=(),
            competition_sources=(), keywords=(), enable_gpu=False, enable_internet=None,
            ):
        self.cfg = cfg
        self.filename = filename
        self.stem, _ = os.path.splitext(os.path.basename(filename))
        assert type in ('tutorial', 'exercise', 'extra')
        self.type = type
        if title is None:
            assert lesson is not None, "Title attribute must be set if lesson_idx is absent"
            assert type in ('tutorial', 'exercise'), type
            self.title = '{}{}'.format(
                'Exercise: ' if type=='exercise' else '',
                self._topic_to_title(lesson.topic),
                )
        else:
            self.title = title
        suffix = cfg.get('suffix',
                'testing' if cfg.get('testing', False) else ''
                )
        if suffix:
            self.title += ' ' + suffix
        # kernels has max title length of 50
        if len(self.title) > 50:
            long_title = self.title
            self.title = self.title[:49]
            logging.warn("Truncated length {} title. Was: {!r}, Now: {!r}".format(
                len(long_title), long_title, self.title))
        self.lesson = lesson
        if slug is None:
            assert author is not None
            self.slug = slugify(self.title, author)
        else:
            self.slug = slug
        self.scriptid = scriptid
        self.kernel_sources = list(kernel_sources)
        self.dataset_sources = list(dataset_sources)
        self.competition_sources = list(competition_sources)
        self.keywords = list(keywords)
        self.enable_gpu = bool(enable_gpu)
        self.enable_internet = enable_internet

    @staticmethod
    def _topic_to_title(topic):
        """Take a string representing a notebook's topic and return a version appropriate
        to use as a kernel title (basically, apply title case).
        """
        # XXX: Special case. The titlecase module is supposed to be good about
        # leaving alone acronyms or words with idiosyncratic internal capitalization
        # (e.g. "eBay"), but it fails on the specific case of "t-SNE", probably because
        # of the punctuation.
        if topic.endswith("t-SNE"):
            base = topic[:topic.rindex(' ')]
            return titlecase.titlecase(base) + ' t-SNE'
        else:
            return titlecase.titlecase(topic)
        # with initialisms and words with idiosyncratic

    @property
    def url(self):
        return 'https://www.kaggle.com/' + self.slug
    @property
    def forking_url(self):
        # TODO: warning if scriptid = default value of 1?
        return 'https://www.kaggle.com/kernels/fork/{}'.format(self.scriptid)

    def kernel_metadata(self, cfg):
        """Return a python dictionary corresponding to an appropriate kernel-metadata.json
        file for pushing this notebook using the Kernels API.
        (cfg is a dictionary of config information, as specific in track_config.yaml)
        """
        # Pushing a kernel through the API fails if len(title) > 50. (b/120288024)
        title = self.title
        dev = cfg.get('development', False)
        return dict(
                id=self.slug,
                language='python',
                is_private=not cfg.get('public', not dev),
                # Path is relative to where kernel-metadata.json file will be written, which is
                #   notebooks/<track>/<cfg-tag>/kernels_api_metadata/<notebook-identifier>/kernel-metadata.json
                code_file="../../rendered/{}".format(self.filename),
                enable_gpu=self.enable_gpu,
                # Enable internet in development mode so we can pip install learntools
                # TODO: Actually, probably only needs to be turned on if we're in
                # development mode AND this is an exercise kernel.
                enable_internet=dev if self.enable_internet is None else self.enable_internet,
                kernel_type='notebook',
                title=title,
                dataset_sources=sorted(self.dataset_sources),
                competition_sources=sorted(self.competition_sources),
                kernel_sources=sorted(self.kernel_sources),
                keywords=sorted(self.keywords),
                docker_image_pinning_type="latest",
                )
