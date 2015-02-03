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
from multiprocessing import Pool, Process

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
    """Laund doggy process
    """
    doggy_proc = subprocess.Popen([sys.executable,
                                   doggy_path],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  bufsize=1)

    # while True:
    #     line = doggy_proc.stdout.readline()
    #     if line != '':
    #         #the real code does filtering here
    #         print("test:", line.rstrip())
    #     else:
    #         break
    # for line in io.open(doggy_proc.stdout.fileno()):
    #     print(line.rstrip())
    #     # logger.info(line.rstrip())

    for line in iter(doggy_proc.stdout.readline, b''):
        # print(line.rstrip())
        logger.info(line.rstrip())
    output = doggy_proc.communicate()[0]
    exit_code = doggy_proc.returncode



if __name__ == "__main__":
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

    # Launch initial processes
    task_list = {}
    logger_list = {}
    # pool = Pool(processes=int(current_args["num_processes"]))

    for i in xrange(int(current_args["num_processes"])):
        process = Process(target=launch_doggy,
                          args=(current_args["doggy_path"]))
        # task_list[i] = pool.apply_async(launch_doggy,
        #                                 [current_args["doggy_path"]],
        #                                 callback=my_callback)
        # launch_doggy(current_args["doggy_path"])
        task_list[i] = process
        # logger_list[i] = logger
        process.start()
    # pool.close()
    # pool.join()

    while True:
        for i in task_list.keys():
            process = task_list[i]
            if process.exitcode is not None and not process.is_alive():
                print("process:{} pool:{} terminated, restarting...".format(
                    process.pid, i))
                task_list[i] = Process(target=launch_doggy,
                                       args=(current_args["doggy_path"],))
                task_list[i].start()
                # task_list[i] = pool.apply_async(launch_doggy,
                #                    [current_args["doggy_path"]])
            elif process.exitcode < 0 and process.exitcode is not None:
                print("{} Process with error or terminate".format(i))
                # process = pool.apply_async(launch_doggy,
                #                            [current_args["DOGGY_PATH"]])
