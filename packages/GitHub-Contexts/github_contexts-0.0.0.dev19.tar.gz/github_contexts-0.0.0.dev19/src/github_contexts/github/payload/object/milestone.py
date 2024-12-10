"""GitHub Milestone Object"""


from github_contexts.github.payload.object.user import User
from github_contexts.github.enum import State

from github_contexts.property_dict import PropertyDict as _PropertyDict


class Milestone(_PropertyDict):
    """GitHub Milestone Object"""

    def __init__(self, data: dict):
        """
        Parameters
        ----------
        data : dict
            The `milestone` dictionary contained in the payload.
        """
        super().__init__(data)
        return

    @property
    def closed_at(self) -> str | None:
        return self._data["closed_at"]

    @property
    def closed_issues(self) -> int:
        return self._data["closed_issues"]

    @property
    def created_at(self) -> str:
        return self._data["created_at"]

    @property
    def creator(self) -> User | None:
        return User(self._data["creator"]) if self._data.get("creator") else None

    @property
    def description(self) -> str | None:
        return self._data["description"]

    @property
    def due_on(self) -> str | None:
        return self._data["due_on"]

    @property
    def html_url(self) -> str:
        return self._data["html_url"]

    @property
    def id(self) -> int:
        return self._data["id"]

    @property
    def labels_url(self) -> str:
        return self._data["labels_url"]

    @property
    def node_id(self) -> str:
        return self._data["node_id"]

    @property
    def number(self) -> int:
        return self._data["number"]

    @property
    def open_issues(self) -> int:
        return self._data["open_issues"]

    @property
    def state(self) -> State:
        return State(self._data["state"])

    @property
    def title(self) -> str:
        return self._data["title"]

    @property
    def updated_at(self) -> str:
        return self._data["updated_at"]

    @property
    def url(self) -> str:
        return self._data["url"]
