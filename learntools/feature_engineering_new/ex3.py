import pandas as pd

from learntools.core import *

df = pd.read_csv("../input/fe-course-data/ames.csv")


class Q1(CodingProblem):
    _hint = """Your code should look something like:
```python
X_1["LivLotRatio"] = ____ / ____
X_1["Spaciousness"] = (____ + ____) / ____
X_1["TotalOutsideSF"] = ____ + ____ + ____ + ____ + ____
```
"""
    _solution = CS(
        """
X_1["LivLotRatio"] = df.GrLivArea / df.LotArea
X_1["Spaciousness"] = (df.FirstFlrSF + df.SecondFlrSF) / df.TotRmsAbvGrd
X_1["TotalOutsideSF"] = df.WoodDeckSF + df.OpenPorchSF + df.EnclosedPorch + df.Threeseasonporch + df.ScreenPorch
"""
    )
    _vars = ["X_1"]

    def check(self, X_1):
        X_solution = pd.DataFrame()
        X_solution["LivLotRatio"] = df.GrLivArea / df.LotArea
        X_solution["Spaciousness"] = (
            df.FirstFlrSF + df.SecondFlrSF
        ) / df.TotRmsAbvGrd
        X_solution["TotalOutsideSF"] = (
            df.WoodDeckSF
            + df.OpenPorchSF
            + df.EnclosedPorch
            + df.Threeseasonporch
            + df.ScreenPorch
        )
        assert len(X_solution.columns) == len(
            X_1.columns
        ), f"Columns are incorrect. You should have {list(X_solution.columns)}. You gave {list(X_1.columns)}"
        assert sorted(X_solution.columns) == sorted(
            X_1.columns
        ), f"Columns are incorrect. You should have {list(X_solution.columns)}. You gave {list(X_1.columns)}"
        assert (
            X_solution.LivLotRatio == X_1.LivLotRatio
        ).all(), "`LivLotRatio` is incorrect."
        assert (
            X_solution.Spaciousness == X_1.Spaciousness
        ).all(), "`Spaciousness` is incorrect."
        assert (
            X_solution.TotalOutsideSF == X_1.TotalOutsideSF
        ).all(), "`TotalOutsideSF` is incorrect."


class Q2(CodingProblem):
    _hint = """Your code should look something like:
```python
X_2 = pd.get_dummies(____, prefix="Bldg")
X_2 = X_2.mul(____, axis=0)
```
"""
    _solution = CS(
        """
X_2 = pd.get_dummies(df.BldgType, prefix="Bldg")
X_2 = X_2.mul(df.GrLivArea, axis=0)
"""
    )
    _var = "X_2"

    def check(self, X_2):
        X_solution = pd.get_dummies(df.BldgType, prefix="Bldg")
        X_solution = X_solution.mul(df.GrLivArea, axis=0)
        assert (X_solution == X_2).all().all()


class Q3(CodingProblem):
    _hint = """Your code should look someting like:
```python
X_3 = pd.DataFrame()

X_3["PorchTypes"] = df[[
    ____,
    ____,
    ____,
    ____,
    ____,
]].____.sum(axis=1)
```
"""
    _solution = CS(
        """
X_3 = pd.DataFrame()

X_3["PorchTypes"] = df[[
    "WoodDeckSF",
    "OpenPorchSF",
    "EnclosedPorch",
    "Threeseasonporch",
    "ScreenPorch",
]].gt(0.0).sum(axis=1)
"""
    )
    _var = "X_3"

    def check(self, X_3):
        X_solution = pd.DataFrame()

        X_solution["PorchTypes"] = (
            df[
                [
                    "WoodDeckSF",
                    "OpenPorchSF",
                    "EnclosedPorch",
                    "Threeseasonporch",
                    "ScreenPorch",
                ]
            ]
            .gt(0.0)
            .sum(axis=1)
        )
        assert len(X_solution.columns) == len(
            X_3.columns
        ), f"Columns are incorrect. You should have {list(X_solution.columns)}. You gave {list(X_3.columns)}"
        assert sorted(X_solution.columns) == sorted(
            X_3.columns
        ), f"Columns are incorrect. You should have {list(X_solution.columns)}. You gave {list(X_3.columns)}"
        assert (X_solution == X_3).all().all()


class Q4(CodingProblem):
    _hint = """Your code should look something like:
```python
X_4 = pd.DataFrame()

X_4["MSClass"] = df.____.str.____(____, n=1, expand=True)[____]
```
"""
    _solution = CS(
        """
X_4 = pd.DataFrame()

X_4["MSClass"] = df.MSSubClass.str.split("_", n=1, expand=True)[0]
"""
    )
    _var = "X_4"

    def check(self, X_4):
        X_solution = pd.DataFrame()
        X_solution["MSClass"] = df.MSSubClass.str.split("_", n=1, expand=True)[
            0
        ]
        assert len(X_solution.columns) == len(
            X_4.columns
        ), f"Columns are incorrect. You should have {list(X_solution.columns)}. You gave {list(X_4.columns)}"
        assert sorted(X_solution.columns) == sorted(
            X_4.columns
        ), f"Columns are incorrect. You should have {list(X_solution.columns)}. You gave {list(X_4.columns)}"
        assert (X_solution.MSClass == X_4.MSClass).all()


class Q5(CodingProblem):
    _hint = """Your code should look something like:
```python
X_5 = pd.DataFrame()

X_5["MedNhbdArea"] = df.____("Neighborhood")["____"].transform(____)
```
"""
    _solution = CS(
        """
X_5 = pd.DataFrame()

X_5["MedNhbdArea"] = df.groupby("Neighborhood")["GrLivArea"].transform("median")
"""
    )
    _var = "X_5"

    def check(self, X_5):
        X_solution = pd.DataFrame()
        X_solution["MedNhbdArea"] = df.groupby("Neighborhood")[
            "GrLivArea"
        ].transform("median")
        assert len(X_solution.columns) == len(
            X_5.columns
        ), f"Columns are incorrect. You should have {list(X_solution.columns)}. You gave {list(X_5.columns)}"
        assert sorted(X_solution.columns) == sorted(
            X_5.columns
        ), f"Columns are incorrect. You should have {list(X_solution.columns)}. You gave {list(X_5.columns)}"
        assert (X_solution.MedNhbdArea == X_5.MedNhbdArea).all()


qvars = bind_exercises(globals(), [Q1, Q2, Q3, Q4, Q5], var_format="q_{n}")
__all__ = list(qvars)
