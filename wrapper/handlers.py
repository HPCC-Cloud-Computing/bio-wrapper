# Copyright 2016 - Nguyen Quang "TechBK" Binh.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from aiohttp import web
from managers import SwiftManager, Job
import json


def to_json(func):
    def wrapped(self, request):
        return web.Response(body=json.dumps(func(self, request)).encode('utf-8'))
    return wrapped


def handle_errors(func):
    def wrapped(self, request):
        data = {}
        try:
            data = func(self, request)
        except Exception as e:
            print(e)
            data = {
                'status': False,
                'job_id': None,
                'error_message': str(e)
            }
        finally:
            return data

    return wrapped


class JobsHandler(object):
    def __init__(self, loop):
        self.loop = loop
        self.list_of_job = {}
        self._taskid = 0

    def _get_job_id(self):
        self._taskid += 1
        return str(self._taskid)

    @to_json
    @handle_errors
    def runtask(self, request):
        """
        POST method

        :param request: require user, key, tenant, container_name, auth_version, authurl
        :return: job_id
        """
        request.post()
        # user = request.POST['user']
        # key = request.POST['key']
        # tenant = request.POST['tenant']
        # container_name = request.POST['container_name']
        # auth_version = request.POST['auth_version']
        # authurl = request.POST['authurl']

        # swift = SwiftManager(user, key, tenant, container_name, auth_version, authurl)
        # job = Job(swift)
        job = Job(False)
        self.list_of_job[self._get_job_id()] = job
        data = {
            'status': True,
            'job_id': str(self._taskid),
        }
        return data

    @to_json
    @handle_errors
    def listjobs(self, request):
        """
        GET method
        :param request: no requirement
        :return:
        """
        if not self.list_of_job:
            return {
                'empty': True,
                'jobs': '[]',
                'status': True
            }
        else:
            return {
                'empty': False,
                'jobs': self.list_of_job.keys(),
                'status': True
            }
        # data = {
        #     'jobs': self.list_of_job.keys(),
        #     'status': True,
        # }


    @to_json
    @handle_errors
    def job(self, request):
        job_id = request.POST['job_id']
        job = self.list_of_job[job_id]
        result, error = yield from job.process
        data = {
            'job_id': job_id,
            'job_status': job.process.done() and not job.error,
            'result': result,
            'status': True
        }
        return data

    @to_json
    @handle_errors
    def canceljob(self, request):
        """
        POST method
        If prevstatus = True -> job is running, else job is already done.
        :param request: require job_id
        :return:
        """
        request.post()
        job_id = request.POST['job_id']
        job = self.list_of_job[job_id]
        data = {
            'prevstatus': job.process.cancel(),
            'job_id': job_id,
            'status': True,
        }
        return data
