from enum import Enum as _Enum


class ActiveLockReason(_Enum):
    RESOLVED = "resolved"
    OFF_TOPIC = "off-topic"
    TOO_HEATED = "too heated"
    SPAM = "spam"
    OTHER = None

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return self is other

    def __hash__(self):
        return hash((self.__class__, self.value))


class AuthorAssociation(_Enum):
    OWNER = "OWNER"
    MEMBER = "MEMBER"
    CONTRIBUTOR = "CONTRIBUTOR"
    COLLABORATOR = "COLLABORATOR"
    FIRST_TIME_CONTRIBUTOR = "FIRST_TIME_CONTRIBUTOR"
    FIRST_TIMER = "FIRST_TIMER"
    MANNEQUIN = "MANNEQUIN"
    NONE = "NONE"

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return self is other

    def __hash__(self):
        return hash((self.__class__, self.value))


class State(_Enum):
    OPEN = "open"
    CLOSED = "closed"

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return self is other

    def __hash__(self):
        return hash((self.__class__, self.value))


class RefType(_Enum):
    BRANCH = "branch"
    TAG = "tag"

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return self is other

    def __hash__(self):
        return hash((self.__class__, self.value))


class UserType(_Enum):
    USER = "User"
    ORGANIZATION = "Organization"
    BOT = "Bot"

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return self is other

    def __hash__(self):
        return hash((self.__class__, self.value))


class EventType(_Enum):
    BRANCH_PROTECTION_CONFIGURATION = "branch_protection_configuration"
    BRANCH_PROTECTION_RULE = "branch_protection_rule"
    CHECK_RUN = "check_run"
    CHECK_SUITE = "check_suite"
    CODE_SCANNING_ALERT = "code_scanning_alert"
    COMMIT_COMMENT = "commit_comment"
    CREATE = "create"
    CONTENT_REFERENCE = "content_reference"
    CUSTOM_PROPERTY = "custom_property"
    CUSTOM_PROPERTY_VALUES = "custom_property_values"
    DELETE = "delete"
    DEPENDABOT_ALERT = "dependabot_alert"
    DEPLOY_KEY = "deploy_key"
    DEPLOYMENT = "deployment"
    DEPLOYMENT_PROTECTION_RULE = "deployment_protection_rule"
    DEPLOYMENT_REVIEW = "deployment_review"
    DEPLOYMENT_STATUS = "deployment_status"
    DISCUSSION = "discussion"
    DISCUSSION_COMMENT = "discussion_comment"
    FORK = "fork"
    GITHUB_APP_AUTHORIZATION = "github_app_authorization"
    GOLLUM = "gollum"
    INSTALLATION = "installation"
    INSTALLATION_REPOSITORIES = "installation_repositories"
    INSTALLATION_TARGET = "installation_target"
    ISSUE_COMMENT = "issue_comment"
    ISSUES = "issues"
    LABEL = "label"
    MARKETPLACE_PURCHASE = "marketplace_purchase"
    MEMBER = "member"
    MEMBERSHIP = "membership"
    MERGE_GROUP = "merge_group"
    META = "meta"
    MILESTONE = "milestone"
    ORG_BLOCK = "org_block"
    ORGANIZATION = "organization"
    PACKAGE = "package"
    PAGE_BUILD = "page_build"
    PERSONAL_ACCESS_TOKEN_REQUEST = "personal_access_token_request"
    PING = "ping"
    PROJECT_CARD = "project_card"
    PROJECT = "project"
    PROJECT_COLUMN = "project_column"
    PROJECTS_V2 = "projects_v2"
    PROJECTS_V2_ITEM = "projects_v2_item"
    PUBLIC = "public"
    PULL_REQUEST = "pull_request"
    PULL_REQUEST_REVIEW_COMMENT = "pull_request_review_comment"
    PULL_REQUEST_REVIEW = "pull_request_review"
    PULL_REQUEST_REVIEW_THREAD = "pull_request_review_thread"
    PULL_REQUEST_TARGET = "pull_request_target"
    PUSH = "push"
    REGISTRY_PACKAGE = "registry_package"
    RELEASE = "release"
    REMINDER = "reminder"
    REPOSITORY_ADVISORY = "repository_advisory"
    REPOSITORY = "repository"
    REPOSITORY_DISPATCH = "repository_dispatch"
    REPOSITORY_IMPORT = "repository_import"
    REPOSITORY_RULESET = "repository_ruleset"
    REPOSITORY_VULNERABILITY_ALERT = "repository_vulnerability_alert"
    SCHEDULE = "schedule"
    SECRET_SCANNING_ALERT = "secret_scanning_alert"
    SECRET_SCANNING_ALERT_LOCATION = "secret_scanning_alert_location"
    SECURITY_ADVISORY = "security_advisory"
    SECURITY_AND_ANALYSIS = "security_and_analysis"
    SPONSORSHIP = "sponsorship"
    STAR = "star"
    STATUS = "status"
    TEAM_ADD = "team_add"
    TEAM = "team"
    WATCH = "watch"
    WORKFLOW_DISPATCH = "workflow_dispatch"
    WORKFLOW_JOB = "workflow_job"
    WORKFLOW_RUN = "workflow_run"

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return self is other

    def __hash__(self):
        return hash((self.__class__, self.value))


