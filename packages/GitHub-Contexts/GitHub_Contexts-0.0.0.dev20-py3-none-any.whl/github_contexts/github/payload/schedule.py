from github_contexts.github.payload.base import Payload


class SchedulePayload(Payload):

    def __init__(self, payload: dict):
        super().__init__(payload=payload)
        return

    @property
    def schedule(self) -> str:
        """The schedule that triggered the event."""
        return self._data["schedule"]