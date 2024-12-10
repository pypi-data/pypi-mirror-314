from github_contexts.property_dict import PropertyDict as _PropertyDict


class License(_PropertyDict):

    def __init__(self, license_data: dict):
        super().__init__(license_data)
        return

    @property
    def key(self) -> str:
        return self._data["key"]

    @property
    def name(self) -> str:
        return self._data["name"]

    @property
    def node_id(self) -> str:
        return self._data["node_id"]

    @property
    def spdx_id(self) -> str:
        return self._data["spdx_id"]

    @property
    def url(self) -> str:
        return self._data["url"]
