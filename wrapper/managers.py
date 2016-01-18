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
import os
import shutil
import swiftclient
import swiftclient.exceptions
import asyncio
# import config
# from swiftclient.exceptions import ClientException


class SwiftManager(object):
    def __init__(self, user, key, tenant, authurl, input_file, output_file, directory):
        """
        step1: khoi tao Swift Connection
        step2: tao directory tuong ung voi job_id
        step3: parsing input file, kiem tra input file da ton tai hay chua
        step4: parsing output file, kiem tra output container da ton tai hay chua, neu chua thi tao moi

        :param user:
        :param key:
        :param tenant:
        :param str input_file:
        :param str output_file:
        :param authurl:
        :param str directory:
        :return:
        """
        # step1
        self.conn = swiftclient.client.Connection(
                user=user,
                tenant_name=tenant,
                auth_version='2.0',
                key=key,
                authurl=authurl
        )

        # step2
        os.makedirs(directory, exist_ok=True)
        # os.makedirs(os.path.dirname(directory), exist_ok=True)
        self.directory = directory

        # step3
        if input_file:
            self.input_container, list_of_input_file = input_file.split('/')
            self.input_file = list_of_input_file.split('|')
            self.input_path = []
            for file in self.input_file:
                self.conn.head_object(self.input_container, file)
                self.input_path.append("%s/%s" % (directory, file))
            # self.input_path = "%s/%s" % (directory, self.input_file)

        # step4
        if output_file:
            self.output_container, self.output_file = output_file.split('/')
            try:
                self.conn.head_container(self.output_container)
            except swiftclient.exceptions.ClientException:
                self.conn.put_container(self.output_container)
            self.output_path = "%s/%s" % (directory, self.output_file)

    # @asyncio.coroutine
    # def get_data(self):
    #     """
    #     Lay data tu swift, luu vao thu muc data/
    #     :return: string: tra ve duong dan toi file data thu dc
    #     """
    #     obj_tuple = self.conn.get_object(self.input_container, self.input_file)
    #     return obj_tuple[1].decode('utf-8')

    @asyncio.coroutine
    def get_and_save_data(self):
        """
        Get input file and save it!!!
        """
        if hasattr(self, 'input_file'):
            for file, file_path in zip(self.input_file, self.input_path):
                obj_tuple = self.conn.get_object(self.input_container, file)
                with open(file_path, 'wb') as f:
                    f.write(obj_tuple[1])

    @asyncio.coroutine
    def put_data(self, out=None):
        """
        Lay du ket qua co duoc gui len swift
        :param out:
        :return: tra ve
        """
        if hasattr(self, 'output_file'):
            if out:
                return self.conn.put_object(self.output_container,
                                            self.output_file,
                                            contents=out,
                                            content_type='text/plain')

            # filepath = "%s/%s" % (self.directory, self.output_file)
            # os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(self.output_path, 'r') as f:
                return self.conn.put_object(self.output_container,
                                            self.output_file,
                                            contents=f.read(),
                                            content_type='text/plain')

    @asyncio.coroutine
    def clear_directory(self):
        """
        Clear directory.
        :return:
        """
        return shutil.rmtree(self.directory, True)


class Job(object):
    def __init__(self, swift, cm):
        """

        :param SwiftManager swift:
        :return:
        """
        # self.first = is_first
        # self.is_first(is_first)
        self.swift = swift
        self.error = False
        self.cm = cm
        self.process = asyncio.async(self.run_process())

    # def is_first(self, is_first):
    #     """
    #     Check first.
    #     Khong ro co can ham nay ko nua :v
    #     if is_first: Error, because job need get_data.
    #     :param bool is_first:
    #     :return:
    #     :raises Exception: First :v
    #     """
    #
    #     # if not is_first:
    #     #     self.error = True
    #     #     raise Exception("Job have to be first")
    #     if is_first:
    #         self.error = True
    #         raise Exception("Job have to be not first")

    @asyncio.coroutine
    @asyncio.coroutine
    def run_process(self):
        """
        :return:
        :raise Exception: set self.error = True
        """
        try:
            # if not self.first:
            #     dictionary = yield from self.swift.get_data()
            #     commandline = u"ls -l %s" % dictionary
            # else:
            #     commandline = u"ls -l"

            yield from self.swift.get_and_save_data()

            cm = self.cm.format(input_file=self.swift.input_path, output_file=self.swift.output_path)

            # Create the subprocess, redirect the standard output into a pipe
            create = asyncio.create_subprocess_shell(cmd=cm,
                                                     stdout=asyncio.subprocess.PIPE,
                                                     stderr=asyncio.subprocess.PIPE)
            # Wait for create
            proc = yield from create  # proc is Process Instance

            out, err = yield from proc.communicate()

            if err:
                raise Exception("Out: %s | Error: %s" % (out.decode('utf-8'), err.decode('utf-8')))

            if '{output_file}' in self.cm:
                yield from self.swift.put_data()
            else:
                yield from self.swift.put_data(out)
            yield from self.swift.clear_directory()
            return out
        except Exception as e:
            self.error = True
            yield from self.swift.clear_directory()
            raise e

    def __str__(self):
        return "Job Object"
