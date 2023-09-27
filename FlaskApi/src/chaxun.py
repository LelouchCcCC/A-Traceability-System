import json
import datetime
import math
import pandas as pd
import numpy as np
import pymysql
import re
from pyhanlp import *
import requests
import configparser

config = configparser.ConfigParser()
config.read('./config.ini')

analyzer = PerceptronLexicalAnalyzer()


class query(object):
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

    def cuti(self, txt, city):
        txt = txt.replace('\u3000', '')
        special_word = ['在', '到', '至', '返回', '从', '前往', '返回', '居住地', '旁边']
        date = '?!?!'
        lst = []
        count = 0
        txt = txt.replace('(', '')
        txt = txt.replace(')', '')
        txt = txt.split('\n')
        for sk in txt:
            pattern_riqi = '([0-9]{1,2})月([0-9]{1,2})日'
            sk = re.split('，|；|。|？|！', sk)
            for sksk in sk:
                act_date = re.findall(pattern_riqi, sksk)
                if len(act_date) > 0:
                    date = act_date
                else:
                    date = date
                for i in special_word:
                    ff = False
                    if i in sksk:
                        ff = True
                        new_s = re.findall(str(i) + '(.*)', sksk)
                        new_s = ''.join(new_s)
                        #                 print(new_s)
                        term_list = analyzer.analyze(new_s)
                        tg = ''
                        for n, term in enumerate(term_list):
                            if n == 0:
                                if '[' in term.toString():
                                    flag = False
                                else:
                                    flag = True
                                tg = ''.join(re.findall('[^\x00-\xff]', term.toString()))
                            #                         print(tg)
                            elif re.search(r'/n|/ns|/nt|/nsf|/ntc|/ntcb|/ntcf|/ntch|/nto|/nts|/ntu|/nz|/nf',
                                           str(term)):
                                ss = re.findall('[^\x00-\xff]', term.toString())
                                #                         print(ss)
                                flag = False
                                ss = ''.join(ss)
                                tg = tg + ss
                            else:
                                break
                        if flag == False:
                            dat = str(2022) + '-' + date[0][0] + '-' + date[0][1]
                            tup = (city, dat, str(tg))
                            targ_dic = {}
                            targ_dic['date'] = dat
                            targ_dic['action'] = str(tg)
                            lst.append(targ_dic)
                            count += 1
                    if ff == True:
                        break
        return lst

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

    def panduan(self, data, city):
        conn = self.sql_connect()
        cursor = conn.cursor()
        fir = []
        fir2 = []
        sec = []
        sec2 = []
        try:
            for i in data:
                ii = json.loads(i)
                ac = ii['action']
                tim = ii['date']
                tim = datetime.datetime.strptime(tim, "%Y-%m-%d")
                tim_h = tim + datetime.timedelta(days=0)
                tim_l = tim - datetime.timedelta(days=3)
                dh = str(tim_h.year) + '-' + str(tim_h.month) + '-' + str(tim_h.day)
                dl = str(tim_l.year) + '-' + str(tim_l.month) + '-' + str(tim_l.day)
                sql = 'select * from new_liudiao where actdate <="' + str(dh) + '" and actdate>="' + str(dl) + '";'
                jing, wei = self.cha_baidu(ac, city)
                if jing == 0:
                    continue
                p1 = np.array([jing, wei])
                cursor.execute(sql)
                fir_n = []
                fir2_n = {}
                sec_n = []
                nearby = []
                sec2_n = {}
                result = {}
                a_tim = cursor.fetchall()
                for n, val in enumerate(a_tim):
                    x = val[5]
                    y = val[6]
                    pp1 = np.array([x, y])
                    pp0 = pp1 - p1
                    ppp = math.hypot(pp0[0], pp0[1])
                    if ppp < 0.0001:
                        fir_n.append(val[0])
                        fir2_n['date'] = val[2]
                        fir2_n['place'] = ac


                        nearby.append(val[4])

                result['nearby']=nearby
                fir2_n['result'] = result
                sql = 'select * from new_liudiao where act = "' + ac + '";'
                cursor.execute(sql)
                a_ac = cursor.fetchall()
                pb = {}
                nearby = []
                result = {}
                if len(a_ac) > 0:
                    for j in a_ac:
                        p2 = np.array([j[5], j[6]])
                        p3 = p2 - p1
                        p4 = math.hypot(p3[0], p3[1])
                        if p4 < 0.0001:
                            sec_n.append(j[0])
                            sec2_n['date'] = j[2]
                            sec2_n['place'] = ac
                            nearby.append(j[4])
                result['nearby'] = nearby
                sec2_n['result'] = result
                fir.append(fir_n)
                sec.append(sec_n)
                fir2.append(fir2_n)
                sec2.append(sec2_n)
        except:
            fir.append([])
            sec.append([])
            fir2.append([])
            sec2.append([])
        cursor.close()
        conn.close()
        return fir, sec, fir2, sec2

    #     下面是新项目的判断
    def new_judge_panduan(self, data):
        conn = self.sql_connect()
        cursor = conn.cursor()
        fir = []
        fir2 = []
        sec = []
        sec2 = []
        # try:
        for i in data:
            ac = i['place']
            jw = i['source']['location']
            p = jw.split(',')
            jing = float(p[0])
            wei = float(p[1])
            date = i['date']
            tim = datetime.datetime.strptime(date, "%Y-%m-%d")
            tim_h = tim + datetime.timedelta(days=0)
            tim_l = tim - datetime.timedelta(days=3)
            dh = str(tim_h.year) + '-' + str(tim_h.month) + '-' + str(tim_h.day)
            dl = str(tim_l.year) + '-' + str(tim_l.month) + '-' + str(tim_l.day)
            sql = 'select * from new_liudiao where actdate <="' + str(dh) + '" and actdate>="' + str(dl) + '";'
            p1 = np.array([jing, wei])
            cursor.execute(sql)
            fir_n = []
            fir2_n = {}
            sec_n = []
            nearby = []
            sec2_n = {}
            result = {}
            a_tim = cursor.fetchall()
            for n, val in enumerate(a_tim):
                x = val[5]
                y = val[6]
                pp1 = np.array([x, y])
                pp0 = pp1 - p1
                ppp = math.hypot(pp0[0], pp0[1])
                if ppp < 0.01:
                    fir_n.append(val[0])
                    fir2_n['date'] = val[2]
                    fir2_n['place'] = ac
                    print('val[4]:', val[4])
                    nearby.append(val[4])

            result['nearby'] = nearby
            result['date'] = date
            result['place'] = ac
            fir2_n['result'] = result
            sql = 'select * from new_liudiao where act = "' + ac + '";'
            cursor.execute(sql)
            a_ac = cursor.fetchall()
            pb = {}
            nearby = []
            result = {}
            if len(a_ac) > 0:
                for j in a_ac:
                    p2 = np.array([j[5], j[6]])
                    p3 = p2 - p1
                    p4 = math.hypot(p3[0], p3[1])
                    if p4 < 0.01:
                        sec_n.append(j[0])
                        sec2_n['date'] = j[2]
                        sec2_n['place'] = ac
                        nearby.append(j[4])
            result['date'] = date
            result['place'] = ac
            result['nearby'] = nearby
            sec2_n['result'] = result
            fir.append(fir_n)
            sec.append(sec_n)
            fir2.append(fir2_n)
            sec2.append(sec2_n)
        # except:
        #     fir.append([])
        #     sec.append([])
        #     fir2.append([])
        #     sec2.append([])
        cursor.close()
        conn.close()
        return fir, sec, fir2, sec2





    def new_judge(self, date, cont):
        conn = self.sql_connect()
        cursor = conn.cursor()
        pattern = '([^T]*)T'
        tim = datetime.datetime.strptime(date, "%Y-%m-%d")
        p = str(tim.date())
        sql = 'select no from transport where date = "' + p + '" and item = "' + cont + '";'
        cursor.execute(sql)
        print(sql)
        a = cursor.fetchall()
        print(a)
        cursor.close()
        conn.close()
        return a
