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

import swiftclient
import asyncio
# from swiftclient.exceptions import ClientException


class SwiftManager(object):
    def __init__(self, user, key, tenant, container_name, auth_version='2.0', authurl='http://controller:5000/v2.0'):
        self.conn = swiftclient.client.Connection(
                user=user,
                tenant_name=tenant,
                auth_version=auth_version,
                key=key,
                authurl=authurl
        )

        if not container_name:
            self.container_name = 'example_container'
            self.conn.put_container('example_container')

    def get_data(self):
        """
        Lay data tu swift, luu vao thu muc data/
        :return: tra ve duong dan toi file data thu dc
        """
        pass

    def put_data(self):
        """
        Lay du ket qua co duoc gui len swift
        :return: tra ve
        """
        pass


class Job(object):
    def __init__(self, swift):
        self.swift = swift
        self.error = False
        self.process = asyncio.async(self.run_process())

    @asyncio.coroutine
    def run_process(self):
        # dictionary = self.swift.get_data()
        # dictionary = '/'
        commandline = u"ll" #% dictionary
        # Create the subprocess, redirect the standard output into a pipe
        create = asyncio.create_subprocess_shell(cmd=commandline,
                                                 stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        # Wait for create
        proc = yield from create  # proc is Process Instance

        out, err = yield from proc.communicate()
        if err:
            print(err)
            self.error = True
        return out, err

    def __str__(self):
        return "Job Object"
