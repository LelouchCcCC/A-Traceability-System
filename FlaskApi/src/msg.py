import re
import requests
import pymysql
from bs4 import BeautifulSoup
import time
from pyhanlp import *
import configparser

config = configparser.ConfigParser()
config.read('./config.ini')

class sj(object):

    def sql_get(self,date):
        time_tuple = time.strptime(date, '%Y-%m-%d')
        year, month, day = time_tuple[:3]
        conn = self.sql_connect()
        cursor = conn.cursor()
        database_name = ['bentu', 'jingwai', 'yisi', 'wzzbentu']
        for n, i in enumerate(database_name):
            sql = """select procity, num from """ + i + """ where date = '""" + str(date) + """';"""
            print(sql)
            cursor.execute(sql)
            a = cursor.fetchall()
            for k in a:
                # print(k)
                # print(k[0])
                kw = str(month) + '月' + str(day) + '日' + k[0] + '疫情流调信息'
                for pg in range(0, 1):
                    page = pg*10+1
                    self.pc('https://cn.bing.com/search?q='+str(kw)+'&filters=ex1%3a"ez3"'+'&first='+str(page))
        cursor.close()
        conn.close()


    def pc(self,url):
        conn = self.sql_connect()
        cursor = conn.cursor()
        analyzer = PerceptronLexicalAnalyzer()
        # try:
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.50',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        }
        r = requests.get(url, headers=header, timeout=30)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'lxml')
        x = soup.find_all(class_='b_algo')
        href = []
        for i in x:
            a = i.find_all('a')
            # print(a)
            for h in a:
                href.append(h['href'])
                print(h['href'])
                self.detailed_html(h['href'])
                break
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

    def detailed_html(self, url):
        try:
            header = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.50',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
            }
            response = requests.get(url, headers=header, timeout=30)
            pattern = '[病例][0-9]*([^病例]*)'
            try:
                html = response.text.encode("latin1").decode("utf-8")
                soup = BeautifulSoup(html, 'lxml')
                print()
            except UnicodeEncodeError:
                html = response.text
                soup = BeautifulSoup(html, 'lxml')
                # print(soup.text)
            except UnicodeDecodeError:
                try:
                    html = response.text.encode("latin1").decode("gbk")
                    soup = BeautifulSoup(html, 'lxml')
                except:
                    pass
                # print(soup.text)

                # soup = BeautifulSoup(html, 'lxml')
            #     # print(soup.text)
            need = re.findall(pattern,soup.text.replace('\n', ' ').replace('\r', ' ').replace('\xa0', ' ').replace('\u2002',' ').replace('\u3000', ' ').replace('\u200b', ' '))
            print(need)
        except:
            pass