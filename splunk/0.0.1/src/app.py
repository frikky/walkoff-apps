#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import time
import random
import requests
import urllib3
import splunk

from walkoff_app_sdk.app_base import AppBase

class Splunk(AppBase):
    """
    Splunk integration for WALKOFF with some basic features
    """
    __version__ = "0.0.1"
    app_name = "splunk"

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        self.verify = False
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        super().__init__(redis, logger, console_logger)

    async def echo(self, input_data):
        return input_data 

    async def SplunkQuery(self, url, username, password, query, result_limit=100, earliest_time="-24h", latest_time="now"):
        auth = (username, password)

        # "latest_time": "now"
        query = {
            "search": "| search %s" % query,
            "exec_mode": "normal",
            "count": result_limit,
            "earliest_time": earliest_time,
            "latest_time": latest_time
        }

        print("Current search: %s" % query["search"])

        try:
            ret = splunk.run_search(auth, url, query)
        except requests.exceptions.ConnectTimeout as e:
            print("Timeout: %s" % e)
            return 0 

        if ret.status_code != 201:
            print("Bad status code: %d" % ret.status_code)
            return 0 

        search_id = ret.json()["sid"]

        print("Search ID: %s" % search_id)

        ret = splunk.get_search(auth, url, search_id)
        if len(ret.json()["entry"]) == 1:
            count = ret.json()["entry"][0]["content"]["resultCount"]
            print("Result: %d" % count)
            return count

        print("No results (or wrong?): %d" % (len(ret.json()["entry"])))
        return 0
        
if __name__ == "__main__":
    asyncio.run(Splunk.run(), debug=True)
