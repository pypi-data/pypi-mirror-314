from github_contexts.property_dict import PropertyDict as _PropertyDict
from github_contexts.github.payload.object.issue import Issue
from github_contexts.github.payload.object.repository import Repository


class IssueOpenedChanges(_PropertyDict):

    def __init__(self, changes: dict):
        super().__init__(changes)
        return

    @property
    def old_issue(self) -> Issue | None:
        return Issue(self._data["old_issue"]) if self._data.get("old_issue") else None

    @property
    def old_repository(self) -> Repository:
        return Repository(self._data["old_repository"])


class IssueTransferredChanges(_PropertyDict):

    def __init__(self, changes: dict):
        super().__init__(changes)
        return

    @property
    def new_issue(self) -> Issue:
        return Issue(self._data["new_issue"])

    @property
    def new_repository(self) -> Repository:
        return Repository(self._data["new_repository"])


class IssueEditedChanges(_PropertyDict):

    def __init__(self, changes: dict):
        super().__init__(changes)
        return

    @property
    def body(self) -> dict | None:
        return self._data.get("body")

    @property
    def title(self) -> dict | None:
        return self._data.get("title")


class PullRequestEditedChanges(_PropertyDict):

    def __init__(self, changes: dict):
        super().__init__(changes)
        return

    @property
    def base_ref(self) -> str | None:
        return self._data.get("base", {}).get("ref", {}).get("from")

    @property
    def base_sha(self) -> str | None:
        return self._data.get("base", {}).get("sha", {}).get("from")

    @property
    def body(self) -> str | None:
        """"The previous version of the body."""
        return self._data.get("body", {}).get("from")

    @property
    def title(self) -> dict | None:
        """The previous version of the title."""
        return self._data.get("title", {}).get("from")


class IssueCommentEditedChanges(_PropertyDict):

    def __init__(self, changes: dict):
        super().__init__(changes)
        return

    @property
    def body(self) -> str | None:
        """The previous version of the body."""
        return self._data.get("body", {}).get("from")
