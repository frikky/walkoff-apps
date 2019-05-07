#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import time
import random

import secret
import requests
import thehive4py
from thehive4py.api import TheHiveApi
from thehive4py.query import *
from thehive4py.models import Alert

from walkoff_app_sdk.app_base import AppBase

class TheHive(AppBase):
    """
    An example of a Walkoff App.
    Inherit from the AppBase class to have Redis, logging, and console logging set up behind the scenes.
    """
    __version__ = "0.0.3"
    app_name = "thehive"

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        self.thehive = TheHiveApi(secret.url, secret.apikey)
        super().__init__(redis, logger, console_logger)

    async def show_secret(self):
        return "url=%s, apikey=%s" % (secret.url, secret.apikey)

    async def get_case_count(self, title_query):
        response = self.thehive.find_cases(query=String("title:'%s'" % title_query), range='all', sort=[])
        casecnt = len(response.json())
        return casecnt

    async def string_contains(self, field, string_check):
        if string_check in field.lower():
            return True

        return False

    async def string_startswith(self, field, string_check):
        if field.lower().startswith(string_check):
            return True

        return False

    # Gets an item based on input. E.g. field_type = Alert
    async def get_item(self, field_type, cur_id): 
        newstr = ""
        ret = ""
        if field_type.lower() == "alert":
            ret = self.thehive.get_alert(cur_id) 
        elif field_type.lower() == "case":
            ret = self.thehive.get_case(cur_id)
        elif field_type.lower() == "case_observables":
            ret = self.thehive.get_case_observables(cur_id)
        elif field_type.lower() == "case_task":
            ret = self.thehive.get_case_task(cur_id)
        elif field_type.lower() == "case_tasks":
            ret = self.thehive.get_case_tasks(cur_id)
        elif field_type.lower() == "case_template":
            ret = self.thehive.get_case_tasks(cur_id)
        elif field_type.lower() == "linked_cases":
            ret = self.thehive.get_linked_cases(cur_id)
        elif field_type.lower() == "task_log":
            ret = self.thehive.get_task_log(cur_id)
        elif field_type.lower() == "task_logs":
            ret = self.thehive.get_task_logs(cur_id)
        else:
            return "%s is not implemented. See https://github.com/frikky/walkoff-integrations for more info." % field_type

        newstr = str(ret.json()).replace("\'", "\"")
        newstr = newstr.replace("True", "true")
        newstr = newstr.replace("False", "false")
        return newstr

    # Not sure what the data should be
    async def update_field_string(self, field_type, cur_id, field, data):
        # This is kinda silly but..
        if field_type.lower() == "alert":
            newdata = {}

            if data.startswith("%s"): 
                ticket = self.thehive.get_alert(cur_id)
                if ticket.status_code != 200:
                    pass 
            
                newdata[field] = "%s%s" % (ticket.json()[field], data[2:])
            else:
                newdata[field] = data

            # Bleh
            url = "%s/api/alert/%s" % (secret.url, cur_id)
            if field == "status":
                if data == "New" or data == "Updated":
                    url = "%s/markAsUnread" % url
                elif data == "Ignored": 
                    url = "%s/markAsRead" % url

                ret = requests.post(
                    url,
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer %s' % secret.apikey
                    }
                )
            else:
                ret = requests.patch(
                    url,
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer %s' % secret.apikey
                    }, 
                    json=newdata,
                )

            return ret.status_code
        else:
            return 0

if __name__ == "__main__":
    asyncio.run(TheHive.run(), debug=True)
