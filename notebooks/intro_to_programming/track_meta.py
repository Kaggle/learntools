track = dict(
    author_username="alexisbcook",
    course_name="Intro to Programming",
    course_url="https://www.kaggle.com/learn/intro-to-programming",
    course_forum_url=""
)

TOPICS = [
    "Arithmetic and Variables",  # 1
    "Functions",  # 2
    "Data Types",  # 3
    "Conditions and Conditional Statements",  # 4
    "Intro to Lists",  # 5
]
lessons = [{"topic": topic_name} for topic_name in TOPICS]

notebooks = [
    dict(filename="tut1.ipynb", lesson_idx=0, type="tutorial"),      # 25258229
    dict(filename="ex1.ipynb", lesson_idx=0, type="exercise", scriptid=25258219),
    dict(filename="tut2.ipynb", lesson_idx=1, type="tutorial"),      # 25258223
    dict(filename="ex2.ipynb", lesson_idx=1, type="exercise", scriptid=25258227),
    dict(filename="tut3.ipynb", lesson_idx=2, type="tutorial"),      # 25258222
    dict(filename="ex3.ipynb", lesson_idx=2, type="exercise", scriptid=25258226),
    dict(filename="tut4.ipynb", lesson_idx=3, type="tutorial"),      # 25880617
    dict(filename="ex4.ipynb", lesson_idx=3, type="exercise", scriptid=25880622),
    dict(filename="tut5.ipynb", lesson_idx=4, type="tutorial"),      # 26034860
    dict(filename="ex5.ipynb", lesson_idx=4, type="exercise", scriptid=26034864),
]

for nb in notebooks:
    if nb['filename'] == 'ex1.ipynb':
        nb['competition_sources'] = ["titanic"]
