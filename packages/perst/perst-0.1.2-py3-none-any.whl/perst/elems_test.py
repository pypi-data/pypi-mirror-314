import pytest

import perst


@pytest.fixture
def elems(tmp_path):
    yield perst.elems(tmp_path / 'data.json')


class Test_add:

    def test_add(self, elems):
        elem = {'id': 1, 'name': 'foo'}
        elems.add(elem)
        assert elems[1] == elem


class Test_update:

    def test_update_by_whole_data(self, elems):
        self.prepare(elems)
        elem = {'id': 1, 'name': 'bar', 'age': 3}
        elems.update(elem)
        assert elems[1] == elem

    def test_update_by_partial_data(self, elems):
        self.prepare(elems)
        elems.update(1, {'name': 'bar'})
        assert elems[1]['name'] == 'bar'
        assert elems[1]['age'] == 3

    def test_update_identity(self, elems):
        self.prepare(elems)
        elems.update(1, {'id': 2, 'name': 'bar'})
        assert elems.get(1) is None
        assert elems[2]['name'] == 'bar'
        assert elems[2]['age'] == 3

    def test_update_by_decorator(self, elems):
        self.prepare(elems)

        @elems.update(1)
        def _(elem):
            elem['name'] = 'bar'

        assert elems[1]['name'] == 'bar'

    def prepare(self, elems):
        elem = {'id': 1, 'name': 'foo', 'age': 3}
        elems.add(elem)


class Test_remove:

    def test_remove_by_key(self, elems):
        self.prepare(elems)
        elems.remove(1)
        assert elems.get(1) is None

    def test_remove_by_elem(self, elems):
        self.prepare(elems)
        elems.remove(elems[1])
        assert elems.get(1) is None

    def prepare(self, elems):
        elem = {'id': 1, 'name': 'foo'}
        elems.add(elem)


class Test_iter_and_len:

    def test_iter(self, elems):
        assert len(elems) == 0

        _elems = {
            d['id']: d for d in [{'id': 1, 'name': 'foo'}, {'id': 2, 'name': 'bar'}]
        }
        for _elem in _elems.values():
            elems.add(_elem)

        assert len(elems) == len(_elems)
        for elem in elems:
            assert elem == _elems[elem['id']]


class Test_bool:

    def test_empty(self, elems):
        assert not elems

    def test_non_empty(self, elems):
        elems.add({'id': 1, 'name': 'foo'})
        assert elems
