track = dict(
    author_username="alexisbcook",
    course_name="Intro to Programming",
    course_url="https://www.kaggle.com/learn/intro-to-programming",
)

TOPICS = [
    "Arithmetic and Variables",  # 1
    "Functions",  # 2
    #"Data Types",  # 3
    #"Conditions and Conditional Statements",  # 4
    #"Lists",  # 5
    #"Loops",  # 6
]
lessons = [{"topic": topic_name} for topic_name in TOPICS]

notebooks = [
    dict(filename="tut1.ipynb", lesson_idx=0, type="tutorial"),
    dict(filename="ex1.ipynb", lesson_idx=0, type="exercise", scriptid=-1),
    dict(filename="tut2.ipynb", lesson_idx=1, type="tutorial"),
    #dict(filename="ex2.ipynb", lesson_idx=1, type="exercise", scriptid=-1),
    #dict(filename="tut3.ipynb", lesson_idx=2, type="tutorial"),
    #dict(filename="ex3.ipynb", lesson_idx=2, type="exercise", scriptid=-1),
    #dict(filename="tut4.ipynb", lesson_idx=3, type="tutorial"),
    #dict(filename="ex4.ipynb", lesson_idx=3, type="exercise", scriptid=-1),
    #dict(filename="tut5.ipynb", lesson_idx=4, type="tutorial"),
    #dict(filename="ex5.ipynb", lesson_idx=4, type="exercise", scriptid=-1),
    #dict(filename="tut6.ipynb", lesson_idx=5, type="tutorial"),
    #dict(filename="ex6.ipynb", lesson_idx=5, type="exercise", scriptid=-1),
]

# add dataset sources

