from github_contexts.property_dict import PropertyDict as _PropertyDict
from github_contexts.github.enum import AuthorAssociation
from github_contexts.github.payload.object.user import User
from github_contexts.github.payload.object.performed_via_github_app import PerformedViaGitHubApp
from github_contexts.github.payload.object.reactions import Reactions


class Comment(_PropertyDict):

    def __init__(self, comment: dict):
        super().__init__(comment)
        return

    @property
    def author_association(self) -> AuthorAssociation:
        return AuthorAssociation(self._data["author_association"])

    @property
    def body(self) -> str:
        """Contents of the issue comment."""
        return self._data["body"]

    @property
    def created_at(self) -> str:
        """Timestamp of when the comment was created."""
        return self._data["created_at"]

    @property
    def html_url(self) -> str:
        """URL of the comment on GitHub."""
        return self._data["html_url"]

    @property
    def id(self) -> int:
        """Unique identifier of the comment."""
        return self._data["id"]

    @property
    def issue_url(self) -> str:
        """URL of the issue on GitHub."""
        return self._data["issue_url"]

    @property
    def node_id(self) -> str:
        """Node ID of the comment."""
        return self._data["node_id"]

    @property
    def performed_via_github_app(self) -> PerformedViaGitHubApp | None:
        """GitHub App that performed the comment."""
        return PerformedViaGitHubApp(self._data["performed_via_github_app"]) if self._data.get("performed_via_github_app") else None

    @property
    def reactions(self) -> Reactions:
        """Reactions to the comment."""
        return Reactions(self._data["reactions"])

    @property
    def updated_at(self) -> str:
        """Timestamp of when the comment was last updated."""
        return self._data["updated_at"]

    @property
    def url(self) -> str:
        """URL of the comment API resource."""
        return self._data["url"]

    @property
    def user(self) -> User | None:
        """User who created the comment."""
        return User(self._data["user"]) if self._data.get("user") else None
