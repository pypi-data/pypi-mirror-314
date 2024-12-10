from github_contexts.property_dict import PropertyDict as _PropertyDict
from github_contexts.github.enum import UserType


class User(_PropertyDict):

    def __init__(self, user: dict):
        super().__init__(user)
        return

    @property
    def avatar_url(self) -> str | None:
        return self._data.get("avatar_url")

    @property
    def deleted(self) -> bool | None:
        return self._data.get("deleted")

    @property
    def email(self) -> str | None:
        return self._data.get("email")

    @property
    def events_url(self) -> str | None:
        return self._data.get("events_url")

    @property
    def followers_url(self) -> str | None:
        return self._data.get("followers_url")

    @property
    def following_url(self) -> str | None:
        return self._data.get("following_url")

    @property
    def gists_url(self) -> str | None:
        return self._data.get("gists_url")

    @property
    def gravatar_id(self) -> str | None:
        return self._data.get("gravatar_id")

    @property
    def html_url(self) -> str | None:
        return self._data.get("html_url")

    @property
    def id(self) -> int:
        return self._data["id"]

    @property
    def login(self) -> str:
        """GitHub username."""
        return self._data["login"]

    @property
    def name(self) -> str | None:
        return self._data.get("name")

    @property
    def node_id(self) -> str | None:
        return self._data.get("node_id")

    @property
    def organizations_url(self) -> str | None:
        return self._data.get("organizations_url")

    @property
    def received_events_url(self) -> str | None:
        return self._data.get("received_events_url")

    @property
    def repos_url(self) -> str | None:
        return self._data.get("repos_url")

    @property
    def site_admin(self) -> bool | None:
        return self._data.get("site_admin")

    @property
    def starred_url(self) -> str | None:
        return self._data.get("starred_url")

    @property
    def subscriptions_url(self) -> str | None:
        return self._data.get("subscriptions_url")

    @property
    def type(self) -> UserType | None:
        return UserType(self._data["type"]) if "type" in self._data else None

    @property
    def url(self) -> str | None:
        return self._data.get("url")

    @property
    def github_email(self) -> str:
        return f"{self.id}+{self.login}@users.noreply.github.com"
