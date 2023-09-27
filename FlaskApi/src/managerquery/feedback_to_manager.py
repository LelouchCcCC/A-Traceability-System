import configparser
import pymysql

config = configparser.ConfigParser()
config.read('./config.ini')


class ftm(object):
    def sql_connect(self):
        conn = pymysql.connect(
            host=str(config.get('config', 'mysql_host').replace(',', '')),
            user=str(config.get('config', 'mysql_user').replace(',', '')),
            password=str(config.get('config', 'mysql_passwd').replace(',', '')),
            database='yiqing',
            charset='utf8',
            # autocommit=True,    # 如果插入数据，， 是否自动提交? 和conn.commit()功能一致。
        )
        return conn

    def get_feedback(self):
        conn = self.sql_connect()
        cursor = conn.cursor()
        sql = 'select date,email,content from feedback where done = ' + '0' + ' Order By date;'
        cursor.execute(sql)
        a = cursor.fetchall()
        da = []
        for i in a:
            dic = {}
            tm3 = i[0]
            nyr = str(tm3.year) + '-' + str(tm3.month) + '-' + str(tm3.day)
            dic['date'] = nyr
            dic['con'] = i[1]
            dic['email'] = i[2]
            da.append(dic)
        cursor.close()
        conn.close()
        return da

    # feedback的0-->1(暂时处理有问题，不是很准)
    def pos01(self, date, email):
        conn = self.sql_connect()
        cursor = conn.cursor()
        sql = 'update feedback set done=1 where date = '+date+' and email = '+email+';'
        print(sql)
        cursor.execute(sql)
        cursor.close()
        conn.close()

    def addman(self, name, password):
        conn = self.sql_connect()
        cursor = conn.cursor()
        try:
            word = (name, password, 1)
            sql = 'insert into user values{}'.format(word)
            cursor.execute(sql)
            res = {'code': '20000', 'message': '提交成功'}
        except:
            res = {'code': '20001', 'message': '提交失败，请再次检查'}
        conn.commit()
        cursor.close()
        conn.close()
        return res

    def watchman(self):
        conn = self.sql_connect()
        cursor = conn.cursor()
        sql = '''select * from user;'''
        cursor.execute(sql)
        a = cursor.fetchall()
        data = []
        for i in a:
            dic = {}
            if i[2] != 0:
                dic['name'] = i[0]
                dic['password'] = i[1]
                data.append(dic)
        return data

