from github_contexts.github.payload.base import Payload
from github_contexts.github.enum import ActionType
from github_contexts.github.payload.object.comment import Comment
from github_contexts.github.payload.object.issue import Issue
from github_contexts.github.payload.object.changes import IssueCommentEditedChanges


class IssueCommentPayload(Payload):
    def __init__(self, payload: dict):
        super().__init__(payload=payload)
        return

    @property
    def action(self) -> ActionType:
        """Action that triggered the event;
        either 'created', 'edited', or 'deleted'.
        """
        return ActionType(self._data["action"])

    @property
    def comment(self) -> Comment:
        """Comment data."""
        return Comment(self._data["comment"])

    @property
    def issue(self) -> Issue:
        """Issue data."""
        return Issue(self._data["issue"])

    @property
    def is_on_pull(self) -> bool:
        """Whether the comment is on a pull request (True) or an issue (False)."""
        return bool(self.issue.pull_request)

    @property
    def changes(self) -> IssueCommentEditedChanges | None:
        """The changes to the comment if the action was 'edited'."""
        if self.action == ActionType.EDITED:
            return IssueCommentEditedChanges(self._data["changes"])
        return
