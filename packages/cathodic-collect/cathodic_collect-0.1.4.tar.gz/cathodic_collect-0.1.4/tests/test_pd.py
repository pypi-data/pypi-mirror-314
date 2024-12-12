import pandas as pd


def test_pd_to_se():
    df = pd.DataFrame({"name": ["john", "svtter"], "gender": ["male", "male"]})
    df = df[df["name"] == "svtter"]
    assert not df.empty
