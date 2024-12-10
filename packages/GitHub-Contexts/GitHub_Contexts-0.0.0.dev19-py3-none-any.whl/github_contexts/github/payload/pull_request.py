
from github_contexts.github.payload.base import Payload
from github_contexts.github.enum import ActionType
from github_contexts.github.payload.object.pull_request import PullRequest
from github_contexts.github.payload.object.user import User
from github_contexts.github.payload.object.team import Team
from github_contexts.github.payload.object.milestone import Milestone
from github_contexts.github.payload.object.label import Label
from github_contexts.github.payload.object.changes import (
    PullRequestEditedChanges
)


class PullRequestPayload(Payload):

    def __init__(self, payload: dict):
        super().__init__(payload=payload)
        self._pull_request = payload["pull_request"]
        return

    @property
    def action(self) -> ActionType:
        return ActionType(self._data["action"])

    @property
    def number(self) -> int:
        """Pull request number"""
        return self._data["number"]

    @property
    def pull_request(self) -> PullRequest:
        return PullRequest(self._pull_request)

    @property
    def internal(self) -> bool:
        """Whether the pull request is internal, i.e., within the same repository."""
        return self.pull_request.head.repo.full_name == self.repository.full_name

    @property
    def after(self) -> str | None:
        """
        The SHA hash of the most recent commit on the head branch after the synchronization event.

        This is only available for the 'synchronize' action.
        """
        return self._data.get("after")

    @property
    def assignee(self) -> User | None:
        """The user that was assigned or unassigned from the pull request.

        This is only available for the 'assigned' and 'unassigned' events.
        """
        return User(self._data.get("assignee"))

    @property
    def before(self) -> str | None:
        """
        The SHA hash of the most recent commit on the head branch before the synchronization event.

        This is only available for the 'synchronize' action.
        """
        return self._data.get("before")

    @property
    def changes(self) -> PullRequestEditedChanges | None:
        """The changes to the pull request if the action was 'edited'."""
        if self.action == ActionType.EDITED:
            return PullRequestEditedChanges(self._data["changes"])
        return

    @property
    def label(self) -> Label | None:
        """The label that was added or removed from the pull request.

        This is only available for the 'labeled' and 'unlabeled' events.
        """
        return Label(self._data["label"]) if self._data.get("label") else None

    @property
    def milestone(self) -> Milestone | None:
        """The milestone that was added to or removed from the pull request.

        This is only available for the 'milestoned' and 'demilestoned' events.
        """
        return Milestone(self._data.get("milestone"))

    @property
    def reason(self) -> str | None:
        """This is only available for the
        'auto_merge_disabled', 'auto_merge_disabled', 'dequeued' events.
        """
        return self._data.get("reason")

    @property
    def requested_reviewer(self) -> User | None:
        """The user that was requested for review.

        This is only available for the 'review_request_removed', 'review_requested' events.
        """
        return User(self._data["requested_reviewer"]) if self._data.get("requested_reviewer") else None

    @property
    def requested_team(self) -> Team | None:
        """The team that was requested for review.

        This is only available for the 'review_request_removed', 'review_requested' events.
        """
        return Team(self._data["requested_team"]) if self._data.get("requested_team") else None
