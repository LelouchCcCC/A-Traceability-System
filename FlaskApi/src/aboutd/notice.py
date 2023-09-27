import pymysql
import configparser
import datetime
import pandas as pd
config = configparser.ConfigParser()
config.read('./config.ini')

class Notice(object):
    def sql_connect(self):
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password=str(config.get('config', 'mysql_passwd').replace(',', '')),
            database='yiqing',
            charset='utf8',
            # autocommit=True,    # 如果插入数据，， 是否自动提交? 和conn.commit()功能一致。
        )
        return conn

    def no(self):
        conn = self.sql_connect()
        cursor = conn.cursor()
        sql = '''select title, link, abstract, DATE_FORMAT(time, '%Y-%m-%d %H:%i:%S') from notice'''
        cursor.execute(sql)
        notice = cursor.fetchall()
        data = []
        for i in notice:
            tab = {'title': i[0], 'link': i[1], 'abstract': i[2], 'time': i[3]}
            data.append(tab)
        return data

    def on(self, title, abstract, url, time, timeout):
        conn = self.sql_connect()
        cursor = conn.cursor()
        try:
            tup = (title, url, abstract, time, timeout)
            sql = """insert into notice values{}""".format(tup)
            cursor.execute(sql)
            conn.close()
            return {'status': 'success'}
        except:
            conn.close()
            return {'status': 'failure'}

