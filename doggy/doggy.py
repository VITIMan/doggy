# -*- coding: utf-8 -*-

"""
Doggy

Simple output text, sometimes fails.
"""
# python3 imports
from __future__ import absolute_import, unicode_literals, print_function

# python imports
import ConfigParser
import os
import datetime
import random
import optparse
import time


def doggy(process_id, crash_probability, *args, **kwargs):
    """Main function for doggy
    """
    while True:
        # No execute so quickly, just for readability
        time.sleep(0.1)

        # Text output
        print("Process {} {} text".format(
            process_id,
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")))

        # Probability of crashing
        is_crashing = random.randrange(0, 101)
        if is_crashing < crash_probability:
            print("Process {} CRASHING".format(process_id))
            break

"""
python doggy.py -c 3
"""

if __name__ == "__main__":
    """
    """
    pid = os.getpid()
    # You can change via prompt
    CRASHING_PROBABILITY = 1

    # Parse options
    p = optparse.OptionParser()

    p.add_option("-p", "--probability",
                 action="store",
                 type="int",
                 help="crashing probability",
                 dest="crash")
    p.add_option("-c", "--configfile",
                 action="store",
                 type="string",
                 help="config file path",
                 dest="config_file")

    opt, args = p.parse_args()

    if opt.crash is not None:
        if opt.crash < 0 or opt.crash > 100:
            raise TypeError(
                "Invalid value for parameter crash (between 0 to 100)")
        CRASHING_PROBABILITY = opt.crash
        print("{} Using command line args".format(pid))

    elif opt.config_file is not None:
        config_file = opt.config_file
        # config file
        config = ConfigParser.SafeConfigParser()
        config.read(config_file)
        config_scope = "doggy"
        CRASHING_PROBABILITY = int(config.get(config_scope, "crashing_probability"))
        print("{} Using config file".format(pid))
    else:
        print("{} Using default configuration".format(pid))

    # Execute doggy
    doggy(pid, CRASHING_PROBABILITY)
