import sys
from tkinter import messagebox

import pymysql


class LinkDatabase():
    '''
    创建一个mysql的连接，并提供了大量获取数据库信息的方法
    '''

    def __init__(self, host, user, passwd, port):
        try:
            self.db = pymysql.connect(host=host,
                                      user=user,
                                      passwd=passwd,
                                      port=port,
                                      charset='utf8',
                                      cursorclass=pymysql.cursors.DictCursor)
            self.cursor = self.db.cursor()
            self.db_is_exist = True
        except:
            error_buf = sys.exc_info()
            messagebox.showerror(error_buf[0].__name__, error_buf[1])
            self.db_is_exist = False
        self.db_is_ues = False

    def get_databases(self):
        if not self.db_is_exist:
            return -1
        try:
            self.cursor.execute('show databases')
        except:
            error_buf = sys.exc_info()
            messagebox.showerror(error_buf[0].__name__, error_buf[1])
        return self.cursor.fetchall()

    def set_database(self, db):
        try:
            self.cursor.execute('use %s' % db)
        except:
            error_buf = sys.exc_info()
            messagebox.showerror(error_buf[0].__name__, error_buf[1])
            return False
        self.db_is_ues = True
        return True

    def show_tables(self):
        if not self.db_is_ues:
            return -1
        self.cursor.execute('show tables')
        self.tables = self.cursor.fetchall()
        return self.tables

    def get_table(self, name):
        if not self.db_is_exist:
            return -1
        try:
            self.cursor.execute('SELECT * FROM %s' % name)
        except:
            error_buf = sys.exc_info()
            messagebox.showerror(error_buf[0].__name__, error_buf[1])
            return 'no table'
        return self.cursor.fetchall()

    def __del__(self):
        try:
            self.cursor.close()
            self.db.close()
        except AttributeError:
            pass

    def get_table_row(self, name):
        if not self.db_is_exist:
            return -1
        try:
            # mysql语句：查找某数据库某表的字段名
            self.cursor.execute(
                'select column_name from information_schema.columns where table_name="%s" and table_schema="basketball_test"' %
                name[0])
        except:
            error_buf = sys.exc_info()
            messagebox.showerror(error_buf[0].__name__, error_buf[1])
            return 'no table'
        return self.cursor.fetchall()


if __name__ == '__main__':
    buf = LinkDatabase("192.168.1.201", "test", "L*&k34HC98K.kDG%KH", 3307)
    # array = buf.get_databases()
    buf.set_database('basketball_test')
    from Util import dataanalyze

    table_names = buf.show_tables()
    table_names = dataanalyze.change_dic(table_names)
    table_names.pop(0)
    resute = []
    for name in table_names:
        content = buf.get_table_row(name)
        content = dataanalyze.change_dic(content)
        if ['team_id'] not in content:
            resute.append(name)
    resute_1 = []

    for name in resute:
        content = buf.get_table_row(name)
        content = dataanalyze.change_dic(content)
        if ['alliance_id'] not in content:
            resute_1.append(name)

    key = 0
    for i in resute_1:
        print(i[0])
        key += 1
    print(key)
