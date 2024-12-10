from github_contexts.property_dict import PropertyDict as _PropertyDict
from github_contexts.github.enum import ActiveLockReason, AuthorAssociation, State
from github_contexts.github.payload.object.label import Label
from github_contexts.github.payload.object.user import User
from github_contexts.github.payload.object.milestone import Milestone
from github_contexts.github.payload.object.performed_via_github_app import PerformedViaGitHubApp
from github_contexts.github.payload.object.pull_request import PullRequest
from github_contexts.github.payload.object.reactions import Reactions


class Issue(_PropertyDict):
    """
    The `issue` object contained in the payload of the `issues` and `issue_comment` events.
    """

    def __init__(self, issue: dict):
        """
        Parameters
        ----------
        issue : dict
            The `issue` dictionary contained in the payload.
        """
        super().__init__(issue)
        return

    @property
    def active_lock_reason(self) -> ActiveLockReason:
        return ActiveLockReason(self._data["active_lock_reason"])

    @property
    def assignee(self) -> User | None:
        return User(self._data["assignee"]) if "assignee" in self._data else None

    @property
    def assignees(self) -> list[User]:
        assignees_list = self._data.get("assignees", [])
        return [User(assignee) for assignee in assignees_list if assignee]

    @property
    def author_association(self) -> AuthorAssociation:
        return AuthorAssociation(self._data["author_association"])

    @property
    def body(self) -> str | None:
        """Contents of the issue."""
        return self._data["body"]

    @property
    def closed_at(self) -> str | None:
        return self._data["closed_at"]

    @property
    def comments(self) -> int:
        return self._data["comments"]

    @property
    def comments_url(self) -> str:
        return self._data["comments_url"]

    @property
    def created_at(self) -> str:
        return self._data["created_at"]

    @property
    def draft(self) -> bool | None:
        return self._data.get("draft")

    @property
    def events_url(self) -> str:
        return self._data["events_url"]

    @property
    def html_url(self) -> str:
        return self._data["html_url"]

    @property
    def id(self) -> int:
        return self._data["id"]

    @property
    def labels(self) -> list[Label]:
        return [Label(label) for label in self._data.get("labels", [])]

    @property
    def labels_url(self) -> str:
        return self._data["labels_url"]

    @property
    def locked(self) -> bool | None:
        return self._data.get("locked")

    @property
    def milestone(self) -> Milestone | None:
        return Milestone(self._data["milestone"]) if self._data.get("milestone") else None

    @property
    def node_id(self) -> str:
        return self._data["node_id"]

    @property
    def number(self) -> int:
        return self._data["number"]

    @property
    def performed_via_github_app(self) -> PerformedViaGitHubApp | None:
        return PerformedViaGitHubApp(self._data["performed_via_github_app"]) if self._data.get("performed_via_github_app") else None

    @property
    def pull_request(self) -> PullRequest | None:
        return PullRequest(self._data["pull_request"]) if self._data.get("pull_request") else None

    @property
    def reactions(self) -> Reactions:
        return Reactions(self._data["reactions"])

    @property
    def repository_url(self) -> str:
        return self._data["repository_url"]

    @property
    def state(self) -> State | None:
        return State(self._data["state"]) if self._data.get("state") else None

    @property
    def state_reason(self) -> str | None:
        return self._data.get("state_reason")

    @property
    def timeline_url(self) -> str | None:
        return self._data.get("timeline_url")

    @property
    def title(self) -> str:
        """Title of the issue."""
        return self._data["title"]

    @property
    def updated_at(self) -> str:
        return self._data["updated_at"]

    @property
    def url(self) -> str:
        return self._data["url"]

    @property
    def user(self) -> User | None:
        return User(self._data["user"]) if self._data.get("user") else None

    @property
    def label_names(self) -> list[str]:
        return [label.name for label in self.labels]
