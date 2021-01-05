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
# Local imports
from tododb import tododb
from todocommon import todocsv

def main():
    logging.basicConfig(level=logging.DEBUG)
    td = tododb('test.db')
    td.setup_db()
    td.populate_db()
    print(td.get_db_columns('tasks'))
    print(td.select('tasks'))

    # tc = todocsv()
    # tc.load_csv4db('./csv/test.csv'); print(tc.db_data)
    # tc.load_csv('./csv/test.csv'); print(tc.csv_data)
    # for row in tc.db_data:
    #     # print(td.get_data4insert('tasks', tc.db_data[row]))
    #     td.save('tasks', tc.db_data[row])

# boilerplate code to run the main function if it is not a import..
if __name__ == '__main__':
    main()
# EOF
###