#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/10/19
@des:   grpc.client
"""

from __future__ import print_function

import grpc

from grpc_communication.proto.proto_test_pb2 import demo_request
from grpc_communication.proto.proto_test_pb2_grpc import DemoStub


def run(host, port):
    channel = grpc.insecure_channel(f'{host}:{port}')
    stub = DemoStub(channel)
    response = stub.demo_func(demo_request(name='tom', age=32))
    print("message: {0}: salary:{1}".format(response.message, response.salary))


if __name__ == '__main__':
    run(host='localhost', port=50051)
