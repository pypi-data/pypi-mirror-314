"""GitHub Webhook Issues Payload."""


from github_contexts.github.payload.base import Payload
from github_contexts.github.enum import ActionType
from github_contexts.github.payload.object.issue import Issue
from github_contexts.github.payload.object.user import User
from github_contexts.github.payload.object.milestone import Milestone
from github_contexts.github.payload.object.label import Label
from github_contexts.github.payload.object.changes import (
    IssueOpenedChanges, IssueEditedChanges, IssueTransferredChanges
)


class IssuesPayload(Payload):

    def __init__(self, payload: dict):
        super().__init__(payload=payload)
        return

    @property
    def action(self) -> ActionType:
        return ActionType(self._data["action"])

    @property
    def issue(self) -> Issue:
        """The issue data.

        References
        ----------
        - [GitHub API Docs](https://docs.github.com/en/rest/issues/issues?apiVersion=2022-11-28#get-an-issue)
        """
        return Issue(self._data["issue"])

    @property
    def assignee(self) -> User | None:
        """The user that was assigned or unassigned from the issue.

        This is only available for the 'assigned' and 'unassigned' events.
        """
        return User(self._data.get("assignee"))

    @property
    def changes(self) -> IssueOpenedChanges | IssueEditedChanges | IssueTransferredChanges | None:
        """The changes to the issue if the action was 'edited'."""
        if self.action == ActionType.EDITED:
            return IssueEditedChanges(self._data["changes"])
        if self.action == ActionType.OPENED:
            return IssueOpenedChanges(self._data["changes"])
        if self.action == ActionType.TRANSFERRED:
            return IssueTransferredChanges(self._data["changes"])
        return

    @property
    def label(self) -> Label | None:
        """The label that was added or removed from the issue.

        This is only available for the 'labeled' and 'unlabeled' events.
        """
        return Label(self._data["label"]) if self._data.get("label") else None

    @property
    def milestone(self) -> Milestone | None:
        """The milestone that was added to or removed from the issue.

        This is only available for the 'milestoned' and 'demilestoned' events.
        """
        return Milestone(self._data.get("milestone"))
