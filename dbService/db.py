#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb
from conf.config import Setting
from log.accessLog import Logger


logger = Logger().logger


class Db(object):

    def __init__(self):
        setting = Setting()
        # 也可以使用字典进行连接参数的管理
        config = {
            'host': setting.config["db"]["host"],
            'port': setting.config["db"]["port"],
            'user': setting.config["db"]["username"],
            'passwd': setting.config["db"]["passwd"],
            'db': setting.config["db"]["dbname"],
            'charset': 'utf8'
        }
        self.conn = MySQLdb.connect(**config)
        # 如果使用事务引擎，可以设置自动提交事务，或者在每次操作完成后手动提交事务conn.commit()
        # self.conn.autocommit(1)  # conn.autocommit(True)
        self.cursor = self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)

    def fetch_records(self, sql):
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            self.conn.commit()
            pass
        except Exception, e:
            print 'str(Exception):\t', str(Exception)
            print 'str(e):\t\t', str(e)
        return results

    # 普通提交
    # noinspection PyBroadException
    def commit_record(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception, e:
            logger.error("创建供应商异常: %s, %s, 异常sql: %s", str(Exception),str(e), sql)

    # 事务提交
    # noinspection PyBroadException
    def transaction_commit(self, sql):
        try:
            for i in sql:
                self.cursor.execute(i)
            self.conn.commit()
        except Exception, e:
            self.conn.rollback()
            logger.error("创建同款数据异常: %s, %s", str(Exception), str(e))

    def __del__(self):
        self.cursor.close()
        self.conn.close

if __name__=="__main__":
    db = Db()
