#!/usr/bin/python3

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

import asyncio
import getopt
import sys
from handlers import JobsHandler
from aiohttp import web

__author__ = 'techbk'

SERVICE_IP = '0.0.0.0'
SERVICE_PORT = 8080


def get_opt(argv):
    _ip = SERVICE_IP
    _port = SERVICE_PORT
    try:
        opts, args = getopt.getopt(argv, "hi:p:", ["ip=", "port="])
    except getopt.GetoptError:
        print('service.py -i <ip> -p <port>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('service.py -i <ip> -p <port>')
            sys.exit()
        elif opt in ("-i", "--ip"):
            _ip = arg
        elif opt in ("-p", "--port"):
            _port = int(arg)

    return _ip, _port


@asyncio.coroutine
def init(_loop, _ip, _port):
    """
    - Khoi tao Jobshandler
    - Tao handler va run service
    :param _loop:
    :param _ip:
    :param _port:
    """
    jobs = JobsHandler(_loop)

    app = web.Application(loop=_loop)
    app.router.add_route('POST', '/runtask/', jobs.runtask, name='runtask')
    app.router.add_route('GET', '/listjobs/', jobs.listjobs, name='listjobs')
    app.router.add_route('GET', '/job/', jobs.job, name='job')
    app.router.add_route('POST', '/canceljob/', jobs.canceljob, name='canceljob')

    _handler = app.make_handler()
    _srv = yield from _loop.create_server(_handler, _ip, _port)
    print("Server started at http://{ip}:{port}".format(ip=_ip, port=_port))
    return _srv, _handler


if __name__ == "__main__":
    ip, port = get_opt(sys.argv[1:])
    loop = asyncio.get_event_loop()
    srv, handler = loop.run_until_complete(init(loop, ip, port))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
