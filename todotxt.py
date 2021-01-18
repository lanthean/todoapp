#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# @Author   https://github.com/lanthean
# @Created  06/01/2021
#
# @Package  todoapp
"""

# Imports
import logging
import pprint

# local imports
from todocommon import todocsv
from tododb import tododb

class todotxt():
    """
    docstring
    """
    def __init__(self):
        self.db_data = {}
        self.logging = logging.getLogger("todotxt")
        # eo: todoist2todotxt()

    def get_db_data(self, db_file = "todoapp.db"):
        """ Convert loaded todoist csv data to todotxt output """
        td = tododb(db_file)
        self.db_data = td.select('tasks')
        return self.db_data
        # eo: get_db_data()
    # eo: todoist2todotxt

# boilerplate code to run the main function if it is not a import..
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    tx = todotxt()
    tx.logging.info("start")
    tx.get_db_data('test.db')
    output = ""
    td = tododb('test.db')
    columns = td.get_db_columns('tasks')
    
    data = tmp_data = {}
    for row in tx.db_data:
        if len(columns) == len(row):
            for i in range(0,len(columns)):
                tmp_data[columns[i]] = row[i]

            data[row[0]] = tmp_data
            tmp_data = {}
        
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(data)
    tx.logging.info("finish")

        # if isinstance(row, tuple):
        #     for value in row:
        #         output += "".join(str(value))
        #         output += " "
        #     output += "\n"
        # else:
        #     output += "".join(str(row))
        #     output += " "

# EOF
###