from github_contexts.property_dict import PropertyDict as _PropertyDict
from github_contexts.github.enum import ActiveLockReason, AuthorAssociation, State
from github_contexts.github.payload.object.label import Label
from github_contexts.github.payload.object.user import User
from github_contexts.github.payload.object.milestone import Milestone
from github_contexts.github.payload.object.auto_merge import AutoMerge
from github_contexts.github.payload.object.head_base import HeadBase
from github_contexts.github.payload.object.team import Team


class PullRequest(_PropertyDict):

    def __init__(self, pull_request: dict):
        super().__init__(pull_request)
        return

    @property
    def active_lock_reason(self) -> ActiveLockReason:
        return ActiveLockReason(self._data["active_lock_reason"])

    @property
    def additions(self) -> int | None:
        return self._data.get("additions")

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
    def auto_merge(self) -> AutoMerge | None:
        return AutoMerge(self._data["auto_merge"]) if self._data.get("auto_merge") else None

    @property
    def base(self) -> HeadBase:
        """Pull request's base branch info."""
        return HeadBase(self._data["base"])

    @property
    def body(self) -> str | None:
        """Pull request body."""
        return self._data.get("body")

    @property
    def changed_files(self) -> int | None:
        return self._data.get("changed_files")

    @property
    def closed_at(self) -> str | None:
        return self._data.get("closed_at")

    @property
    def comments(self) -> int | None:
        return self._data.get("comments")

    @property
    def comments_url(self) -> str:
        return self._data["comments_url"]

    @property
    def commits(self) -> int | None:
        return self._data.get("commits")

    @property
    def commits_url(self) -> str:
        return self._data["commits_url"]

    @property
    def created_at(self) -> str:
        return self._data["created_at"]

    @property
    def deletions(self) -> int | None:
        return self._data.get("deletions")

    @property
    def diff_url(self) -> str | None:
        return self._data.get("diff_url")

    @property
    def draft(self) -> bool:
        return self._data["draft"]

    @property
    def head(self) -> HeadBase:
        """Pull request's head branch info."""
        return HeadBase(self._data["head"])

    @property
    def html_url(self) -> str | None:
        return self._data.get("html_url")

    @property
    def id(self) -> int:
        return self._data["id"]

    @property
    def issue_url(self) -> str:
        return self._data["issue_url"]

    @property
    def labels(self) -> list[Label]:
        return [Label(label) for label in self._data.get("labels", [])]

    @property
    def locked(self) -> bool:
        return self._data["locked"]

    @property
    def maintainer_can_modify(self) -> bool | None:
        return self._data.get("maintainer_can_modify")

    @property
    def merge_commit_sha(self) -> str | None:
        return self._data.get("merge_commit_sha")

    @property
    def mergeable(self) -> bool | None:
        return self._data.get("mergeable")

    @property
    def mergeable_state(self) -> str | None:
        return self._data.get("mergeable_state")

    @property
    def merged(self) -> bool | None:
        """Whether the pull request has been merged."""
        return self._data.get("merged")

    @property
    def merged_at(self) -> str | None:
        return self._data.get("merged_at")

    @property
    def merged_by(self) -> User | None:
        return User(self._data["merged_by"]) if self._data.get("merged_by") else None

    @property
    def milestone(self) -> Milestone | None:
        return Milestone(self._data["milestone"]) if self._data.get("milestone") else None

    @property
    def node_id(self) -> str:
        return self._data["node_id"]

    @property
    def number(self) -> int:
        """Number uniquely identifying the pull request within its repository."""
        return self._data["number"]

    @property
    def patch_url(self) -> str | None:
        return self._data.get("patch_url")

    @property
    def rebaseable(self) -> bool | None:
        return self._data.get("rebaseable")

    @property
    def requested_reviewers(self) -> list[User]:
        return [User(user) for user in self._data.get("requested_reviewers", [])]

    @property
    def requested_teams(self) -> list[Team]:
        return [Team(team) for team in self._data.get("requested_teams", [])]

    @property
    def review_comment_url(self) -> str:
        return self._data["review_comment_url"]

    @property
    def review_comments(self) -> int | None:
        return self._data.get("review_comments")

    @property
    def review_comments_url(self) -> str:
        return self._data["review_comments_url"]

    @property
    def state(self) -> State:
        return State(self._data["state"])

    @property
    def statuses_url(self) -> str:
        return self._data["statuses_url"]

    @property
    def title(self) -> str:
        """Pull request title."""
        return self._data["title"]

    @property
    def updated_at(self) -> str:
        return self._data["updated_at"]

    @property
    def url(self) -> str | None:
        return self._data.get("url")

    @property
    def user(self) -> User | None:
        return User(self._data["user"]) if self._data.get("user") else None

    @property
    def label_names(self) -> list[str]:
        return [label.name for label in self.labels]
