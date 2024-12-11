from pathlib import Path
from typing import Optional

from perst import utils


class elems:

    def __init__(self, path: str, id: str = 'id', **__):
        self._id = id
        self._data_path = Path(path)
        self._name = self._data_path.stem
        self._meta_path = self._data_path.parent / f'{self._name}.meta.json'
        self._data = self._ensure_loaded()

    def add(self, elem: dict) -> bool:
        assert isinstance(elem, dict)
        elem_id = elem[self._id]
        if elem_id in self._data:
            return False
        else:
            self._data[elem_id] = elem
            utils.dump(self._data, self._data_path)
            return True

    def update(self, *args) -> bool:
        """
        Sample usages:

            # update by whole data
            elems.update({'id': 1, 'name': 'foo', 'age': 35})

            # update by key and partial data
            elems.update(1, {'name': 'foo'})

            # update by decorator
            @elems.update
            def _(elem):
                elem['name'] = 'foo'
        """
        if len(args) == 1:
            if not isinstance(args[0], dict):
                elem_id = args[0]
                def deco(update_func):
                    elem = self[elem_id]
                    try:
                        update_func(elem)
                    except Exception:
                        pass
                    else:
                        self._update_by_elem(elem)
                return deco
            else:
                self._update_by_elem(args[0])
        elif len(args) == 2:
            elem_id, update = args
            if self._id in update and update[self._id] != elem_id:
                elem = self[elem_id]
                self.remove(elem_id)
                elem.update(update)
                self.add(elem)
            else:
                elem = self[elem_id]
                elem.update(update)
                self._update_by_elem(elem)
        else:
            raise TypeError(f'invalid update arguments {args}')

    def _update_by_elem(self, elem: dict) -> bool:
        assert isinstance(elem, dict)
        elem_id = elem[self._id]
        if elem_id in self._data:
            self._data[elem_id] = elem
            utils.dump(self._data, self._data_path)
            return True
        else:
            return False

    def remove(self, elem: any) -> bool:
        if isinstance(elem, dict):
            elem_id = elem[self._id]
        else:
            elem_id = elem

        if elem_id in self._data:
            del self._data[elem_id]
            utils.dump(self._data, self._data_path)
            return True
        else:
            return False

    def get(self, elem_id: any) -> Optional[any]:
        return self._data.get(elem_id)

    def __getitem__(self, elem_id: any) -> any:
        return self._data[elem_id]

    def __iter__(self):
        self._ensure_loaded()
        yield from self._data.values()

    def __len__(self):
        return len(self._data)

    def __bool__(self):
        return bool(self._data)

    def _ensure_loaded(self):
        if self._data_path.exists():
            return utils.load(self._data_path)
        else:
            return {}
