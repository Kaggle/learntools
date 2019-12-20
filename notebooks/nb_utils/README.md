The natural entry point into this directory is `lesson_preprocessor`. It provides a `LearnLessonPreprocessor` that goes through a notebook's cells sequentially with the `for cell in nb.cells` loop. 

The primary action in each cell is applying macros. `add_header_and_footer()` in that file is a good example of how you can take actions outside the cell-at-a-time loop. Some macros are defined in that file (they are the capitalized methods). Other types of macros are in the `line_macros.py` file. The comments in those files help distinguish which type of macro goes in each file.

The other higher-level file in this directory is `track_metadata`, which is important for creating the Kaggle CLI metadata yaml files we use to push content to kaggle.


