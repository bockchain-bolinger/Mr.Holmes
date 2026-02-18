# ORIGINAL CREATOR: Luca Garofalo (Lucksi)
# AUTHOR: Luca Garofalo (Lucksi)
# Copyright (C) 2024 Lucksi <lukege287@gmail.com>
# License: GNU General Public License v3.0

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class Client:
    _session = None
    DEFAULT_TIMEOUT = 10

    @staticmethod
    def session():
        if Client._session is None:
            retry = Retry(
                total=3,
                connect=3,
                read=3,
                backoff_factor=0.5,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["GET", "HEAD"],
                raise_on_status=False,
            )
            adapter = HTTPAdapter(max_retries=retry)
            sess = requests.Session()
            sess.mount("http://", adapter)
            sess.mount("https://", adapter)
            Client._session = sess
        return Client._session

    @staticmethod
    def get(url, headers=None, proxies=None, timeout=None, allow_redirects=True):
        sess = Client.session()
        request_timeout = timeout if timeout is not None else Client.DEFAULT_TIMEOUT
        return sess.get(
            url=url,
            headers=headers,
            proxies=proxies,
            timeout=request_timeout,
            allow_redirects=allow_redirects,
        )

    @staticmethod
    def post(url, headers=None, data=None, timeout=None, allow_redirects=True):
        sess = Client.session()
        request_timeout = timeout if timeout is not None else Client.DEFAULT_TIMEOUT
        return sess.post(
            url=url,
            headers=headers,
            data=data,
            timeout=request_timeout,
            allow_redirects=allow_redirects,
        )

    @staticmethod
    def reset_session():
        if Client._session is not None:
            Client._session.close()
            Client._session = None
