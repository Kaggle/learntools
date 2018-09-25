import os

import titlecase

def slugify(title, author):
    s = title.replace('(', '').replace(')', '').replace(',', '').replace(':', '').lower()
    tokens = s.split()
    return author + '/' + '-'.join(tokens)

class TrackMeta(object):

    def __init__(self, track, lessons_meta, nbs_meta):
        self.track = track
        self.lessons = [Lesson(**lmeta) for lmeta in lessons_meta]
        for lesson, next_lesson in zip(self.lessons, self.lessons[1:]):
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
                assert not hasattr(lesson, type)
                setattr(lesson, type, nb)
        self._resolve_kernel_deps()

    @classmethod
    def from_module(cls, module):
        return cls(module.track, module.lessons, module.notebooks)

    def get_notebook(self, fname):
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
    """
    - topic
    - next/prev?
    """
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
            assert lesson is not None
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
        dev = cfg.get('development', False)
        return dict(
                id=self.slug,
                language='python',
                is_private=not cfg.get('public', not dev),
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

