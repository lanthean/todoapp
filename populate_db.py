#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# @Author   https://github.com/lanthean
# @Created  15/01/2021
#
# @Package
"""

# Imports
import logging
from datetime import date
import os

# Local imports
from tododb import tododb
from todocommon import todocsv

# Main function
def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.info("start")
    td = tododb('todoist.db')
    directory = '/Users/lanthean/Documents/data/work/docs/notes/todoist/'
    today = date.today().strftime("%Y%m%d")
    logging.debug("go through todoist csv exports and import data to db")
    for csv_file in os.listdir(directory):
        if csv_file.startswith(today) and csv_file.endswith("_todoist.csv"):
            td.populate_db(os.path.join(directory, csv_file))
    
    logging.info("end")

# boilerplate code to run the main function if it is not a import..
if __name__ == '__main__':
    main()
# EOF
###