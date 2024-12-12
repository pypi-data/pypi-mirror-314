import pytest

from cathodic_collect import utils


@pytest.mark.parametrize("name", ["test"])
def test_utils(name):
    res = utils.get_min_max_avg(name)
    assert res[0].endswith("_min")
    assert res[1].endswith("_max")
    assert res[2].endswith("_average")
