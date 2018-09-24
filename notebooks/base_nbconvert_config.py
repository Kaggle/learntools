c = get_config()

# XXX: I forget what this signifies?
c.NbConvertApp.notebooks = ['*.ipynb']
c.Exporter.preprocessors = ['lesson_preprocessor.LearnLessonPreprocessor']

#c.LearnLessonPreprocessor.lessons_metadata = lessons_meta
#c.EmbeddingsLessonPreprocessor.lessons_metadata = lessons_meta
