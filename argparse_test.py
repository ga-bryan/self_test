#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/08/11
@des:   
"""

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('c', '--config', required=False, type=str, help="runtime conf path")
    print(parser.parse_args().c)
