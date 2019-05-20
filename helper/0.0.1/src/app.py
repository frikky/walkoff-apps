#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import time
import random

import requests
import json
import re

from walkoff_app_sdk.app_base import AppBase

class Helper(AppBase):
    """
    An example of a Walkoff App.
    Inherit from the AppBase class to have Redis, logging, and console logging set up behind the scenes.
    """
    __version__ = "0.0.1"
    app_name = "helper"

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    async def echo(self, input_data):
        print(input_data)
        # Special attributes from https://github.com/nsacyber/WALKOFF/blob/0c35c64bf89c2958cc04d523df35ca744603e72f/app_sdk/walkoff_app_sdk/common/workflow_types.py -> variables
        try:
            return input_data.value
        except AttributeError:
            return input_data

    async def get_json_field(self, input_data, field):
        # Formatting..
        print(input_data)
        input_data = str(input_data).replace("\'", "\"")
        input_data = input_data.replace("True", "true")
        input_data = input_data.replace("False", "false")
        input_data = input_data.replace("None", "\"\"")
        print(input_data)

        try:
            input_data = json.loads(input_data)
        except TypeError as e:
            print(e)
            return e
        except json.decoder.JSONDecodeError as e:
            print(e)
            return e

        try:
            return str(input_data[field])
        except KeyError as e:
            return "%s doesn't exist: %s" % (field, e)

        # Return first match 
    async def re_submatch(self, pattern, input_string):
        print("%s, %s" % (pattern, input_string))
        try:
            ret = re.search(pattern, input_string)
        except re.error as e:
            return "Error in pattern: %s" % e

        if ret:
            return ret.group(1)

        return ""
    
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
    asyncio.run(Helper.run(), debug=True)
