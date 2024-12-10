import json
from pathlib import Path
from typing import Optional


default_data_fpath = './perst.data.json'


def dump(data, fpath: str = default_data_fpath):
    with Path(fpath).open('w') as f:
        json.dump(data, f)


def load(fpath: str = default_data_fpath):
    with Path(fpath).open() as f:
        return json.load(f)


class elems:

    def __init__(self, path: str, key: str = 'key'):
        self._key = key
        self._data_path = Path(path)
        self._name = self._data_path.stem
        self._meta_path = self._data_path.parent / f'{self._name}.meta.json'
        self._data = self._ensure_loaded()

    def add(self, elem: dict) -> bool:
        assert isinstance(elem, dict)
        key = elem[self._key]
        if key in self._data:
            return False
        else:
            self._data[key] = elem
            dump(self._data, self._data_path)
            return True

    def update(self, *args) -> bool:
        if len(args) == 1:
            if callable(args[0]):
                raise NotImplementedError('update deco')
            else:
                self._update_by_elem(args[0])
        elif len(args) == 2:
            key, update = args
            elem = self[key]
            elem.update(update)
            self._update_by_elem(elem)
        else:
            raise TypeError(f'invalid update arguments {args}')

    def _update_by_elem(self, elem: dict) -> bool:
        assert isinstance(elem, dict)
        key = elem[self._key]
        if key in self._data:
            self._data[key] = elem
            dump(self._data, self._data_path)
            return True
        else:
            return False

    def remove(self, elem: dict) -> bool:
        assert isinstance(elem, dict)
        key = elem[self._key]
        if key in self._data:
            del self._data[key]
            dump(self._data, self._data_path)
            return True
        else:
            return False

    def __iter__(self):
        self._ensure_loaded()
        yield from self._data.values()

    def __len__(self):
        return len(self._data)

    def __bool__(self):
        return bool(self._data)

    def __getitem__(self, key: str) -> Optional[dict]:
        return self._data.get(key)

    def _ensure_loaded(self):
        if self._data_path.exists():
            return load(self._data_path)
        else:
            return {}
