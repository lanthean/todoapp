#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# @Author   https://github.com/lanthean
# @Created  05/01/2021
#
# @Package
"""

# Imports
import logging
import os
import pprint
from datetime import date

# Local imports
from tododb import tododb
from todocommon import todocsv

def _print(data):
    """
    pretty print
    """
    pp = pprint.PrettyPrinter()
    pp.pprint(data)

def test():
    td = tododb('test.db')
    # td.setup_db()
    directory = './todoist/'
    for csv_file in os.listdir(directory):
        if csv_file.endswith("_todoist.csv"):
            td.populate_db(os.path.join(directory, csv_file))
            # print(os.path.join(directory, csv_file))

    # print(td.get_db_columns('tasks'))
    # print(r)
    db_data = td.get_db_data('tasks', single=False)
    # pp = pprint.PrettyPrinter()
    # pp.pprint(db_data)
    for row in db_data.values():
        # print(row['date_completed'])
        if row['date_completed'] != "null":
            print(row)

    # tc = todocsv()
    # tc.load_csv4db('./csv/test.csv'); print(tc.db_data)
    # tc.load_csv('./csv/test.csv'); print(tc.csv_data)
    # for row in tc.db_data:
    #     # print(td.get_data4insert('tasks', tc.db_data[row]))
    #     td.save('tasks', tc.db_data[row])

def test_write():
    path = '/Users/lanthean/Documents/data/sandbox/github/todoapp'
    logging.debug("@test.py: init td")
    td = tododb(os.path.join(path, 'todoist.db'))
    logging.debug("@test.py: td.get_db_columns()")
    fields = td.get_db_columns('tasks')
    logging.debug("@test.py: td.get_db_data()")
    data = td.get_db_data('tasks')
    logging.debug("@test.py: init tc")
    tc = todocsv()
    logging.debug("@test.py: tc.write2file()")
    try:
        tc.write2file(os.path.join(path, 'test_output.csv'), fields, data)
    except Exception as e:
        logging.error("tc.write2file failed: {}".format(e))

def test_populate_db(destroy=False):
    """
    docstring
    @var destroy: Boolean (False) - Drop old DB and create clean DB if True
    """
    path = '/Users/lanthean/Documents/data/sandbox/github/todoapp'
    td = tododb(os.path.join(path, 'todoist.db'))
    if destroy: 
        td.setup_db()
    directory = '/Users/lanthean/Documents/data/work/docs/notes/todoist/'
    today = date.today().strftime("%Y%m%d")
    logging.debug("go through todoist csv exports and import data to db")
    for csv_file in os.listdir(directory):
        # if csv_file.endswith("_todoist.csv"):
        if csv_file.startswith(today) and csv_file.endswith("_todoist.csv"):
            td.populate_db(os.path.join(directory, csv_file))

def main():
    logging.basicConfig(level=logging.TRACE)
    logging.info("start")
    test_write()
    # test_populate_db()
    logging.info("end")

# boilerplate code to run the main function if it is not a import..
if __name__ == '__main__':
    main()
# EOF
###