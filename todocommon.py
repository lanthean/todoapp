#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
# @Author   https://github.com/lanthean
# @Created  05/01/2021
#
# @Package  todoapp
"""

# Imports
import logging
import csv
import io

class todocsv():
    """
    ToDo CSV module
    """
    def __init__(self):
        self.csv_data = {}
        self.db_data = {}
        self.logging = logging.getLogger("todocsv")
        # eo: todocsv()

    def load_csv(self, file_name):
        """ Load todoist csv, parse it (projects with tasks with subtasks) """
        self.logging.debug("load_csv: load csv from file")
        with open(file_name, 'r') as csvfile:
            csv_data = csv.DictReader(csvfile)
            for row in csv_data:
                self.csv_data[row['id']]=row
        # eo: load_csv()

    def load_csv4db(self, file_name):
        """ Load todoist csv, parse it (projects with tasks with subtasks) """
        self.logging.debug("load_csv: load csv from file")
        with open(file_name, 'r') as csvfile:
            db_data = csv.DictReader(csvfile)
            for row in db_data:
                self.db_data[row['id']] = {
                    'task_id': row['id'],
                    'content': row['content'],
                    'due': row['due'],
                    'due_is_recurring': row['due.is_recurring'],
                    'date_added': row['date_added'],
                    'date_completed': row['date_completed'],
                    'child_order': row['child_order'],
                    'parent_id': row['parent_id'],
                    'project_id': row['project_id'],
                    'user_id': row['user_id'],
                    'assigned_by_uid': row['assigned_by_uid'],
                    'is_deleted': row['is_deleted'],
                    'responsible_uid': row['responsible_uid']
                    }
        # eo: load_csv()

    def to_utf8(self, lst):
        return [str(elem).encode('utf-8') for elem in lst]

    def write2file(self, file_name, fields, data, db_file='./todoapp.db'):
        """
        Write data to csv file
        """
        with io.open(file_name, 'w', encoding='utf8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=str(fields))
            writer.writeheader()
            for row in data.values():
                writer.writerow(str(row))
        # eo: write2file()
    # eo: todocsv
# EOF
###