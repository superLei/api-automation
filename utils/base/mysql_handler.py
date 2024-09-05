# -*- coding: UTF-8 -*-

import pymysql
import logging
from utils.base.env_conf_util import get_db_config


"""
__author__ = maxsu
"""


class MysqlHandler:
    def __init__(self, mysql_conf):
        self.mysql_conf = mysql_conf
        self.con = None
        self.cur = None

    def connect(self):
        try:
            self.con = pymysql.connect(
                **self.mysql_conf,
                cursorclass=pymysql.cursors.DictCursor,  # type: ignore
            )
            logging.debug("Connected to MySQL database")
            self.cur = self.con.cursor()
        except pymysql.MySQLError as e:
            logging.error("Failed to connect to MySQL database: %s", e)

    def query(self, sql_exp):
        try:
            self.connect()
            with self.con.cursor() as cursor:  # type: ignore
                cursor.execute(sql_exp)
                self.con.commit()  # type: ignore
                result = cursor.fetchall()
                return result
        except pymysql.MySQLError as e:
            logging.error("Failed to execute query: %s", e)
            return None
        finally:
            self.close()

    def update(self, sql_exp):
        try:
            self.connect()
            with self.con.cursor() as cursor:  # type: ignore
                cursor.execute(sql_exp)
                self.con.commit()  # type: ignore
                return True
        except pymysql.MySQLError as e:
            logging.error("Failed to execute update: %s", e)
            self.con.rollback()  # type: ignore
            return False
        finally:
            self.close()

    def close(self):
        try:
            if self.cur:
                self.cur.close()
            if self.con:
                self.con.close()
            logging.debug("Database connection closed")
        except Exception as e:
            logging.error("Failed to close database connection: %s", e)


if __name__ == "__main__":
    db_conf = get_db_config(project_name="toc")
    mysql_handler = MysqlHandler(db_conf)
    sql = "SELECT id FROM server_tab WHERE is_disabled = 1"
    data = mysql_handler.query(sql)
    print(data)
