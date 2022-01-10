#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/08/11
@des:   
"""

import argparse

JOB_FUNC = []
DATA_FUNC = []
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f',
        '--function',
        type=str,
        choices=(JOB_FUNC + DATA_FUNC),
        required=True,
        help="function to call",
    )
    parser.add_argument(
        '-c', '--config', required=False, type=str, help="runtime conf path"
    )

    parser.add_argument('-j', '--job_id', required=False, type=str, help="job id")
    parser.add_argument(
        '-dn', '--dataset_name', required=False, type=str, help="dataset name"
    )
