#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:  BryanGa
@time:  2021/08/11
@des:   
"""
import subprocess
import typing

subp = subprocess.Popen(["python",
                         "fate_flow_path",
                         "-f",
                         "job_log",
                         "-j",
                         "1234",
                         "-o",
                         "log_dir"],
                        shell=False,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)


def get_eggroll_version() -> typing.Optional[str]:
    return typing.Optional[str]


if __name__ == "__main__":
    t = get_eggroll_version()
    t = 22
    # s =
    print(t << 2)
    print(t)
    pass
