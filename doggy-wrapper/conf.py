# -*- coding: utf-8 -*-
# python3 imports
from __future__ import absolute_import, unicode_literals, print_function

# python imports
import ConfigParser
import optparse


# DEFAULT CONFIGS
default_configs = {
    "config_file": "doggy-wrapper.conf",
    "num_processes": 3,
    "rotating_timer": 5,
    "log_file": "wrapper.log",
    "compress_mode": "gz",
    "doggy_path": "../doggy/doggy.py",  # in relative path
    "block_time": "m"  # https://docs.python.org/2/library/logging.handlers.html#timedrotatingfilehandler
}


def check_command_line(**kwargs):
    """The command line configuration

    Returns:
        dictionary with overrided arguments
    """
    p = optparse.OptionParser()

    p.add_option("-c", "--config",
                 action="store",
                 type="string",
                 help="location of config file",
                 dest="config_file")
    p.add_option("-p", "--processes",
                 action="store",
                 type="int",
                 help="Number of doggy processes",
                 dest="num_processes")
    p.add_option("-r", "--rotating",
                 action="store",
                 type="int",
                 help="Every time the log is rotated",
                 dest="rotating_timer")
    p.add_option("-l", "--logfile",
                 action="store",
                 type="string",
                 help="location of log file",
                 dest="log_file")
    p.add_option("-d", "--doggy",
                 action="store",
                 type="string",
                 help="location of doggy process",
                 dest="doggy_path")
    p.add_option("-b", "--blocktime",
                 action="store",
                 type="string",
                 help="rotation by seconds, minutes, hours, days",
                 dest="block_time")
    p.add_option("--compression",
                 action="store",
                 type="choice",
                 help="compression type: gz, zip",
                 dest="compress_mode",
                 choices=["gz", "zip"])

    opt, args = p.parse_args()

    new_values = {}

    for key in kwargs.keys():
        if getattr(opt, key, None) is not None:
            new_values[key] = getattr(opt, key)
    print(new_values)
    return new_values


def check_file_config(**kwargs):
    """Check config file for doggy-wrapper

    Returns:
        dictionary with overrided arguments
    """
    config = ConfigParser.SafeConfigParser()
    config.read(kwargs["config_file"])
    config_scope = "doggy-wrapper"

    new_values = {}
    for key in default_configs.keys():
        try:
            new_values[key] = config.get(config_scope, key)
        except:
            # Argument not specified
            pass

    return new_values
