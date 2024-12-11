import perst


def test_schema(tmp_path):
    pst = perst.schema({
        'attrs': {
            'hosts': {'type': 'elems', 'path': tmp_path / 'data.json'},
        },
    })
    assert isinstance(pst.hosts, perst.elems)
