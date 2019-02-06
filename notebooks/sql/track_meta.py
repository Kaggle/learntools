# See also examples/example_track/example_meta.py for a longer, commented example
track = dict(
    author_username='dansbecker',
    course_name='SQL',
    course_url='https://www.kaggle.com/learn/SQL'
)

lessons = [ {'topic': topic_name} for topic_name in
                    [
			'Getting Started with SQL and BigQuery',
			'Select, From & Where',
			'Group By, Having & Count',
			'Order By',
			'As & With',
			'Joining Data'
			]
            ]

notebooks = [
    dict(
        filename='tut1_intro.ipynb',
        lesson_idx=0,
        type='tutorial',
	dataset_sources = ["hacker-news/hacker-news"],
        ),
    dict(
        filename='ex1_intro.ipynb',
        lesson_idx=0,
        type='exercise',
	dataset_sources = ["hacker-news/hacker-news",
			  "chicago/chicago-crime"],
	scriptid=1058477
        ),
    dict(
	filename='tut2_select.ipynb',
	lesson_idx=1,
	type='tutorial',
	dataset_sources = ["hacker-news/hacker-news", "open-aq/openaq"],
	),
    dict(
        filename='ex2_select.ipynb',
        lesson_idx=1,
        type='exercise',
	scriptid=681989,
	dataset_sources = ["hacker-news/hacker-news", "open-aq/openaq"],
        ),
    dict(
        filename='tut3_groupby.ipynb',
        lesson_idx=2,
        type='tutorial',
	dataset_sources = ["hacker-news/hacker-news"],
    ),
    dict(
        filename='ex3_groupby.ipynb',
        lesson_idx=2,
        type='exercise',
	scriptid=682058,
	dataset_sources = [
	"hacker-news/hacker-news"
	  ],
    ),
    dict(
        filename='tut4_orderby.ipynb',
        lesson_idx=3,
        type='tutorial',
	dataset_sources = [
    "usdot/nhtsa-traffic-fatalities"
	  ],
    ),
    dict(
        filename='ex4_orderby.ipynb',
        lesson_idx=3,
        type='exercise',
	scriptid=682087,
	dataset_sources = ["usdot/nhtsa-traffic-fatalities", "theworldbank/world-bank-intl-education"],
    ),
    dict(
        filename='tut5_as_with.ipynb',
        lesson_idx=4,
        type='tutorial',
	dataset_sources = ["bigquery/bitcoin-blockchain"],
    ),
    dict(
        filename='ex5_as_with.ipynb',
        lesson_idx=4,
        type='exercise',
	scriptid=682113,
       	dataset_sources = ["chicago/chicago-taxi-trips-bq", "bigquery/bitcoin-blockchain"],
 ),
    dict(
        filename='tut6_joining.ipynb',
        lesson_idx=5,
        type='tutorial',
	dataset_sources = ["github/github-repos"],
        ),
    dict(filename='ex6_joining.ipynb',
        lesson_idx=5,
        type='exercise',
	dataset_sources = ["stackoverflow/stackoverflow"],
	scriptid=682118,
        ),
]
