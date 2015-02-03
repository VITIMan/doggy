# -*- coding: utf-8 -*-
"""
Doggy-Wrapper

Wrapper for doggy process, this process try to maintain available the doggy
process
"""
# python3 imports
from __future__ import absolute_import, unicode_literals, print_function

# python imports
import io
import logging
import sys
import datetime
import subprocess
import time

# project imports
from conf import default_configs, check_command_line, check_file_config
from log_rotation import CompressedTimedRotatingFileHandler


def create_timed_rotating_log(path, when, interval, compress_mode):
    """Create a timed rotating log given intervals and set a compress mode

    Returns:
        A logger handler
    """
    logger = logging.getLogger("doggy_log")
    logger.setLevel(logging.INFO)

    handler = CompressedTimedRotatingFileHandler(path,
                                                 when=when,
                                                 interval=interval,
                                                 backupCount=5,
                                                 compress_mode=compress_mode)
    logger.addHandler(handler)
    return logger


def launch_doggy(doggy_path):
    """Launch doggy process

    Create a subprocess for the doggy application, prepare the standard output
    to be collected by the wrapper.

    Returns:
        the doggy process
    """
    doggy_proc = subprocess.Popen([sys.executable,
                                   doggy_path],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  bufsize=1)

    return doggy_proc

if __name__ == "__main__":
    """Main entrance of app

    Parse the configuration and execute and relaunch the doggy process
    """
    current_args = default_configs
    # check command line
    current_args.update(check_command_line(**current_args))
    # Parsing config
    current_args.update(check_file_config(**current_args))

    # Creating log handler
    logger = create_timed_rotating_log(current_args["log_file"],
                                       current_args["block_time"],
                                       int(current_args["rotating_timer"]),
                                       current_args["compress_mode"])

    print(current_args)
    # Launch initial processes
    task_list = {}
    logger_list = {}

    processes = {i: launch_doggy(current_args["doggy_path"])
                 for i in xrange(int(current_args["num_processes"]))}

    # Log the output and relaunch the processes
    while True:
        for i in processes.keys():
            process = processes[i]
            for line in iter(process.stdout.readline, b''):
                logger.info(line.rstrip())
            if process.poll() is not None:
                output = process.communicate()[0]
                print("Reset process, task:{}, pid:{}".format(i, process.pid))
                processes[i] = launch_doggy(current_args["doggy_path"])
