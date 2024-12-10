"""Base class for all GitHub webhook payloads."""

from github_contexts.property_dict import PropertyDict as _PropertyDict
from github_contexts.github.payload.object.user import User
from github_contexts.github.payload.object.repository import Repository


class Payload(_PropertyDict):
    """
    The full webhook payload of the triggering event.

    References
    ----------
    - [GitHub Docs](https://docs.github.com/en/webhooks/webhook-events-and-payloads)
    """

    def __init__(self, payload: dict):
        super().__init__(payload)
        return

    @property
    def enterprise(self) -> dict | None:
        """An enterprise on GitHub.

        This is only available when the webhook is configured on an enterprise account
        or an organization that's part of an enterprise account.
        """
        return self._data.get("enterprise")

    @property
    def installation(self) -> dict | None:
        """The GitHub App installation.

        This is only available when the event is configured for and sent to a GitHub App.
        """
        return self._data.get("installation")

    @property
    def organization(self) -> dict | None:
        """An organization on GitHub.

        This is only available when the event occurs from activity in a repository owned by an organization,
        or when the webhook is configured for an organization.
        """
        return self._data.get("organization")

    @property
    def repository(self) -> Repository | None:
        """The repository on GitHub where the event occurred.

        This is only available when the event occurs from activity in the repository.
        """
        return Repository(self._data["repository"]) if "repository" in self._data else None

    @property
    def sender(self) -> User:
        """The GitHub user that triggered the event."""
        return User(self._data["sender"])
