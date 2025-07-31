from configparser import ConfigParser
import logging

import requests

class UpdateHelper:
    def __init__(self, config: ConfigParser):
        self.config = config

    def get_latest_version(self) -> str | None:
        latest_version = None
        try:
            url = self.config.get("update", "check_url")
            headers = {"Accept": "application/vnd.github.v3+json"}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                tags = response.json()
                if tags:
                    latest_version = tags[0]['name']  # latest tag name
        except Exception as e:
            logging.exception(e)
        return latest_version

    