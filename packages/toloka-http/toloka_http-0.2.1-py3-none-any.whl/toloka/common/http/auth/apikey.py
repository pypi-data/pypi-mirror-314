from toloka.common.http.auth.common import AuthHeaders


class ApiKeyHeaders(AuthHeaders):
    def __init__(self, api_key: str, key_prefix: str = 'ApiKey') -> None:
        self.api_key = api_key
        self.key_prefix = key_prefix

    def get_headers(self) -> dict[str, str]:
        api_key = self.api_key.removeprefix(f'{self.key_prefix} ')
        return {'Authorization': f'{self.key_prefix} {api_key}'}
