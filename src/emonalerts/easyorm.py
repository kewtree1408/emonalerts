#!/usr/bin/env python
"""
EasyORM - wrapper class for create, insert, update and get data from tables.
"""

import sqlite3
import logging
import emonalerts.settings as settings

logger = logging.getLogger(__name__)


class EasyORM(object):
    def __init__(self, table_name):
        self.table_name = table_name
        self.conn = sqlite3.connect(settings.DB_NAME)

    def _array_to_query(self, array):
        """
        Transform array into query:
        1. Put comma after every element
        2. Erase the last comma and the space
        """
        query = ','.join(array)
        query.rsplit(',')
        return query

    def create_table(self, **kwargs):
        """
        Create table. If it's already exist, then skip it.
        :params: kwargs is a dict with key as a column and value as a column type
        """
        create_query = self._array_to_query([f'{column}, {kwargs[column]}' for column in kwargs])

        cur = self.conn.cursor()
        try:
            cur.execute(f'CREATE TABLE "{self.table_name}" ({create_query})')
        except sqlite3.OperationalError as err:
            logger.info(err)
        cur.close()

    def insert_record(self, **kwargs):
        """
        Insert a first record into the table.
        :params: kwargs is a dict with key as a column and value for the column
        """
        column_query = self._array_to_query(list(kwargs.keys()))
        values_query = self._array_to_query([f'"{kwargs[column]}"' for column in kwargs])

        cur = self.conn.cursor()
        cur.execute(f'INSERT INTO "{self.table_name}" ({column_query}) VALUES ({values_query})')
        self.conn.commit()
        cur.close()

    def update_record(self, **kwargs):
        """
        Update a first record on the table.
        :params: kwargs is a dict contains the other dicts.
        Example:
        {
            'set_data': {
                column_name1: value_name1,
                column_name2: value_name2,
                ...
            },
            'where_data': {
                column_name3: value_name3,
                column_name4: value_name4,
            }
        }
        """

        set_data = [
            '{c}="{v}"'.format(c=column, v=kwargs['set_data'][column])
            for column in kwargs['set_data']
        ]
        set_query = self._array_to_query(set_data)

        where_data = [
            '{c}="{v}"'.format(c=column, v=kwargs['where_data'][column])
            for column in kwargs['where_data']
        ]
        where_query = self._array_to_query(where_data)

        cur = self.conn.cursor()
        cur.execute(f'UPDATE "{self.table_name}" SET {set_query} WHERE {where_query}')
        self.conn.commit()
        cur.close()

    def get_data(self, **kwargs):
        """
        Get data from the table.
        :params: kwargs is a dict contains the <get_data> list and <where_data> dict.
        Example:
        {
            'get_data': [column_name1, column_name2, ...],
            'where_data': {
                column_name1: value_name1,
                column_name2: value_name2,
            }
        }
        :return: return dict data regards to the kwargs['get_data'] columns.
        If there are few results from db, one the first one will be returned.
        """

        get_data = list(kwargs['get_data'])
        get_query = self._array_to_query(get_data)

        where_data = [
            '{c}="{v}"'.format(c=column, v=kwargs['where_data'][column])
            for column in kwargs['where_data']
        ]
        where_query = self._array_to_query(where_data)

        cur = self.conn.cursor()
        cur.execute(f'SELECT {get_query} FROM "{self.table_name}" WHERE {where_query}')
        return_data = cur.fetchone()
        cur.close()
        return return_data
