`learntools.core` contains the basic elements of exercise checking, shared across all Learn micro-courses and exercises.

The course-specific directories subclass ProblemViews from `learntools.core`. Examples of types of ProblemViews are `CodingProblem`, `EqualityCheckProblem` and `ThoughtExperiment`.

The `ProblemView` provides an interface that wraps a `learntools.core.Problem`. The interface it provides generally includes `hint()`, `check()` and `solution()` methods. The behavior of these is determined by the values for `var`, `_hint` and `_solution` in the checking code written by the couse author.

