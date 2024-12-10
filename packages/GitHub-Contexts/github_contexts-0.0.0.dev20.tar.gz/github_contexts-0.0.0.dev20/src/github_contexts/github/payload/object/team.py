from __future__ import annotations
from typing import Union

from github_contexts.property_dict import PropertyDict as _PropertyDict
from github_contexts.github.enum import TeamPrivacy


class Team(_PropertyDict):

    def __init__(self, team: dict):
        super().__init__(team)
        return

    @property
    def deleted(self) -> bool | None:
        return self._data.get("deleted")

    @property
    def description(self) -> str | None:
        return self._data.get("description")

    @property
    def html_url(self) -> str | None:
        return self._data.get("html_url")

    @property
    def id(self) -> int:
        return self._data["id"]

    @property
    def members_url(self) -> str | None:
        return self._data.get("members_url")

    @property
    def name(self) -> str:
        return self._data["name"]

    @property
    def node_id(self) -> str:
        return self._data["node_id"]

    @property
    def parent(self) -> Union["Team", None]:
        return Team(self._data["parent"]) if self._data.get("parent") else None

    @property
    def permission(self) -> str | None:
        return self._data.get("permission")

    @property
    def privacy(self) -> TeamPrivacy | None:
        return TeamPrivacy(self._data["privacy"]) if self._data.get("privacy") else None

    @property
    def repositories_url(self) -> str | None:
        return self._data.get("repositories_url")

    @property
    def slug(self) -> str | None:
        return self._data.get("slug")

    @property
    def url(self) -> str | None:
        return self._data.get("url")