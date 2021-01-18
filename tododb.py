#!/usr/bin/env python3
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
        self.db_columns = {}

        self.logging = logging.getLogger("tododb")
        # self.logging.debug("tododb initiation")
        # eo: tododb()

    def setup_db(self):
        self.connect()
        # Create table tasks
        try:
            self.c.execute('''DROP TABLE tasks;''')
        except:
            self.logging.warning("setup_db() - drop table tasks failed")        
        self.c.execute('''CREATE TABLE tasks
                            (task_id integer, content text, due datetime, due_is_recurring boolean,
                             date_added datetime, date_completed datetime, child_order integer,
                             parent_id integer, project_id text, user_id text, assigned_by_uid text,
                             is_deleted boolean, responsible_uid text)''')
        # Create table projects
        # c.execute('''CREATE TABLE projects
        #             (id integer, description text)''')
        # Create table tags
        try:
            self.c.execute('''DROP TABLE tags;''')
        except:
            self.logging.warning("setup_db() - drop table tags failed")
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
            # self.conn = GetSqliteConnection(self.db_file)
            # self.conn.text_factory = lambda x: str(x, 'utf-8', 'ignore')            
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

    def select(self, table, where = None, fields='*', single=False):
        self.connect()
        if where is None:
            self.c.execute('''SELECT {} FROM {};'''.format(fields, table))
        else:
            self.c.execute('''SELECT {} FROM {} WHERE {};'''.format(fields, table, where))
        # return self.c.fetchall()
        if single:
            self.logging.debug("select(table={}, where={}, fields={}, single={})".format(table, where, fields, single))
            return self.c.fetchone()
        else:
            self.logging.debug("select(table={}, where={}, fields={}, single={})".format(table, where, fields, single))
            return self.c.fetchall()
        # eo: select()

    def insert(self, table, data, keys = None):
        self.connect()
        qmarks = ', '.join('?' * len(data))
        if keys is None:
            self.logging.debug('''INSERT INTO {}({}) VALUES({});'''.format(table, ", ".join(data.keys()), ", ".join(data.values())))
            query = '''INSERT INTO {}({}) VALUES({});'''.format(table, ", ".join(data.keys()), qmarks)
            self.logging.debug("'{}', {}".format(query, data.keys() + data.values()))
            self.c.execute(query, list(data.values()))
        else:
            self.logging.debug('''INSERT INTO {}({}) VALUES({});'''.format(table, keys, data))
            query = '''INSERT INTO {}({}) VALUES({});'''.format(table, qmarks, qmarks)
            self.c.execute(query, keys + data)
        # eo: insert()

    def update(self, table, data, where, limit = None):
        self.connect()
        if limit is not None:
            query = '''UPDATE {} SET {} WHERE {} LIMIT {};'''.format(table, ", ".join('{}=%s'.format(k) for k in data), where, limit)
            self.logging.debug('''UPDATE {} SET {} WHERE {} LIMIT {};'''.format(table, data, where, limit))
            self.c.execute(query, data.values())
        else:
            query = '''UPDATE {} SET {} WHERE {};'''.format(table, ", ".join('{}=?'.format(k) for k in data), where)
            self.logging.debug('''UPDATE {} SET {} WHERE {};'''.format(table, data, where))
            self.c.execute(query, list(data.values()))
        # eo: update()

    def save(self, table, db_data):
        """ Save data to DB (user does not have to check, if insert/update is needed - just saves) """
        self.connect()
        try:
            where = "{}='{}'".format('task_id', db_data['task_id'])
        except:
            self.logging.error("task_id is missing in db_data:")
            self.logging.error(db_data)
            exit()

        if len(self.select(table, where)) == 0:
            # keys, data = self.get_data4insert(table, db_data)
            self.insert(table, db_data)
        else:
            # self.update(table, self.get_data4update(table, db_data), where)
            self.update(table, db_data, where)
        self.commit()
        # eo: save()

    def get_data4insert(self, table, data):
        """
        docstring
        """
        # column_names = self.get_db_columns(table)
        # ret_data = ""
        # ret_keys = ""
        # first = True
        # for k in data:
        #     if k in column_names:
        #         if first:
        #             ret_keys += "'{}'".format(k)
        #             ret_data += "'{}'".format(data[k])
        #             first = False
        #         else:
        #             ret_keys += ",'{}'".format(k)
        #             ret_data += ",'{}'".format(data[k])
        self.logging.debug('get_data4insert: input data: {}'.format(data))
        self.logging.warning('get_data4insert: keys {}'.format(data.keys()))
        self.logging.warning('get_data4insert: values {}'.format(data.values()))
        return data.keys(), data.values()
        # self.logging.debug('get_data4insert: returned keys: {}'.format(ret_keys))
        # self.logging.debug('get_data4insert: returned data: {}'.format(ret_data))
        # return ret_keys, ret_data
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
        self.logging.debug('get_data4insert: input data: {}'.format(data))
        self.logging.debug('get_data4insert: returned data: {}'.format(ret_data))
        return ret_data
        # eo: get_data4update()

    def get_db_columns(self, table):
        self.logging.debug("tododb.get_db_columns() called")
        try:
            return self.db_columns[table]
        except:
            self.connect()
            try:
                self.c.execute("SELECT count(*) from {};".format(table))
                rs = self.c.fetchall()
                self.logging.debug("Number of records in db for table '{}' is '{}'".format(table, rs[0][0]))
            except:
                self.logging.error("DB is not initialized")
                exit()
            self.c.execute("PRAGMA table_info('{}')".format(table))
            rs2 = self.c.fetchall()
            self.logging.debug("PRAGMA: {}".format(rs2))
            
            try:
                self.db_columns[table] = zip(*self.c.execute("PRAGMA table_info('{}')".format(table)).fetchall())[1]
            except:
                self.logging.error("PRAGMA table_info failed")
                exit()

        # eo: get_db_columns()

    def get_db_data(self, table, single = False):
        """
        docstring
        """
        self.connect()
        column_names = self.get_db_columns(table)
        db_data = self.select(table, single=single)
        ret_data = {}
        if not single:
            j = 0
            for row in db_data:
                tmp_data = {}
                for i in range(0, len(column_names)):
                    tmp_data[column_names[i]] = row[i]
                ret_data[j] = tmp_data
                j += 1
        else:
            for i in range(0, len(column_names)):
                ret_data[column_names[i]] = db_data[i]
        # self.logging.debug('get_db_data: db_data: {}'.format(db_data))
        # self.logging.debug('get_db_data: returned data: {}'.format(ret_data))
        return ret_data
        # eo: get_data4update()

    def populate_db(self, csv_file = None):
        """
        docstring
        """
        tc = todocsv()
        if csv_file is not None:
            tc.load_csv4db(csv_file)
        else:
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
