from github_contexts.property_dict import PropertyDict as _PropertyDict


class Reactions(_PropertyDict):

    def __init__(self, reactions: dict):
        super().__init__(reactions)
        return

    @property
    def plus_one(self) -> int:
        return self._data["+1"]

    @property
    def minus_one(self) -> int:
        return self._data["-1"]

    @property
    def confused(self) -> int:
        return self._data["confused"]

    @property
    def eyes(self) -> int:
        return self._data["eyes"]

    @property
    def heart(self) -> int:
        return self._data["heart"]

    @property
    def hooray(self) -> int:
        return self._data["hooray"]

    @property
    def laugh(self) -> int:
        return self._data["laugh"]

    @property
    def rocket(self) -> int:
        return self._data["rocket"]

    @property
    def total_count(self) -> int:
        return self._data["total_count"]

    @property
    def url(self) -> str:
        return self._data["url"]
