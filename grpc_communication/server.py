#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/10/19
@des:   grpc.server
"""

import time
from concurrent import futures
import grpc

from grpc_communication.proto.proto_test_pb2 import demo_reply
from grpc_communication.proto.proto_test_pb2_grpc import DemoServicer, add_DemoServicer_to_server

from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
from flask import Flask

from utils import log_utils
from grpc_communication.app_test.test_app import manager as test_manager

logger = log_utils.getLogger()

manager = Flask(__name__)


class MyDemo(DemoServicer):
    def __init__(self):
        pass

    def demo_func(self, request, context):
        print("request name:{0}, age:{1}".format(request.name, request.age))
        return demo_reply(message=request.name, salary=10000)


def grpc_server(port=50051):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_DemoServicer_to_server(MyDemo(), server)
    server.add_insecure_port("0.0.0.0:9340")
    server.start()
    logger.info("Start server successful")
    app = DispatcherMiddleware(
        manager,
        {
            '/test': test_manager
        }
    )
    run_simple(hostname="0.0.0.0", port=9350, application=app, threaded=True)
    try:
        while True:
            time.sleep(3)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    grpc_server()
