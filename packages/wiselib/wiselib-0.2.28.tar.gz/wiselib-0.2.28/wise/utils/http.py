import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from wise.utils.http_requests import HTTPClientWithMonitoring


def create_session(
    retry_count=1, backoff_factor=0.5, service_name="unset"
) -> HTTPClientWithMonitoring:
    """
        Reference:
            https://stackoverflow.com/a/47475019/2581953
    :param retry_count:
    :param backoff_factor:
    :param service_name:
    :return:
    """
    session = requests.Session()
    retry = Retry(total=retry_count, backoff_factor=backoff_factor)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return HTTPClientWithMonitoring(service_name, session)
