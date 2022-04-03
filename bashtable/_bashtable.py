from typing import Any, NamedTuple


class Pair(NamedTuple):
    key: Any
    value: Any


class BashTable:
    """A HashTable implementation for my own learning"""

    @classmethod
    def from_dict(cls, dictionary: dict, capacity: int = None):
        bash_table = cls(capacity or len(dictionary) * 10)
        for key, value in dictionary.items():
            bash_table[key] = value
        return bash_table

    def __init__(self, capacity: int = None) -> None:
        """Initialize a BashTable of capacity size"""
        if capacity < 1:
            raise ValueError("Capacity must be a positive number")
        self._slots = capacity * [None]

    def __len__(self) -> int:
        return len(self.pairs)

    def __setitem__(self, key: Any, value: Any) -> None:
        self._slots[self._index(key)] = Pair(key, value)

    def __getitem__(self, key: Any) -> Any:
        pair = self._slots[self._index(key)]
        if pair is None:
            raise KeyError(key)
        return pair.value

    def __delitem__(self, key: Any) -> None:
        if key in self:
            self._slots[self._index(key)] = None
        else:
            raise KeyError(key)

    def __contains__(self, key: Any) -> bool:
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True

    def __iter__(self):
        yield from self.keys

    def __str__(self):
        pairs = []
        for key, value in self.pairs:
            pairs.append(f"{key!r}: {value!r}")
        return "{" + ", ".join(pairs) + "}"

    def __repr__(self):
        cls = self.__class__.__name__
        return f"{cls}.from_dict({str(self)})"

    def __eq__(self, other):
        if self is other:
            return True
        if type(self) is not type(other):
            return False
        return set(self.pairs) == set(other.pairs)

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def copy(self):
        return BashTable.from_dict(dict(self.pairs), self.capacity)

    @property
    def pairs(self):
        return {pair for pair in self._slots if pair}

    @property
    def values(self):
        return [pair.value for pair in self.pairs]

    @property
    def keys(self):
        return {pair.key for pair in self.pairs}

    @property
    def capacity(self):
        return len(self._slots)

    def _index(self, key: Any) -> int:
        """Returns length modulated hash of input key"""
        return hash(key) % self.capacity
