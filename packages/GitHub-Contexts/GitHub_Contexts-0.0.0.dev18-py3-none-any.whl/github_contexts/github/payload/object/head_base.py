from github_contexts.property_dict import PropertyDict as _PropertyDict
from github_contexts.github.payload.object.repository import Repository
from github_contexts.github.payload.object.user import User


class HeadBase(_PropertyDict):
    """Head or base branch info for a pull request."""

    def __init__(self, head_or_base: dict):
        """
        Parameters
        ----------
        head_or_base : dict
            The `head` or `base` object contained in the `pull_request` object of the payload.
        """
        super().__init__(head_or_base)
        return

    @property
    def label(self) -> str:
        """The label of the branch."""
        return self._data["label"]

    @property
    def ref(self) -> str:
        """The reference name of the branch."""
        return self._data["ref"]

    @property
    def name(self) -> str:
        """Alias for 'ref'."""
        return self.ref

    @property
    def repo(self) -> Repository:
        """The repository that contains the branch."""
        return Repository(self._data["repo"])

    @property
    def sha(self) -> str:
        """The SHA hash of the branch."""
        return self._data["sha"]

    @property
    def user(self) -> User | None:
        return User(self._data["user"]) if self._data.get("user") else None

    @property
    def url(self) -> str:
        return f"{self.repo.html_url.removesuffix("/")}/tree/{self.ref}"