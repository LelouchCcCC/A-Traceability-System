import json
# from sqlite3 import IntegrityError
from bs4 import BeautifulSoup
import pymysql
import configparser
from urllib.parse import quote
import requests

config = configparser.ConfigParser()
config.read('config.ini')


class Policy(object):
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

            r = requests.get(url=url, headers=headers)
            r.encoding = r.apparent_encoding
            status = r.status_code
            # 将原始数据类型转换为json类型，方便处理
            data_json = json.loads(r.text)
            print(status)
            return data_json['data']
        except:
            print("爬取失败")

    def exec(self, city_name):
        url = 'https://wx.wind.com.cn/alert/traffic/getPolicy?city=' + str(city_name)
        print(url)
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
        }
        data = self.get_html(url, headers)
        return data
