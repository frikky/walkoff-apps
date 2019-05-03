#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import time
import random

import secret
import requests
import json

from walkoff_app_sdk.app_base import AppBase

class NSA(AppBase):
    """
    An example of a Walkoff App.
    Inherit from the AppBase class to have Redis, logging, and console logging set up behind the scenes.
    """
    __version__ = "0.0.1"
    app_name = "nsa_search"

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    async def show_secret(self):
        return "url=%s" % (secret.url)

    # Return object
    async def run_search(self, search_string):
        ret = requests.get("%s/api/search/%s" % (secret.url, search_string))
        while(1):
            if ret.json()["done"]:
                return ret.text
    
            time.sleep(1)
    
    # Requires json object of NSA search
    # Searches for a specific search in NSA (e.g. CVE)
    async def find_search_object(self, input_object, search_type, array_name, object_name):
        try:
            input_object = json.loads(input_object)
        except TypeError:
            pass

        for item in input_object[array_name]:
            if item[object_name] == search_type:
                return item
    
        return {}

if __name__ == "__main__":
    asyncio.run(NSA.run(), debug=True)
