import os

import titlecase

def slugify(title, author):
    # NB: This was hacked together ad-hoc and probably still has some holes where it doesn't agree with Kernels logic.
    s = title.replace('(', '').replace(')', '').replace(',', '').replace(':', '').lower()
    tokens = s.split()
    return author + '/' + '-'.join(tokens)

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

    def __init__(self, track, lessons_meta, nbs_meta):
        self.track = track
        self.lessons = [Lesson(**lmeta) for lmeta in lessons_meta]
        # Add convenience next/prev pointers to lessons
        for lesson, next_lesson in zip(self.lessons, self.lessons[1:]):
            # TODO: Add next/prev getters to raise custom message for attempts
            # to access next of last lesson etc. for clarity
            lesson.next = next_lesson
            next_lesson.prev = lesson
        self.notebooks = []
        for nb_meta in nbs_meta:
            nb_meta = nb_meta.copy()
            nb_meta.setdefault('author', track['author_username'])
            lesson_idx = nb_meta.pop('lesson_idx', None)
            if lesson_idx is not None:
                lesson = self.lessons[lesson_idx]
                nb_meta['lesson'] = lesson
            nb = Notebook(**nb_meta)
            self.notebooks.append(nb)
            type = nb_meta['type']
            if type in ('tutorial', 'exercise'):
                assert not hasattr(lesson, type), "Can't have two {}s in one lesson".format(type)
                setattr(lesson, type, nb)
        self._resolve_kernel_deps()

    @classmethod
    def from_module(cls, module):
        return cls(module.track, module.lessons, module.notebooks)

    def get_notebook(self, fname):
        """Look up a Notebook object by its filename."""
        matches = [nb for nb in self.notebooks if nb.filename == fname]
        assert len(matches) <= 1, fname
        return matches[0]

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
    def __init__(self, topic):
        self.topic = topic

class Notebook(object):

    def __init__(self, filename, type, author=None, title=None, lesson=None,
            slug=None, scriptid=1, kernel_sources=(), dataset_sources=(),
            ):
        self.filename = filename
        self.stem, _ = os.path.splitext(os.path.basename(filename))
        assert type in ('tutorial', 'exercise', 'extra')
        self.type = type
        if title is None:
            assert lesson is not None, "Title attribute must be set if lesson_idx is absent"
            assert type in ('tutorial', 'exercise'), type
            self.title = '{}{}'.format(
                'Exercise: ' if type=='exercise' else '',
                titlecase.titlecase(lesson.topic)
                )
        else:
            self.title = title
        self.lesson = lesson
        if slug is None:
            assert author is not None
            self.slug = slugify(self.title, author)
        else:
            self.slug = slug
        self.scriptid = scriptid
        self.kernel_sources = list(kernel_sources)
        self.dataset_sources = list(dataset_sources)

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
        dev = cfg.get('development', False)
        return dict(
                id=self.slug,
                language='python',
                is_private=not cfg.get('public', not dev),
                # Path is relative to where kernel-metadata.json file will be written, which is
                #   notebooks/<track>/pushables/<notebook-identifier>/kernel-metadata.json
                code_file="../../rendered/" + self.filename,
                enable_gpu=False,
                # Enable internet in development mode so we can pip install learntools
                enable_internet=dev,
                kernel_type='notebook',
                title=self.title,
                dataset_sources=sorted(self.dataset_sources),
                kernel_sources=sorted(self.kernel_sources),
                competition_sources=[],
                )

