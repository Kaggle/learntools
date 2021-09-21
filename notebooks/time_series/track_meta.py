# See also examples/example_track/track_meta.py for a longer, commented example
track = dict(
    author_username="ryanholbrook",
    course_name="Time Series",
    course_url="https://www.kaggle.com/learn/time-series",
    course_forum_url="https://www.kaggle.com/learn-forum",
)

TOPICS = [
    "Linear Regression with Time Series",  # 1
    "Trend",  # 2
    "Seasonality",  # 3
    "Time Series as Features",  # 4
    "Hybrid Models",  # 5
    "Forecasting with Machine Learning",  # 6
]
lessons = [{"topic": topic_name} for topic_name in TOPICS]

notebooks = [
    dict(filename="tut1.ipynb", lesson_idx=0, type="tutorial"),
    dict(filename="ex1.ipynb", lesson_idx=0, type="exercise", scriptid=19615998),
    dict(filename="tut2.ipynb", lesson_idx=1, type="tutorial"),
    dict(filename="ex2.ipynb", lesson_idx=1, type="exercise", scriptid=19616015),
    dict(filename="tut3.ipynb", lesson_idx=2, type="tutorial"),
    dict(filename="ex3.ipynb", lesson_idx=2, type="exercise", scriptid=19615991),
    dict(filename="tut4.ipynb", lesson_idx=3, type="tutorial"),
    dict(filename="ex4.ipynb", lesson_idx=3, type="exercise", scriptid=19616002),
    dict(filename="tut5.ipynb", lesson_idx=4, type="tutorial"),
    dict(filename="ex5.ipynb", lesson_idx=4, type="exercise", scriptid=19616007),
    dict(filename="tut6.ipynb", lesson_idx=5, type="tutorial"),
    dict(filename="ex6.ipynb", lesson_idx=5, type="exercise", scriptid=20667477),
]
for nb in notebooks:
    nb["dataset_sources"] = ["ryanholbrook/ts-course-data"]
    nb["competition_sources"] = ["store-sales-time-series-forecasting"]
