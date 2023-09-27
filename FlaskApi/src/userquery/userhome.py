import pymysql
import configparser
import datetime

config = configparser.ConfigParser()
config.read('./config.ini')


class user_query(object):
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

    def cha(self):
        conn = self.sql_connect()
        cursor = conn.cursor()
        today = datetime.datetime.today()
        today = today.strftime('%Y-%m-%d')
        today = '2022-08-22'
        # 虚假的今天
        sql = 'select province,today_confirm,today_abroad,today_local from daily_spider where date = "' + str(
            today) + '";'
        cursor.execute(sql)
        print(sql)
        a = cursor.fetchall()
        lis = []
        for n, i in enumerate(a):
            province_data = {'province': i[0], 'total': i[1], 'foreign': i[2], 'local': i[3]}
            lis.append(province_data)
        return lis

    # 处理feedback
    def pos_feedback(self, desc, email):
        conn = self.sql_connect()
        cursor = conn.cursor()
        today = datetime.datetime.today()
        today = today.strftime('%Y-%m-%d %H-%M-%S')
        try:
            tup = (today, desc, email, 0)
            sql = 'insert into feedback values{}'.format(tup)
            cursor.execute(sql)
            conn.commit()
        except:
            return 1
        cursor.close()
        conn.close()
        return 0

    def get_feedback(self):
        conn = self.sql_connect()
        cursor = conn.cursor()
        sql = 'select * from feedback where done = ' + '0' + ';'
        cursor.execute(sql)
        a = cursor.fetchall()
        print(a)
        cursor.close()
        conn.close()
