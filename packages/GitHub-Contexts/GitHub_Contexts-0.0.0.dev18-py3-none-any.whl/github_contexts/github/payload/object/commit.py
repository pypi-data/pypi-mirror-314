from github_contexts.property_dict import PropertyDict as _PropertyDict
from github_contexts.github.payload.object.commit_author import CommitAuthor


class Commit(_PropertyDict):

    def __init__(self, commit: dict):
        super().__init__(commit)
        return

    @property
    def added(self) -> list[str]:
        """Paths of added files."""
        return self._data.get("added", [])

    @property
    def author(self) -> CommitAuthor:
        """Git author information."""
        return CommitAuthor(self._data["author"])

    @property
    def committer(self) -> CommitAuthor:
        """Git committer information."""
        return CommitAuthor(self._data["committer"])

    @property
    def distinct(self) -> bool:
        """Whether this commit is distinct from any that have been pushed before."""
        return self._data["distinct"]

    @property
    def id(self) -> str:
        return self._data["id"]

    @property
    def message(self) -> str:
        return self._data["message"]

    @property
    def modified(self) -> list[str]:
        """Paths of modified files."""
        return self._data.get("modified", [])

    @property
    def removed(self) -> list[str]:
        """Paths of removed files."""
        return self._data.get("removed", [])

    @property
    def timestamp(self) -> str:
        """ISO 8601 (YYYY-MM-DDTHH:MM:SSZ) timestamp of the commit."""
        return self._data["timestamp"]

    @property
    def tree_id(self) -> str:
        return self._data["tree_id"]

    @property
    def url(self) -> str:
        """URL that points to the commit API resource."""
        return self._data["url"]
