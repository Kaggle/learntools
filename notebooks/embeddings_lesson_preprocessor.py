import logging

import nbformat

from lesson_preprocessor import LearnLessonPreprocessor

PIP_INSTALL_HACK = True

class EmbeddingsLessonPreprocessor(LearnLessonPreprocessor):

    def preprocess(self, nb, resources):
        lt_meta = nb['metadata']['learntools_metadata']
        lesson_ix = lt_meta['lesson_index']
        if lesson_ix < 0:
            logging.warn("Aborting preprocessing for notebook with index {}".format(lesson_ix))
            return nb, resources
        nb, resources = super().preprocess(nb, resources)
        extra_pkgs = []
        if lt_meta['type'] == 'exercise':
            extra_pkgs.append('git+https://github.com/Kaggle/learntools.git@embeddings-v2')
        if lesson_ix == 2:
            extra_pkgs.append('gensim')
        self.pip_install_hack(nb, extra_pkgs)
        return nb, resources

    def pip_install_hack(self, nb, pkgs=()):
        if not pkgs:
            return
        extra_cells = []
        for pkg in pkgs:
            extra_cells.append(self.pip_install_cell(pkg))

        syspath_lines = [
                'import sys\n',
                "sys.path.append('/kaggle/working')",
        ]
        syspath_cell = self.make_code_cell(source=syspath_lines)
        extra_cells.append(syspath_cell)
        # Not sure if this works...
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