class ActionType(_Enum):
    """
    Triggering actions of events that can trigger a workflow.
    Each action is only available for certain events.

    Attributes
    ----------
    ASSIGNED : str
        An issue or pull request was assigned to a user.
        Available for `issues`, `pull_request`.
    AUTO_MERGE_DISABLED : str
        Auto merge was disabled for a pull request.
        Available for `pull_request`.
    AUTO_MERGE_ENABLED : str
        Auto merge was enabled for a pull request.
        Available for `pull_request`.
    CLOSED : str
        An issue or pull request was closed.
        Available for `issues`, `pull_request`.
    CONVERTED_TO_DRAFT : str
        A pull request was converted to a draft.
        Available for `pull_request`.
    CREATED : str
        A comment on an issue or pull request was created.
        Available for `issue_comment`.
    DELETED : str
        An issue, pull request, or a comment on an issue or pull request was deleted.
        Available for `issue_comment`, `issues`, `pull_request`.
    DEMILESTONED : str
        An issue or pull request was removed from a milestone.
        Available for `issues`, `pull_request`.
    DEQUEUED : str
        A pull request was removed from the merge queue.
        Available for `pull_request`.
    EDITED : str
        The title or body on an issue or pull request,
        or a comment on an issue or pull request was edited,
        or the base branch of a pull request was changed.
        Available for `issue_comment`, `issues`, `pull_request`.
    ENQUEUED : str
        A pull request was added to the merge queue.
        Available for `pull_request`.
    LABELED : str
        A label was added to an issue or pull request.
        Available for `issues`, `pull_request`.
    LOCKED : str
        Conversation on an issue or pull request was locked.
        Available for `issues`, `pull_request`.
    MILESTONED : str
        An issue or pull reqeust was added to a milestone.
        Available for `issues`, `pull_request`.
    OPENED : str
        An issue or pull request was created.
        Available for `issues`, `pull_request`.
    PINNED : str
        An issue was pinned to a repository.
        Available for `issues`.
    READY_FOR_REVIEW : str
        A draft pull request was marked as ready for review.
        Available for `pull_request`.
    REOPENED : str
        A closed issue or pull request was reopened.
        Available for `issues`, `pull_request`.
    REVIEW_REQUEST_REMOVED : str
        A request for review by a person or team was removed from a pull request.
        Available for `pull_request`.
    REVIE_REQUESTED : str
        Review by a person or team was requested for a pull request.
        Available for `pull_request`.
    SYNCHRONIZE : str
        A pull request's head branch was updated.
        For example, the head branch was updated from the base branch
        or new commits were pushed to the head branch.
        Available for `pull_request`.
    TRANSFERRED : str
        An issue was transferred to another repository.
        Available for `issues`.
    UNASSIGNED : str
        A user was unassigned from an issue or pull request.
        Available for `issues`, `pull_request`.
    UNLABELED : str
        A label was removed from an issue or pull request.
        Available for `issues`, `pull_request`.
    UNLOCKED : str
        Conversation on an issue or pull request was unlocked.
        Available for `issues`, `pull_request`.
    UNPINNED : str
        An issue was unpinned from a repository.
        Available for `issues`.
    """

    ASSIGNED = "assigned"
    AUTO_MERGE_DISABLED = "auto_merge_disabled"
    AUTO_MERGE_ENABLED = "auto_merge_enabled"
    CLOSED = "closed"
    CONVERTED_TO_DRAFT = "converted_to_draft"
    CREATED = "created"
    DELETED = "deleted"
    DEMILESTONED = "demilestoned"
    DEQUEUED = "dequeued"
    EDITED = "edited"
    ENQUEUED = "enqueued"
    LABELED = "labeled"
    LOCKED = "locked"
    MILESTONED = "milestoned"
    OPENED = "opened"
    PINNED = "pinned"
    READY_FOR_REVIEW = "ready_for_review"
    REOPENED = "reopened"
    REVIEW_REQUEST_REMOVED = "review_request_removed"
    REVIE_REQUESTED = "review_requested"
    SYNCHRONIZE = "synchronize"
    TRANSFERRED = "transferred"
    UNASSIGNED = "unassigned"
    UNLABELED = "unlabeled"
    UNLOCKED = "unlocked"
    UNPINNED = "unpinned"

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return self is other

    def __hash__(self):
        return hash((self.__class__, self.value))


class RepositoryVisibility(_Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    INTERNAL = "internal"

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return self is other

    def __hash__(self):
        return hash((self.__class__, self.value))


class MergeMethod(_Enum):
    MERGE = "merge"
    SQUASH = "squash"
    REBASE = "rebase"

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return self is other

    def __hash__(self):
        return hash((self.__class__, self.value))


class MergeCommitMessage(_Enum):
    PR_TITLE = "PR_TITLE"
    PR_BODY = "PR_BODY"
    BLANK = "BLANK"

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return self is other

    def __hash__(self):
        return hash((self.__class__, self.value))


class MergeCommitTitle(_Enum):
    PR_TITLE = "PR_TITLE"
    MERGE_MESSAGE = "MERGE_MESSAGE"

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return self is other

    def __hash__(self):
        return hash((self.__class__, self.value))


class SquashMergeCommitMessage(_Enum):
    PR_BODY = "PR_BODY"
    COMMIT_MESSAGES = "COMMIT_MESSAGES"
    BLANK = "BLANK"

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return self is other

    def __hash__(self):
        return hash((self.__class__, self.value))


class SquashMergeCommitTitle(_Enum):
    PR_TITLE = "PR_TITLE"
    COMMIT_OR_PR_TITLE = "COMMIT_OR_PR_TITLE"

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return self is other

    def __hash__(self):
        return hash((self.__class__, self.value))


class TeamPrivacy(_Enum):
    OPEN = "open"
    CLOSED = "closed"
    SECRET = "secret"

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return self is other

    def __hash__(self):
        return hash((self.__class__, self.value))


class SecretSource(_Enum):
    """The source of a secret used in a workflow."""

    ACTIONS = "Actions"
    DEPENDABOT = "Dependabot"
    CODESPACES = "Codespaces"
    NONE = "None"

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return self is other

    def __hash__(self):
        return hash((self.__class__, self.value))
