#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# @Author   https://github.com/lanthean
# @Created  05/01/2021
#
# @Package  todoapp
"""

# Imports
import os
import logging
import csv

# local imports
from todocommon import todocsv

class todoist2todotxt():
    """
    docstring
    """
    def __init__(self):
        self.csv_data = {}
        self.logging = logging.getLogger("todoist2todotxt")
        # eo: todoist2todotxt()

    def convert(self):
        """ Convert loaded todoist csv data to todotxt output """
        pass
        # eo: convert()
    # eo: todoist2todotxt

# boilerplate code to run the main function if it is not a import..
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    t2tx = todoist2todotxt()
    t2tx.logging.info("start")
    tc = todocsv()
    tc.load_csv('./csv/20210104_143000_todoist.csv')
    for key in tc.csv_data:
        print("{}: {}".format(key, tc.csv_data[key]['project_id']))
    t2tx.logging.info("finish")

# EOF
###