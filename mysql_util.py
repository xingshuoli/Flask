# -*- coding: utf-8 -*-
"""
@Time ： 2024/4/22 上午10:32
@Auth ： lixingshuo
@File ：mysql_util.py
@IDE ：PyCharm
@mail ： lixingshuo@gotion.com.cn
"""
import pymysql
import logging
import traceback
import sys


class MysqlUtil:
    def __init__(self, host='localhost', port=3306, user='127.0.0.1', password='123456', db='db_test'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                        db=self.db)
            self.cursor = self.conn.cursor()
        except Exception as e:
            logging.error(f"connect mysql error: {e}")
            sys.exit(1)

    def insert(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            logging.error(f"insert error: {e}")
            self.conn.rollback()

    def delete(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            logging.error(f"delete error: {e}")
            self.conn.rollback()
        finally:
            self.cursor.close()
            self.conn.close()

    def update(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            logging.error(f"update error: {e}")
            self.conn.rollback()
        finally:
            self.cursor.close()
            self.conn.close()

    def fetch_all(self, sql):
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
        except Exception as e:
            sys.exc_info()
            logging.error(f"fetch all error: {e}")
            self.conn.rollback()
        finally:
            self.cursor.close()
            self.conn.close()
        return results

    def fetch_one(self, sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
        except Exception as e:
            logging.error(f"fetch one error: {e}")
            self.conn.rollback()
        finally:
            self.cursor.close()
            self.conn.close()
        return result
