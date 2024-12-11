import pandas as pd


def test_list():
    res = pd.Series([1, 2, 3])
    assert list(res) == [1, 2, 3]
