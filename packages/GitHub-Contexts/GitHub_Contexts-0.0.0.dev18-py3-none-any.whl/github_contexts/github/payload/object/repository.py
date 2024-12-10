from github_contexts.property_dict import PropertyDict as _PropertyDict
from github_contexts.github.payload.object.license import License
from github_contexts.github.payload.object.user import User
from github_contexts.github.payload.object.permissions import Permissions
from github_contexts.github.enum import (
    RepositoryVisibility,
    MergeCommitTitle,
    MergeCommitMessage,
    SquashMergeCommitMessage,
    SquashMergeCommitTitle
)


class Repository(_PropertyDict):

    def __init__(self, repository: dict):
        super().__init__(repository)
        return

    @property
    def allow_auto_merge(self) -> bool | None:
        return self._data.get("allow_auto_merge")

    @property
    def allow_forking(self) -> bool | None:
        return self._data.get("allow_forking")

    @property
    def allow_merge_commit(self) -> bool | None:
        return self._data.get("allow_merge_commit")

    @property
    def allow_rebase_merge(self) -> bool | None:
        return self._data.get("allow_rebase_merge")

    @property
    def allow_squash_merge(self) -> bool | None:
        return self._data.get("allow_squash_merge")

    @property
    def allow_update_branch(self) -> bool | None:
        return self._data.get("allow_update_branch")

    @property
    def archive_url(self) -> str:
        return self._data["archive_url"]

    @property
    def archived(self) -> bool:
        return self._data["archived"]

    @property
    def assignees_url(self) -> str:
        return self._data["assignees_url"]

    @property
    def blobs_url(self) -> str:
        return self._data["blobs_url"]

    @property
    def branches_url(self) -> str:
        return self._data["branches_url"]

    @property
    def clone_url(self) -> str:
        return self._data["clone_url"]

    @property
    def collaborators_url(self) -> str:
        return self._data["collaborators_url"]

    @property
    def comments_url(self) -> str:
        return self._data["comments_url"]

    @property
    def commits_url(self) -> str:
        return self._data["commits_url"]

    @property
    def compare_url(self) -> str:
        return self._data["compare_url"]

    @property
    def contents_url(self) -> str:
        return self._data["contents_url"]

    @property
    def contributors_url(self) -> str:
        return self._data["contributors_url"]

    @property
    def created_at(self) -> str:
        return self._data["created_at"]

    @property
    def custom_properties(self) -> dict | None:
        return self._data.get("custom_properties")

    @property
    def default_branch(self) -> str:
        return self._data["default_branch"]

    @property
    def delete_branch_on_merge(self) -> bool | None:
        return self._data.get("delete_branch_on_merge")

    @property
    def deployments_url(self) -> str:
        return self._data["deployments_url"]

    @property
    def description(self) -> str | None:
        return self._data["description"]

    @property
    def disabled(self) -> bool | None:
        return self._data.get("disabled")

    @property
    def downloads_url(self) -> str:
        return self._data["downloads_url"]

    @property
    def events_url(self) -> str:
        return self._data["events_url"]

    @property
    def fork(self) -> bool:
        return self._data["fork"]

    @property
    def forks(self) -> int:
        return self._data["forks"]

    @property
    def forks_count(self) -> int:
        return self._data["forks_count"]

    @property
    def forks_url(self) -> str:
        return self._data["forks_url"]

    @property
    def full_name(self) -> str:
        return self._data["full_name"]

    @property
    def git_commits_url(self) -> str:
        return self._data["git_commits_url"]

    @property
    def git_refs_url(self) -> str:
        return self._data["git_refs_url"]

    @property
    def git_tags_url(self) -> str:
        return self._data["git_tags_url"]

    @property
    def git_url(self) -> str:
        return self._data["git_url"]

    @property
    def has_discussions(self) -> bool | None:
        return self._data.get("has_discussions")

    @property
    def has_downloads(self) -> bool:
        return self._data["has_downloads"]

    @property
    def has_issues(self) -> bool:
        return self._data["has_issues"]

    @property
    def has_pages(self) -> bool:
        return self._data["has_pages"]

    @property
    def has_projects(self) -> bool:
        return self._data["has_projects"]

    @property
    def has_wiki(self) -> bool:
        return self._data["has_wiki"]

    @property
    def homepage(self) -> str | None:
        return self._data["homepage"]

    @property
    def hooks_url(self) -> str:
        return self._data["hooks_url"]

    @property
    def html_url(self) -> str:
        return self._data["html_url"]

    @property
    def id(self) -> int:
        "Unique identifier of the repository."
        return self._data["id"]

    @property
    def is_template(self) -> bool | None:
        return self._data.get("is_template")

    @property
    def issue_comment_url(self) -> str:
        return self._data["issue_comment_url"]

    @property
    def issue_events_url(self) -> str:
        return self._data["issue_events_url"]

    @property
    def issues_url(self) -> str:
        return self._data["issues_url"]

    @property
    def keys_url(self) -> str:
        return self._data["keys_url"]

    @property
    def labels_url(self) -> str:
        return self._data["labels_url"]

    @property
    def language(self) -> str | None:
        return self._data["language"]

    @property
    def languages_url(self) -> str:
        return self._data["languages_url"]

    @property
    def license(self) -> License | None:
        return License(self._data["license"]) if self._data.get("license") else None

    @property
    def master_branch(self) -> str | None:
        return self._data.get("master_branch") or self.default_branch

    @property
    def merge_commit_message(self) -> MergeCommitMessage | None:
        return MergeCommitMessage(self._data["merge_commit_message"]) if self._data.get("merge_commit_message") else None

    @property
    def merge_commit_title(self) -> MergeCommitTitle | None:
        return MergeCommitTitle(self._data["merge_commit_title"]) if self._data.get("merge_commit_title") else None

    @property
    def merges_url(self) -> str:
        return self._data["merges_url"]

    @property
    def milestones_url(self) -> str:
        return self._data["milestones_url"]

    @property
    def mirror_url(self) -> str | None:
        return self._data.get("mirror_url")

    @property
    def name(self) -> str:
        return self._data["name"]

    @property
    def node_id(self) -> str:
        return self._data["node_id"]

    @property
    def notifications_url(self) -> str:
        return self._data["notifications_url"]

    @property
    def open_issues(self) -> int:
        return self._data["open_issues"]

    @property
    def open_issues_count(self) -> int:
        return self._data["open_issues_count"]

    @property
    def organization(self) -> str | None:
        return self._data.get("organization")

    @property
    def owner(self) -> User | None:
        return User(self._data["owner"]) if self._data.get("owner") else None

    @property
    def permissions(self) -> Permissions | None:
        return Permissions(self._data["permissions"]) if self._data.get("permissions") else None

    @property
    def private(self) -> bool:
        """Whether the repository is private (True) or public (False)."""
        return self._data["private"]

    @property
    def public(self) -> bool:
        """Whether the repository is public (True) or private (False)."""
        return self._data.get("public", not self.private)

    @property
    def pulls_url(self) -> str:
        return self._data["pulls_url"]

    @property
    def pushed_at(self) -> str | int | None:
        return self._data["pushed_at"]

    @property
    def releases_url(self) -> str:
        return self._data["releases_url"]

    @property
    def role_name(self) -> str | None:
        return self._data.get("role_name")

    @property
    def size(self) -> int:
        return self._data["size"]

    @property
    def squash_merge_commit_message(self) -> SquashMergeCommitMessage | None:
        return (
            SquashMergeCommitMessage(self._data["squash_merge_commit_message"])
            if self._data.get("squash_merge_commit_message") else None
        )

    @property
    def squash_merge_commit_title(self) -> SquashMergeCommitTitle | None:
        return (
            SquashMergeCommitTitle(self._data["squash_merge_commit_title"])
            if self._data.get("squash_merge_commit_title") else None
        )

    @property
    def ssh_url(self) -> str:
        return self._data["ssh_url"]

    @property
    def stargazers(self) -> int | None:
        return self._data.get("stargazers")

    @property
    def stargazers_count(self) -> int:
        return self._data["stargazers_count"]

    @property
    def stargazers_url(self) -> str:
        return self._data["stargazers_url"]

    @property
    def statuses_url(self) -> str:
        return self._data["statuses_url"]

    @property
    def subscribers_url(self) -> str:
        return self._data["subscribers_url"]

    @property
    def subscription_url(self) -> str:
        return self._data["subscription_url"]

    @property
    def svn_url(self) -> str:
        return self._data["svn_url"]

    @property
    def tags_url(self) -> str:
        return self._data["tags_url"]

    @property
    def teams_url(self) -> str:
        return self._data["teams_url"]

    @property
    def topics(self) -> list[str]:
        return self._data.get("topics", [])

    @property
    def trees_url(self) -> str:
        return self._data["trees_url"]

    @property
    def updated_at(self) -> str:
        return self._data["updated_at"]

    @property
    def url(self) -> str:
        return self._data["url"]

    @property
    def visibility(self) -> RepositoryVisibility:
        return RepositoryVisibility(self._data["visibility"])

    @property
    def watchers(self) -> int:
        return self._data["watchers"]

    @property
    def watchers_count(self) -> int:
        return self._data["watchers_count"]

    @property
    def web_commit_signoff_required(self) -> bool | None:
        return self._data.get("web_commit_signoff_required")
