from github_contexts.github.enum import EventType
from github_contexts.github.payload.object.user import User

from github_contexts.property_dict import PropertyDict as _PropertyDict


class PerformedViaGitHubApp(_PropertyDict):

    def __init__(self, data: dict):
        """
        Parameters
        ----------
        data : dict
            The `performed_via_github_app` dictionary contained in the payload.
        """
        super().__init__(data)
        return

    @property
    def created_at(self) -> str | None:
        return self._data["created_at"]

    @property
    def description(self) -> str | None:
        return self._data["description"]

    @property
    def events(self) -> list[EventType]:
        return [EventType(event) for event in self._data.get("events", [])]

    @property
    def external_url(self) -> str | None:
        return self._data["external_url"]

    @property
    def html_url(self) -> str:
        return self._data["html_url"]

    @property
    def id(self) -> int | None:
        return self._data["id"]

    @property
    def name(self) -> str:
        return self._data["name"]

    @property
    def node_id(self) -> str:
        return self._data["node_id"]

    @property
    def owner(self) -> User | None:
        return User(self._data["owner"]) if self._data.get("owner") else None

    @property
    def permissions(self) -> dict | None:
        return self._data.get("permissions")

    @property
    def slug(self) -> str | None:
        return self._data.get("slug")

    @property
    def updated_at(self) -> str | None:
        return self._data["updated_at"]
