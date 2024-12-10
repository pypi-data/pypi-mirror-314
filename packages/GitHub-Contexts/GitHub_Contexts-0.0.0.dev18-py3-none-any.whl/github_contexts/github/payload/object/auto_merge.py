from github_contexts.property_dict import PropertyDict as _PropertyDict
from github_contexts.github.payload.object.user import User
from github_contexts.github.enum import MergeMethod


class AutoMerge(_PropertyDict):
    """The status of auto merging a pull request."""

    def __init__(self, auto_merge: dict):
        """
        Parameters
        ----------
        auto_merge : dict
            The `auto_merge` dictionary contained in the `pull_request` object of the payload.
        """
        super().__init__(auto_merge)
        return

    @property
    def commit_message(self) -> str | None:
        """The commit message that will be used for the merge commit."""
        return self._data.get("commit_message")

    @property
    def commit_title(self) -> str | None:
        """The commit title that will be used for the merge commit."""
        return self._data.get("commit_title")

    @property
    def enabled_by(self) -> User | None:
        """The user who enabled auto merging."""
        return User(self._data["enabled_by"]) if self._data.get("enabled_by") else None

    @property
    def merge_method(self) -> MergeMethod:
        """The merge method that will be used to merge the pull request."""
        return MergeMethod(self._data["merge_method"])
