import json

import pymysql
import requests
import configparser

config = configparser.ConfigParser()
config.read('./config.ini')

class manag(object):
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

    def pand(self, usrname, passwd):
        conn = self.sql_connect()
        cursor = conn.cursor()
        sql = 'select * from manager where usrname="' + str(usrname) + '" and passwd="' + str(passwd) + '";'
        print(sql)
        cursor.execute(sql)
        a = cursor.fetchall()
        print(a)
        if len(a) > 0:
            return {'status': 'pass'}
        else:
            return {'status': 'wrong'}

    def confm(self, data):
        conn = self.sql_connect()
        cursor = conn.cursor()
        kk = []
        for j in data:
            k = j.replace('[', '').replace(']', '').replace('"', '').split(',')
            kk.append(k)
        mm = ()
        for j in kk:
            tup = tuple(j)
            jing, wei = self.cha_baidu(j[4], j[1])
            if jing != '0':
                tup = tup + tuple([jing, wei])
                sql = 'insert into new_liudiao values{}'.format(tup)
                cursor.execute(sql)
                conn.commit()
        sql = 'delete from zancun'
        cursor.execute(sql)
        conn.commit()
        sql = 'select * from zancun'
        cursor.execute(sql)
        a = cursor.fetchall()
        cursor.close()
        conn.close()
        return 'ok'

    def cha_baidu(self, kw, procity):
        url = 'https://api.map.baidu.com/place/v2/search?query=' + kw + '&region=' + procity + '&output=json&ak=aYNu34AYwt3QTaApv4nNH5tSAxe7NIGe'
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.50',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        }
        r = requests.get(url, headers=header, timeout=30)
        js = r.text
        jj = json.loads(js)
        res = jj['results']
        if len(res) > 0:
            if 'location' in res[0].keys():
                jing = res[0]['location']['lng']
                wei = res[0]['location']['lat']
            else:
                jing = '0'
                wei = '0'
        else:
            jing = '0'
            wei = '0'
        return jing, wei
