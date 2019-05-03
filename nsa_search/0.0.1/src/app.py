#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import time
import random

import secret
import requests
import json
import re

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
        if len(search_string) <= 1:
            return ""

        ret = requests.get("%s/api/search/%s" % (secret.url, search_string))

        # Prevent it from running infinite
        cnt = 0
        maxcnt = 180
        while(1):
            if ret.json()["done"]:
                newstr = str(ret.json()).replace("\'", "\"")
                newstr = newstr.replace("True", "true")
                newstr = newstr.replace("False", "false")
                return newstr
    
            cnt += 1
            if cnt == maxcnt:
                return ""

            time.sleep(1)

    # Return first match 
    async def re_submatch(self, pattern, input_string):
        ret = re.search(pattern, input_string)
        if ret:
            return ret.group(1)

        return ""
    
    # Requires json object of NSA search
    # Searches for a specific search in NSA (e.g. CVE)
    async def find_search_object(self, input_object, search_type, array_name, object_name):
        try:
            input_object = json.loads(input_object)
        except TypeError:
            pass

        for item in input_object[array_name]:
            print("NOT FOUND YET!!")
            if item[object_name] == search_type:
                print("FOUND!!")
                return item
    
        return {}

if __name__ == "__main__":
    asyncio.run(NSA.run(), debug=True)
