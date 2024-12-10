from github_contexts.property_dict import PropertyDict as _PropertyDict


class CommitAuthor(_PropertyDict):

    def __init__(self, author: dict):
        super().__init__(author)
        return

    @property
    def date(self) -> str | None:
        return self._data.get("date")

    @property
    def email(self) -> str | None:
        return self._data.get("email")

    @property
    def name(self) -> str | None:
        """The Git author's name."""
        return self._data.get("name")

    @property
    def username(self) -> str | None:
        return self._data.get("username")
