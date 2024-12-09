import requests
from time import perf_counter as time_now

from wise.utils.monitoring import HTTP_CLIENT_DURATION

DEFAULT_TIMEOUT = 60


class HTTPClientWithMonitoring:
    def __init__(self, service_name: str, session: requests.Session | None = None):
        self.service_name = service_name
        self._client = session or requests.Session()

    def request(self, method: str, url: str, _api_name: str = "unset", **kwargs):
        kwargs.setdefault("timeout", DEFAULT_TIMEOUT)
        start = time_now()
        success = "false"

        try:
            response = self._client.request(method, url, **kwargs)
            success = "true"
            return response
        finally:
            HTTP_CLIENT_DURATION.labels(
                self.service_name, _api_name, method, success
            ).observe(time_now() - start)

    def get(self, url: str, _api_name: str = "unset", **kwargs):
        return self.request("GET", url, _api_name=_api_name, **kwargs)

    def post(self, url: str, _api_name: str = "unset", **kwargs):
        return self.request("POST", url, _api_name=_api_name, **kwargs)

    def put(self, url: str, _api_name: str = "unset", **kwargs):
        return self.request("PUT", url, _api_name=_api_name, **kwargs)

    def patch(self, url: str, _api_name: str = "unset", **kwargs):
        return self.request("PATCH", url, _api_name=_api_name, **kwargs)

    def delete(self, url: str, _api_name: str = "unset", **kwargs):
        return self.request("DELETE", url, _api_name=_api_name, **kwargs)

    def __setattr__(self, key, value):
        if key in ["service_name", "_client"]:
            super().__setattr__(key, value)
        else:
            setattr(self._client, key, value)

    def __getattr__(self, item):
        return getattr(self._client, item)
