from typing import Mapping, Protocol


class AuthHeaders(Protocol):
    def get_headers(self) -> Mapping[str, str]: ...
