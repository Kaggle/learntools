# Purpose
The checking code and notebooks used in [Kaggle Learn](https://www.kaggle.com/learn) courses.

Everything here is open source, but these materials haven't been designed to work independently and likely aren't useful outside of Kaggle Learn.

# Structure
This repo is split into two types of material.
- The `learntools` folder contains a python package that provides feedback to users in Kaggle Learn courses. This package is further divided into
    - Modules for individual courses. For example, `learntools/python` is used to check exercises in the Python course. `learntools/machine_learning` is used to check exercises in the Machine Learning course.  And so on.
    - `core` provides the infrastructure for exercise checking. This is imported into the modules for each course.
- The `notebooks` subdirectory contains tools to simplify publishing courses on kaggle as well as the course materials themselves. The course materials are in notebooks. The notebooks for the python course are in `/notebooks/python/raw/*`. Replace python with another course name to find the materials for other courses.  The notebooks are processed in a templating system before being uploaded to kaggle, so the `raw` notebooks are hard to read. The README in `/notebooks` has instructions to convert `raw` notebooks to rendered notebooks (and to use the templating system more generally).

Some courses have notebooks in a subdirectory of the `learntools` package, reflecting the fact these notebooks were authored and edited outside our templating system.

# Running the tests

Run all tests against the staging image:

```
./test.sh
```

Run all tests against a specific image:

```
./test.sh -i gcr.io/kaggle-images/python:some-tag
```

Run only the tests for the `computer_vision` track:

```
./test.sh -t computer_vision
```

Run only the tests for the 1st exercise of the `computer_vision` track:

```
./test.sh -t computer_vision -n ex1
```