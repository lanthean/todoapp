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
import sqlite3

# Local imports
from todocommon import todocsv

class tododb():
    """
    docstring
    """
    def __init__(self, db_file='todoapp.db'):
        self.db_file = db_file
        self.c = False
        self.conn = False

        self.logging = logging.getLogger("tododb")
        self.logging.debug("tododb initiation")
        # eo: tododb()

    def setup_db(self):
        self.connect()
        # Create table tasks
        self.c.execute('''DROP TABLE tasks;''')
        self.c.execute('''CREATE TABLE tasks
                            (task_id integer, content text, due datetime, due_is_recurring boolean,
                             date_added datetime, date_completed datetime, child_order integer,
                             parent_id integer, project_id text, user_id text, assigned_by_uid text,
                             is_deleted boolean, responsible_uid text)''')
        # Create table projects
        # c.execute('''CREATE TABLE projects
        #             (id integer, description text)''')
        # Create table tags
        self.c.execute('''DROP TABLE tags;''')
        self.c.execute('''CREATE TABLE tags
                            (id integer, description text)''')
        # Save (commit) the changes
        self.commit()
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        self.close()
        # eo: setup_db()

    def connect(self):
        """ Connect to SQLite3 DB """
        if not self.conn:
            self.conn = sqlite3.connect(self.db_file)
            self.c = self.conn.cursor()
        # eo: connect()

    def commit(self):
        """ Commit to SQLite3 DB """
        self.conn.commit()
        # eo: commit()

    def close(self):
        """ Close connection to SQLite3 DB """
        self.conn.close()
        self.conn = False
        self.c = False
        # eo: close()

    def select(self, table, where = None, fields='*'):
        self.connect()
        if where is None:
            self.c.execute('''SELECT {} FROM {};'''.format(fields, table))    
        else:
            self.c.execute('''SELECT {} FROM {} WHERE {};'''.format(fields, table, where))
        return self.c.fetchall()
        # eo: select()

    def get_db_columns(self, table):
        self.connect()
        columns = zip(*self.c.execute("PRAGMA table_info('{}')".format(table)).fetchall())[1]
        return columns
        # eo: get_db_columns()

    def insert(self, table, keys, data):
        self.connect()
        self.logging.debug('''INSERT INTO {}({}) VALUES({});'''.format(table, keys, data))
        self.c.execute('''INSERT INTO {}({}) VALUES({});'''.format(table, keys, data))
        self.commit()
        # eo: insert()

    def update(self, table, data, where, limit = None):
        self.connect()
        if limit is not None:
            self.logging.debug('''UPDATE {} SET {} WHERE {} LIMIT {};'''.format(table, data, where, limit))
            self.c.execute('''UPDATE {} SET {} WHERE {} LIMIT {};'''.format(table, data, where, limit))
        else:
            self.logging.debug('''UPDATE {} SET {} WHERE {};'''.format(table, data, where))
            self.c.execute('''UPDATE {} SET {} WHERE {};'''.format(table, data, where))
        # eo: update()

    def save(self, table, db_data):
        """ Save data to DB """
        self.connect()
        try:
            where = "{}='{}'".format('task_id', db_data['task_id'])
        except:
            self.logging.error("task_id is missing in db_data:")
            self.logging.error(db_data)
            exit()

        if len(self.select(table, where)) == 0:
            keys, data = self.get_data4insert(table, db_data)
            self.insert(table, keys, data)
        else:
            self.update(table, self.get_data4update(table, db_data), where)
        self.commit()
        #eo: save()

    def get_data4insert(self, table, data):
        """
        docstring
        """
        column_names = self.get_db_columns(table)
        ret_data = ""
        ret_keys = ""
        first = True
        for k in data:
            if k in column_names:
                if first:
                    ret_keys += "'{}'".format(k)
                    ret_data += "'{}'".format(data[k])
                    first = False
                else:
                    ret_keys += ",'{}'".format(k)
                    ret_data += ",'{}'".format(data[k])
        self.logging.debug('get_data4insert: data = {}'.format(data))
        self.logging.debug('get_data4insert: ret_data = {}'.format(ret_data))
        return ret_keys, ret_data
        # eo: get_data4insert()

    def get_data4update(self, table, data):
        """
        docstring
        """
        column_names = self.get_db_columns(table)
        ret_data = ""
        first = True
        for k in data:
            if k in column_names:
                if first:
                    ret_data += "{}='{}'".format(k, data[k])
                    first = False
                else:
                    ret_data += "AND {}='{}'".format(k, data[k])
        return ret_data
        # eo: get_data4update()

    def populate_db(self):
        """
        docstring
        """
        tc = todocsv()
        tc.load_csv4db('./csv/test.csv')
        for row in tc.db_data:
            self.save('tasks', tc.db_data[row]) 
        self.close()
        # eo: populate_db()

class dbobject(tododb):
    """
    DBObject of todo project
    """
    def __init__(self):
        self.logging = logging.getLogger("tododb>dbobject")
        self.logging.debug("dbobject initiation")
        # eo: dbobject()

    # eo: dbobject

class dbcollection(dbobject):
    """
    Collection of DBObjects of todo project
    """
    def __init__(self):
        self.logging = logging.getLogger("tododb>dbobject>dbcollection")
        self.logging.debug("dbcollection initiation")
        # eo: dbcollection()

    # eo: dbcollection

# EOF
###