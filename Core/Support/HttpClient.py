# ORIGINAL CREATOR: Luca Garofalo (Lucksi)
# AUTHOR: Luca Garofalo (Lucksi)
# Copyright (C) 2024 Lucksi <lukege287@gmail.com>
# License: GNU General Public License v3.0

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class Client:

    @staticmethod
    def session():
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
        return sess

    @staticmethod
    def get(url, headers=None, proxies=None, timeout=10, allow_redirects=True):
        with Client.session() as sess:
            return sess.get(
                url=url,
                headers=headers,
                proxies=proxies,
                timeout=timeout,
                allow_redirects=allow_redirects,
            )
