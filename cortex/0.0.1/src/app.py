#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import urllib3

from cortex4py.api import Api
import cortex4py 

from walkoff_app_sdk.app_base import AppBase

class Cortex(AppBase):
    """
    An example of a Walkoff App.
    Inherit from the AppBase class to have Redis, logging, and console logging set up behind the scenes.
    """
    __version__ = "0.0.1"
    app_name = "cortex"



    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.api = Api("http://localhost:9001", "APIKEY", cert=False)
        super().__init__(redis, logger, console_logger)

    async def get_available_analyzers(self, datatype):
        try:
            analyzers = self.api.analyzers.find_all({}, range='all')
        except cortex4py.exceptions.ServiceUnavailableError as e:
            return [e]
        except cortex4py.exceptions.AuthorizationError as e:
            return [e]
        except cortex4py.exceptions.NotFoundError as e:
            return [e]

        if len(analyzers) == 0:
            return []

        all_results = []
        for analyzer in analyzers:
            if not datatype in analyzer.dataTypeList:
                continue

            all_results.append(analyzer.name)

        return all_results

    async def run_available_analyzers(self, data, datatype, message="", tlp=1):
        analyzers = await self.get_available_analyzers(datatype)

        alljobs = []
        for analyzer in analyzers:
            try:
                job = self.api.analyzers.run_by_name(analyzer, {
                    'data': data,
                    'dataType': datatype,
                    'tlp': tlp,
                    'message': message,
                }, force=1)

                alljobs.append(job.id)
            except cortex4py.exceptions.ServiceUnavailableError as e:
                return [e]
            except cortex4py.exceptions.AuthorizationError as e:
                return [e]
            except cortex4py.exceptions.NotFoundError as e:
                return [e]

        return alljobs

    async def run_analyzer(self, analyzer_name, data, datatype, message="", tlp=1):
        try:
            job = self.api.analyzers.run_by_name(analyzer_name, {
                'data': data,
                'dataType': datatype,
                'tlp': tlp,
                'message': message,
            }, force=1)
        except cortex4py.exceptions.ServiceUnavailableError as e:
            return e
        except cortex4py.exceptions.AuthorizationError as e:
            return e
        except cortex4py.exceptions.NotFoundError as e:
            return e

        return job.id

    async def get_analyzer_result(self, id):
        try:
            report = self.api.jobs.get_report(id).report
        except cortex4py.exceptions.ServiceUnavailableError as e:
            return e
        except cortex4py.exceptions.AuthorizationError as e:
            return e
        except cortex4py.exceptions.NotFoundError as e:
            return e

        return report 

if __name__ == "__main__":
    asyncio.run(Cortex.run(), debug=True)
