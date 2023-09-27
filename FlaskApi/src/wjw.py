import re
import requests
import html
import xlwt
import pandas as pd
import datetime
from bs4 import BeautifulSoup
import time
from lxml import etree
import dns.resolver
from pyhanlp import *
import pymysql
class Pachong(object):
    def gov_wjw(self):
        analyzer = PerceptronLexicalAnalyzer()
        url="http://www.gov.cn/fuwu/zt/yqfwzq/zxqk.htm"  #疫情防控动态html
        #try:
        header = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.50',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
                }
        r = requests.get(url, headers=header, timeout=30)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'lxml')
        x = soup.find_all(id='tab-1')
        a = x[0].find_all('a')
        url_fy = []
        year=[2022,2021,2020]
        conn = self.sql_connect()
        cursor = conn.cursor()
        choice = 0
        cot = 0
        for i in a:
            # print(i.text)
            pattern = '肺炎疫情最新情况'
            #print(choice)
            if pattern in i.text:
                cot=cot+1
                href = 'http://www.gov.cn'+i['href']
                #print(i['href'])
                #print(i.text)
                term_list = analyzer.analyze(i.text)
                #print((term_list))
                date=[]
                for term in term_list:
                    if re.search(r'/t', str(term)):
                        # print(str(term))
                        date.append(str(term))
                date=''.join(date)
                mon = re.findall('[^0-9]*([0-9]*)月', date)
                day = re.findall('[^0-9]*([0-9]*)日', date)
                if int(mon[0]) == 12 and int(day[0]) == 31:
                    choice=choice +1
                d=str(year[choice])+'-'+str(mon[0])+'-'+str(day[0])
                nn=str(1)
                sql = "insert into dateurl (date,url) values ('"+d+"', '"+href+"');"
                print(sql)
                #try:
                        # 执行sql语句
                cursor.execute(sql)
                        # 提交到数据库执行
                conn.commit()
                    #except:
                        # Rollback in case there is any error
                        #conn.rollback()

                self.gov_con(d,href)
                time.sleep(2)
                if cot == 20:
                    break
                # continue
        conn.close()
       # except:
            #return 1

    def sql_connect(self):
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='20010308',
            database='yiqing',
            charset='utf8',
            # autocommit=True,    # 如果插入数据，， 是否自动提交? 和conn.commit()功能一致。
        )
        return conn


    def gov_con(self,date,url):
        analyzer = PerceptronLexicalAnalyzer()
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.55',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        }
        r = requests.get(url, headers=header, timeout=30)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'lxml')
        x = soup.find(class_='pages_content')
        key_word = ['境外输入', '本土', '疑似病例']
        conn = self.sql_connect()
        cursor = conn.cursor()
        # print(x)
        for i in x:
            # print(i.string)
            strr = i.string
            flag_wzz = False
            if '新增无症状' in strr:
                flag_wzz = True
                wzz = 'wzz'
            for n, i in enumerate(key_word):
                if (flag_wzz == True) and (n == 0):
                    continue
                else:
                    data_jingwai = -1
                    data_bentu = -1
                    data_yisi = -1
                    try:
                        pattern = i + '[^（]*（([^）]*)）'
                        rs = re.search(pattern, strr).group(1)
                        tem = 0
                        if len(rs) > 0:
                            if flag_wzz == True:
                                wzz = 'wzz'
                            else:
                                wzz = ''
                            #             print(rs)
                            if n == 0:
                                database_name = 'jingwai'

                            elif n == 1:
                                database_name = wzz + 'bentu'
                            elif n == 2:
                                database_name = 'yisi'
                            print(database_name)
                            rs = re.split('，|；|、', rs)
                            for x in rs:
                                #                 print(x)

                                #             print(rs)
                                term_list = analyzer.analyze(x)
                                #                 print(term_list)

                                if re.search(r'/ns', str(term_list)):
                                    litp = []
                                    for term in term_list:  # 疑似病例的判断有点问题
                                        ns = re.findall('([^/]*)/ns', str(term))
                                        m = re.findall('([0-9]*)[^/]*/m', str(term))
                                        if len(ns) > 0:
                                            ss = ns[0]
                                        if len(m) > 0:
                                            ms = m[0]
                                    #                     print(ss)
                                    #                     print(ms)
                                    litp.append(date)
                                    litp.append(ss)
                                    litp.append(ms)
                                    tup = tuple(litp)
                                    # print(tup)
                                    sql = """insert into """ + database_name + """ values{}""".format(tup)
                                    print(sql)
                                    cursor.execute(sql)
                                    conn.commit()

                    except AttributeError:
                        if n == 0:
                            data_jingwai = 0
                        elif n == 1:
                            data_bentu = 0
                        elif n == 2:
                            data_yisi = 0



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
                print(k)
                print(k[0])
                kw = str(month) + '月' + str(day) + '日' + k[0] + '疫情流调信息'
                print(kw)
        cursor.close()
        conn.close()

    def Edge(self, kw, las):
        url = 'https://cn.bing.com/search?q='+str(kw)+str(las)
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.55',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        }
        response = requests.get(url, headers=header, timeout=30)
        pattern = '[病例][0-9]*([^病例]*)'
        try:
            html = response.text.encode("latin1").decode("utf-8")
            print()
        except UnicodeEncodeError:
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            # print(soup.text)
        except UnicodeDecodeError:
            html = response.text.encode("latin1").decode("gbk")
            soup = BeautifulSoup(html, 'lxml')
            # print(soup.text)
        else:
            soup = BeautifulSoup(html, 'lxml')
            # print(soup.text)
        need = re.findall(pattern,soup.text.replace('\n', ' ').replace('\r', ' ').replace('\xa0', ' ').replace('\u2002',' ').replace('\u3000', ' ').replace('\u200b', ' '))
        print(need)

        # print(soup.text)
