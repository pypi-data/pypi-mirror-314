from github_contexts.property_dict import PropertyDict as _PropertyDict


class Label(_PropertyDict):

    def __init__(self, label: dict):
        super().__init__(label)
        return

    @property
    def color(self) -> str:
        return self._data["color"]

    @property
    def default(self) -> bool:
        return self._data["default"]

    @property
    def description(self) -> str | None:
        return self._data["description"]

    @property
    def id(self) -> int:
        return self._data["id"]

    @property
    def name(self) -> str:
        return self._data["name"]

    @property
    def node_id(self) -> str:
        return self._data["node_id"]

    @property
    def url(self) -> str:
        return self._data["url"]