import json
# from sqlite3 import IntegrityError
from flask_apscheduler import APScheduler
import pymysql
import configparser

import requests
from pymysql import IntegrityError

config = configparser.ConfigParser()
config.read('config.ini')


class spider(object):
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

    def get_html(self, url, headers):
        try:

            r = requests.get(url=url, headers=headers, verify=False, timeout=(5, 5))
            r.encoding = r.apparent_encoding
            status = r.status_code
            print(status)
            # 将原始数据类型转换为json类型，方便处理
            data_json = json.loads(r.text)

            return data_json['data']['diseaseh5Shelf']['areaTree'][0]['children']
        except:
            print("爬取失败")

    def exec(self):
        url = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=localCityNCOVDataList,diseaseh5Shelf'
        headers = {
            'host': 'api.inews.qq.com',
            'Cookie': 'RK=WZs1bK2wci; ptcz=ea8a07d49585486e3e44a89dcc68ca452b7e3e1607307e0dd5ac4ddf566a10f1; pgv_pvid=4982926256; o_cookie=605286079; pac_uid=1_605286079; eas_sid=J1z6A4r7F589c0D5u8W9Q7i219; uin_cookie=o0605286079; ied_qq=o0605286079; LW_uid=c1x6i611w6k0s485k761e7O1E0; clickNums=1; ptui_loginuin=605286079; LW_sid=h1q6T6f3B3d2L0k6C3K911A293; skey=@Hc27a30cM; uin=o605286079',
            'Connection':'keep-alive',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62'
        }
        data = self.get_html(url, headers)
        conn = self.sql_connect()
        cursor = conn.cursor()
        for i in data:
            name = i['name']
            date = i['date']
            tc = i['today']['confirm']
            ta = i['today']['abroad_confirm_add']
            tl = i['today']['local_confirm_add']
            try:
                insert_word = (
                    name, date, tc, ta, tl)
                sql = 'insert into daily_spider values{}'.format(insert_word)
                cursor.execute(sql)

            except IntegrityError:
                sql = 'update daily_spider set today_confirm = "' + str(tc) + '",today_abroad = "' + str(
                    ta) + '", today_local = "' + str(tl) + '"where province = "' + str(name) + '" and date = "' + str(
                    date) + '";'
                cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
