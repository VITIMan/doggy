# -*- coding: utf-8 -*-
"""
log_rotation.py

The Timed Rotating logger subclassed to be compressed
"""
# python3 imports
from __future__ import absolute_import, unicode_literals, print_function

# python imports
import os
import glob
import datetime

import logging
from logging.handlers import TimedRotatingFileHandler


COMPRESSION_SUPPORTED = {}
try:
   import gzip
   COMPRESSION_SUPPORTED['gz'] = gzip
except ImportError:
   pass

try:
   import zipfile
   COMPRESSION_SUPPORTED['zip'] = zipfile
except ImportError:
   pass


class CompressedTimedRotatingFileHandler(TimedRotatingFileHandler):
    """Subclassing TimedRotatedFileHandler to compress the logs rotated
    previously
    """
    def __init__(self, *args, **kwargs):
        compress_mode = kwargs.pop('compress_mode')

        try:
            self.compress_cls = COMPRESSION_SUPPORTED[compress_mode]
        except KeyError:
            raise ValueError('"%s" compression method not supported.' % compress_mode)

        super(CompressedTimedRotatingFileHandler, self).__init__(*args, **kwargs)

    def doRollover(self):
        """

        Given the rollover compress the most recent backup to a given compress
        mode
        """
        super(CompressedTimedRotatingFileHandler, self).doRollover()

        # Compress the old log.
        # Retrieve the most recent
        dirname = os.chdir(os.path.dirname(self.baseFilename))
        backup_filenames = glob.glob(self.baseFilename + ".*")
        backup_filenames_suffix = [backup_file.split(".")[-1]
                                   for backup_file in backup_filenames]
        backup_filenames_datetime = [
            datetime.datetime.strptime(backup_file, self.suffix)
            for backup_file in backup_filenames_suffix
        ]
        recent_date = max(backup_filenames_datetime)
        recent_date_index = [i for i, d in enumerate(backup_filenames_datetime)
                             if d == recent_date][0]

        newest_backup = backup_filenames[recent_date_index]
        # newest_backup = max([f for f in glob.iglob(self.baseFilename + ".*")
        #                      if not f.endswith('.gz')],
        #                     key=os.path.getctime)

        gz_file = newest_backup + '.gz'
        with open(newest_backup) as log:
            with self.compress_cls.open(gz_file, 'wb') as comp_log:
                comp_log.writelines(log)

        os.rename(gz_file, newest_backup)
        # os.remove(newest_backup)
        print("Log: compressing backup log {}".format(newest_backup))
