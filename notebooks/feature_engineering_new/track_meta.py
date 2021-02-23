track = dict(
    author_username="ryanholbrook",
    course_name="Feature Engineering",
    course_url="https://www.kaggle.com/learn/feature-engineering",
    course_forum_url="https://www.kaggle.com/learn-forum/221677",
)

TOPICS = [
    "What is Feature Engineering",  # 1
    "Mutual Information",  # 2
    "Creating Features",  # 3
    "Clustering with k-Means",  # 4
    "Principal Component Analysis",  # 5
    "Target Encoding",  # 6
    "Feature Engineering for House Prices",  # Bonus
]
lessons = [{"topic": topic_name} for topic_name in TOPICS]

notebooks = [
    dict(filename="tut1.ipynb", lesson_idx=0, type="tutorial"),
    #dict(filename="ex1.ipynb", lesson_idx=0, type="exercise", scriptid=14393915),
    dict(filename="tut2.ipynb", lesson_idx=1, type="tutorial"),
    dict(filename="ex2.ipynb", lesson_idx=1, type="exercise", scriptid=14393925),
    dict(filename="tut3.ipynb", lesson_idx=2, type="tutorial"),
    dict(filename="ex3.ipynb", lesson_idx=2, type="exercise", scriptid=14393912),
    dict(filename="tut4.ipynb", lesson_idx=3, type="tutorial"),
    dict(filename="ex4.ipynb", lesson_idx=3, type="exercise", scriptid=14393920),
    dict(filename="tut5.ipynb", lesson_idx=4, type="tutorial"),
    dict(filename="ex5.ipynb", lesson_idx=4, type="exercise", scriptid=14393921),
    dict(filename="tut6.ipynb", lesson_idx=5, type="tutorial"),
    dict(filename="ex6.ipynb", lesson_idx=5, type="exercise", scriptid=14393917),
]
for nb in notebooks:
    nb["dataset_sources"] = ["ryanholbrook/fe-course-data"]

notebooks.append(
    dict(
        filename="tut_bonus.ipynb",
        lesson_idx=6,
        type="tutorial",
        competition_sources=["house-prices-advanced-regression-techniques"],
    )
)
