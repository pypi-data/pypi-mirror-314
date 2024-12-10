from github_contexts.property_dict import PropertyDict as _PropertyDict


class Permissions(_PropertyDict):

    def __init__(self, permissions: dict):
        super().__init__(permissions)
        return

    @property
    def admin(self) -> bool:
        return self._data["admin"]

    @property
    def maintain(self) -> bool | None:
        return self._data.get("maintain")

    @property
    def pull(self) -> bool:
        return self._data["pull"]

    @property
    def push(self) -> bool:
        return self._data["push"]

    @property
    def triage(self) -> bool | None:
        return self._data.get("triage")
