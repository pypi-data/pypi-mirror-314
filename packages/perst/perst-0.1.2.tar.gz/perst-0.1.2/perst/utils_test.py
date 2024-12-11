from pathlib import Path

from perst import utils


def test_dump_and_load(tmp_path):
    data = {'foo': 3, 'bar': 5}
    fpath = Path(tmp_path / 'data.json')

    utils.dump(data, fpath)
    assert utils.load(fpath) == data
