track = dict(
    author_username="",
    course_name="Feature Engineering",
    course_url="https://www.kaggle.com/learn/feature-engineering",
    course_forum_url="https://www.kaggle.com/learn-forum/",
)

TOPICS = [
    "What is Feature Engineering",  # 1
    "Feature Utility",  # 2
    "Creating Features",  # 3
    "Clustering with k-Means",  # 4
    "Principal Component Analysis",  # 5
    "Target Encoding",  # 6
    "Getting Started with House Prices",  # Bonus
]
lessons = [{"topic": topic_name} for topic_name in TOPICS]

notebooks = [
    dict(filename="tut1.ipynb", lesson_idx=0, type="tutorial", scriptid=1),
    dict(filename="ex1.ipynb", lesson_idx=0, type="exercise", scriptid=1),
    dict(filename="tut2.ipynb", lesson_idx=1, type="tutorial", scriptid=1),
    dict(filename="ex2.ipynb", lesson_idx=1, type="exercise", scriptid=1),
    dict(filename="tut3.ipynb", lesson_idx=2, type="tutorial", scriptid=1),
    dict(filename="ex3.ipynb", lesson_idx=2, type="exercise", scriptid=1),
    dict(filename="tut4.ipynb", lesson_idx=3, type="tutorial", scriptid=1),
    dict(filename="ex4.ipynb", lesson_idx=3, type="exercise", scriptid=1),
    dict(filename="tut5.ipynb", lesson_idx=4, type="tutorial", scriptid=1),
    dict(filename="ex5.ipynb", lesson_idx=4, type="exercise", scriptid=1),
    dict(filename="tut6.ipynb", lesson_idx=5, type="tutorial", scriptid=1),
    dict(filename="ex6.ipynb", lesson_idx=5, type="exercise", scriptid=1),
]
for nb in notebooks:
    nb["dataset_sources"] = ["ryanholbrook/fe-course-data"]

notebooks.append(
    dict(
        filename="tut_bonus.ipynb",
        lesson_idx=6,
        type="tutorial",
        scriptid=1,
        competition_sources=["house-prices-advanced-regression-techniques"],
    )
)
