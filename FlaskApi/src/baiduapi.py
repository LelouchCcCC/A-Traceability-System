import datetime
import numpy as np
from pyhanlp import *
import pymysql
import pandas as pd
import pypinyin
import json
import re
from dateutil import parser
from sklearn.cluster import KMeans
import requests
import math
import configparser

config = configparser.ConfigParser()
config.read('./config.ini')
analyzer = PerceptronLexicalAnalyzer()


class Baid(object):
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

    def datatosql(self):
        data = pd.read_excel(r"D:\python-workspace\liudiao_msg.xls")
        data = data.fillna(0)
        df1 = data[(data['2密接 1阳性'].isin([0]))]
        df2 = data[(data['2密接 1阳性'].isin([2]))]
        conn = self.sql_connect()
        cursor = conn.cursor()
        for i in range(0, len(df1)):
            print(i)
            city = df1.loc[i][0]
            dat = df1.loc[i][2]
            date = str(dat.year) + '-' + str(dat.month) + '-' + str(dat.day)
            st = df1.loc[i][3]
            st = st.replace('：', ':')
            pattern_riqi = '([0-9]{2})'
            st = st.split('\n')
            acdate_flag = False
            acdate_flag = False
            for ii in st:  # 功能可以在具体时间上增加
                pattern_riqi = '([0-9]{1,2})月([0-9]{1,2})日'
                act_date = re.findall(pattern_riqi, ii)
                if len(act_date) > 0:
                    acdate_flag = True
                    #         print(act_date)
                    for k in act_date:
                        acd = '2022-' + str(k[0]) + '-' + str(k[1])
                        print(acd)
                        if type(ii) == list:
                            ii = ''.join(ii)
                        ii = re.split('，|,| ', ii)
                        for iii in ii:
                            act = []
                            #                 print(iii)
                            term_list = analyzer.analyze(iii)

                            for n, term in enumerate(term_list):
                                #                     print(term)
                                if re.search(r'/ns|/nt|/nsf|/ntc|/ntcb|/ntcf|/ntch|/nto|/nts|/ntu|/nz|/nf', str(term)):
                                    tg = ''
                                    k = 0
                                    fg = False
                                    for n, term2 in enumerate(term_list):
                                        if re.search(r'/n', str(term2)):
                                            for nn in re.findall('([^a-z"["/]*)/n', str(term2)):
                                                tg = tg + str(nn)
                                                tg = tg.replace(' ', '').replace(']', '')
                                            k = k + 1
                                        else:
                                            if k > 1:
                                                k = 0
                                                #                                     print(tg)
                                                fg = True
                                                act.append(tg)
                                                #                                     print('111')
                                                tg = ''
                                            else:
                                                k = 0
                                                tg = ''
                                    if tg != '':
                                        act.append(tg)
                                        tg = ''
                                    if fg == False:
                                        tgg = re.findall('([^a-z"["/]*)/n', str(term))
                                        #                             print(tgg)
                                        #                             print(222)
                                        #                             print(tg[0])
                                        for nn in tgg:
                                            tg = tg + str(nn)
                                            tg = tg.replace(' ', '').replace(']', '')
                                        act.append(tg)
                            formatlist = list(set(act))
                            if len(formatlist) > 0:
                                #                     print(formatlist)
                                for f in formatlist:
                                    #                             print(f)
                                    j, w = self.cha_baidu(f, city)
                                    tup = (i, city, date, acd, f, j, w)
                                    print(tup)
                                    sql = """insert into liudiao values{}""".format(tup)
                                    cursor.execute(sql)
                                    conn.commit()

                if acdate_flag == False:
                    act_date = date
                    acd = act_date
                    print(acd)
                    ii = re.split('，|,| ', ii)
                    for iii in ii:
                        act = []
                        #                 print(ii)
                        term_list = analyzer.analyze(iii)

                        for n, term in enumerate(term_list):
                            #                     print(term)
                            if re.search(r'/ns|/nt|/nsf|/ntc|/ntcb|/ntcf|/ntch|/nto|/nts|/ntu|/nz|/nf', str(term)):
                                tg = ''
                                k = 0
                                fg = False
                                for n, term2 in enumerate(term_list):
                                    if re.search(r'/n', str(term2)):
                                        for nn in re.findall('([^a-z"["/]*)/n', str(term2)):
                                            tg = tg + str(nn)
                                            tg = tg.replace(' ', '').replace(']', '')
                                        k = k + 1
                                    else:
                                        if k > 1:
                                            k = 0
                                            #                                     print(tg)
                                            fg = True
                                            act.append(tg)
                                            #                                     print('111')
                                            tg = ''
                                        else:
                                            k = 0
                                            tg = ''
                                if tg != '':
                                    act.append(tg)
                                    tg = ''
                                if fg == False:
                                    tgg = re.findall('([^a-z"["/]*)/n', str(term))
                                    #                             print(tgg)
                                    #                             print(222)
                                    #                             print(tg[0])
                                    for nn in tgg:
                                        tg = tg + str(nn)
                                        tg = tg.replace(' ', '').replace(']', '')
                                    act.append(tg)
                        formatlist = list(set(act))
                        if len(formatlist) > 0:
                            #                     print(formatlist)
                            for f in formatlist:
                                #                         print(f)
                                j, w = self.cha_baidu(f, city)
                                tup = (i, city, date, acd, f, j, w)
                                print(tup)
                                sql = """insert into liudiao values{}""".format(tup)
                                cursor.execute(sql)
                                conn.commit()
        cursor.close()
        conn.close()

    def tg_people(self, tg):
        conn = self.sql_connect()
        cursor = conn.cursor()
        city_name = []
        save = []
        for t in tg:
            city_name.append(t[0])
        for ci in city_name:
            # sql = """select * from liudiao where jing!=0 and city = '"""+ci+"""';"""
            sql = """select min(actdate) from new_liudiao where city = '""" + ci + """';"""
            print(sql)
            cursor.execute(sql)
            a = cursor.fetchall()
            print(a)
            save.append(a)
        lo = min(save)[0][0]
        to = max(save)[0][0]
        sql = """select * from new_liudiao where actdate<'""" + str(to) + """' and actdate>'""" + str(lo) + """';"""
        cursor.execute(sql)
        a = cursor.fetchall()
        aa = np.array(a)
        cursor.close()
        conn.close()
        tup = tuple(set(aa[:, 0]))
        sql = """select * from new_liudiao where n in{}""".format(tup)
        cursor.execute(sql)
        a = cursor.fetchall()

    # def judian(self,tg):                               #需要判断时间
    #     conn = self.sql_connect()
    #     cursor = conn.cursor()
    #     city_name = []
    #     for t in tg:
    #         city_name.append(t[0])
    #     for ci in city_name:
    #         sql = """select * from liudiao where jing!=0 and city = '"""+city_name+"""';"""
    #         a = cursor.fetchall()
    #
    #
    #     sql = """select city from liudiao where jing!=0 and """
    #     cursor.execute(sql)
    #     a = cursor.fetchall()
    #
    #     # print(sql)
    #     cursor.execute(sql)
    #     a = cursor.fetchall()
    #     k = list(set(a))
    #     kk = []
    #     for i in range(0, len(k)):
    #         if k[i][0].endswith('市'):
    #             kk.append(k[i][0])
    #         else:
    #             kk.append(k[i][0] + '市')
    #     kk = list(set(kk))

    def jingwei_sql(self):  # 城市经纬度查询
        conn = self.sql_connect()
        cursor = conn.cursor()
        sql = 'select distinct city from tovillage'
        cursor.execute(sql)
        a = cursor.fetchall()
        sql = 'select distinct country from tovillage'
        cursor.execute(sql)
        b = cursor.fetchall()
        m = a + b
        for n, i in enumerate(m):
            url = 'http://api.map.baidu.com/geocoder?ak=aYNu34AYwt3QTaApv4nNH5tSAxe7NIGe&output=json&address=' + str(
                i[0])
            header = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.50',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
            }
            try:
                r = requests.get(url, headers=header, timeout=30)
                js = r.text
                jj = json.loads(js)
                res = jj['result']
                lng = res['location']['lng']
                lat = res['location']['lat']
                tup = (str(i[0]), lng, lat)
                sql = """insert into city_jingwei values{}""".format(tup)
                cursor.execute(sql)
                conn.commit()
            except:
                print(str(n) + "坏掉了")

    def specify_act(self, filename):  # 需要判断格式问题
        """目前改成了解析模式"""
        df = pd.read_excel(filename)
        df = df.fillna(0)
        xxxx = []
        special_word = ['在', '到', '至', '返回', '从', '前往', '返回', '居住地', '旁边']
        conn = self.sql_connect()
        cursor = conn.cursor()
        sql = 'select max(n) from new_liudiao;'
        cursor.execute(sql)
        a = cursor.fetchone()
        start_nod = a[0] + 1

        # start_nod = 0

        for t in range(0, len(df)):
            city = str(df.loc[t][0])
            nod = t + start_nod
            dat = df.loc[t][2]
            try:
                date = str(dat.year) + '-' + str(dat.month) + '-' + str(dat.day)
            except AttributeError:
                date = str(dat)

            s = df.loc[t][3]
            datee = date
            s = s.replace('(', '')
            s = s.replace(')', '')
            s = s.split('\n')
            for sk in s:
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
                                try:
                                    dat = str(2022) + '-' + date[0][0] + '-' + date[0][1]
                                except:
                                    dat = datee
                                # jing, wei = self.cha_baidu(str(tg), str(city))
                                tup = (nod, city, datee, dat, str(tg))
                                xxxx.append(tup)
                                sql = """insert into zancun values{}""".format(tup)
                                cursor.execute(sql)
                                conn.commit()
                        if ff == True:
                            break

    def specify_act2(self, filename, base):  # 需要判断格式问题
        conn = self.sql_connect()
        cursor = conn.cursor()
        for i in base:
            tup = (i['no'], i['city'], i['date'], i['date'], i['act'])
            sql = """insert into zancun values{}""".format(tup)
            cursor.execute(sql)
            conn.commit()
        conn.close()
        return {'status': 'success'}

    def deal_sql(self):
        sql = """delete from new_liudiao where jing=0"""
        conn = self.sql_connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()

    def jiexi(self):
        conn = self.sql_connect()
        cursor = conn.cursor()
        sql = 'select * from zancun'
        cursor.execute(sql)
        p = cursor.fetchall()
        p = list(p)
        ll = []
        for i in p:
            l = list(i)
            i2 = str(i[2].year) + '-' + str(i[2].month) + '-' + str(i[2].day)
            l[2] = i2
            i3 = str(i[3].year) + '-' + str(i[3].month) + '-' + str(i[3].day)
            l[3] = i3
            ll.append(l)
        return ll


class suyuan(object):
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

    def sql_get_city(self):
        conn = self.sql_connect()
        cursor = conn.cursor()

        sql = """select city from new_liudiao where jing!=0"""
        cursor.execute(sql)
        a = cursor.fetchall()
        today = datetime.datetime.today()
        today = datetime.datetime.strptime("2022-2-25", "%Y-%m-%d")  # 后面需要删掉的时间
        # print(sql)
        cursor.execute(sql)
        a = cursor.fetchall()
        k = list(set(a))

        """数据库中地区最近的确诊日期"""
        tg = []
        pp = []
        for i in k:
            sql = "select max(date) from new_liudiao where city ='" + str(i[0]) + "';"
            cursor.execute(sql)
            a = cursor.fetchone()
            a1 = parser.parse(str(a[0]))
            pp = [str(i[0]), a1]
            if (today - a1).days <= 7:
                tg.append(pp)
        cursor.close()
        conn.close()
        return tg

    def judd(self, tg):
        conn = self.sql_connect()
        cursor = conn.cursor()
        city_name = []
        save_lo = []
        save_hi = []
        fan = []
        tg_n = []
        for t in tg:
            city_name.append(t[0])
        min_date = []
        for ci in city_name:
            sql = """select min(actdate) from new_liudiao where city = '""" + ci + """';"""  # z这三个的时间判断需要！！！
            # print(sql)
            cursor.execute(sql)
            a = cursor.fetchall()
            min_date.append(a[0][0])
            save_lo.append(a)
            sql = """select max(actdate) from new_liudiao where city = '""" + ci + """';"""
            cursor.execute(sql)
            a = cursor.fetchall()
            save_hi.append(a)
            sql = """select distinct n from new_liudiao where city = '""" + ci + """';"""
            cursor.execute(sql)
            a = cursor.fetchall()
            tg_n.append(a)
        cursor.close()
        conn.close()
        lo = min(save_lo)[0][0]
        to = max(save_hi)[0][0]
        sql = """select * from new_liudiao where actdate<='""" + str(to) + """' and actdate>='""" + str(
            lo) + """';"""  # 在这个期间内的活动的全部，或许可以不要max值
        conn = self.sql_connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        a = cursor.fetchall()
        aa = np.array(a)
        m = tuple(set(aa[:, 0]))
        sql = """select * from new_liudiao where n in{}""".format(m)
        cursor.execute(sql)
        a = cursor.fetchall()
        df = pd.DataFrame(list(a))
        df_list = df.index.tolist()
        df_arr = np.array(df_list)
        df['no'] = df_arr
        prob_city_jingwei = []
        xx = df[5]
        yy = df[6]
        su = df[1].value_counts()
        length = len(su.keys())  # 在所选择时间区间内有病例活动的城市数量，su.keys()即为城市名称list
        for h in su.keys():
            sql = """select * from city_jingwei where city='""" + str(h) + """'"""
            cursor.execute(sql)
            b = cursor.fetchall()
            prob_city_jingwei.append(b)
        #         print(prob_city_jingwei)
        tot = []
        for i in range(0, len(xx)):
            tot.append([xx[i], yy[i]])
        #     len(tot)               #在这个时间区间内的行为数，及经纬
        centers, labels, mm = self.judian(length, tot)
        #         for un in df[0].unique():

        #             dd = df[df[0]==un]
        #             noo = dd['no'].unique()
        #             lab = []
        #             for i in noo:
        #                 lab.append(labels[i])
        #             labst = set(lab)
        #             if len(labst)>1:
        #                 print(un,end=":")           #un为有外出行为的人的编号
        # #                 print(dd)           #dd为有外出经历的人的行动
        #                 print(lab)
        ut_to = []  # 所有城市的ut
        fi_ut = []
        for n, un in enumerate(tg_n):
            first_date = min_date[n]
            #             print(first_date)
            #             print(type(first_date))
            ut = []  # 单个城市有外出经历且与别地方的人有交互的list
            utit = []
            for nnn in un:
                first_flag = False
                dd = df[df[0] == nnn[0]]
                #                 print(min(dd[2]),end="|")
                #                 print(first_date)
                #                 print(type(min(dd[2])))
                if (first_date + datetime.timedelta(days=5)) > min(dd[2]):
                    first_flag = True
                #                 print(first_flag)
                noo = dd['no'].unique()
                lab = []
                for i in noo:
                    lab.append(labels[i])
                labst = set(lab)
                if len(labst) > 1:
                    # print(tg[n][0], end="  ")
                    # print(nnn[0], end=":")  # un为有外出行为的人的编号
                    #                 print(dd)           #dd为有外出经历的人的行动
                    #                     print(lab)

                    # for lb in lab:
                    #     print(mm[lb][1], end="、")
                    # print()
                    sql = """select jing,wei from city_jingwei where city = '""" + tg[n][0] + """'"""
                    cursor.execute(sql)
                    a = cursor.fetchall()
                    lp = []
                    #                     print(a)
                    xxx = dd[5].values
                    yyy = dd[6].values
                    for dk in range(0, len(dd[5])):
                        lp.append([xxx[dk], yyy[dk]])
                    p1 = np.array([a[0][0], a[0][1]])
                    for nu, fk in enumerate(lp):
                        strr = ''
                        fr = ''
                        p2 = np.array([fk[0], fk[1]])
                        p3 = p2 - p1
                        p4 = math.hypot(p3[0], p3[1])
                        if p4 > 2:

                            '''下面需要判断有外市旅行史的人的外地地点是不是在疫情点'''
                            #                             pb = []
                            #                             for pn,prob in enumerate(prob_city_jingwei):
                            #                                 p5 = np.array([prob[0][1],prob[0][2]])
                            # #                                 print(p5)
                            #                                 p6 = p5 - p2
                            #                                 p7 = math.hypot(p6[0],p6[1])
                            #                                 pb.append(p7)
                            #                             print(pb.index(min(pb)),end=':')
                            #                             print(min(pb))
                            #                             print(pb)
                            di = df[df[1] != tg[n][0]]
                            di = di.reset_index(drop=True)
                            xl = di[5]
                            yl = di[6]
                            totl = []
                            pcc = []
                            for il in range(0, len(xl)):
                                try:
                                    totl.append([xl[il], yl[il]])
                                except:
                                    pass
                            for l in totl:
                                pl = np.array(l)
                                px = p2 - pl
                                pc = math.hypot(px[0], px[1])
                                pcc.append(pc)
                            if min(pcc) < 0.5:
                                if first_flag == True:
                                    # print(min(dd[2]), end="|")
                                    # print(first_date)
                                    strr = str(di.loc[pcc.index(min(pcc))][1])
                                    utit.append(strr)
                                else:
                                    #                                 print(di.loc[pcc.index(min(pcc))][1])
                                    #                                 print(di.loc[])
                                    strr = str(di.loc[pcc.index(min(pcc))][1])
                                    #                                 print(pcc.index(min(pcc)),end=':')

                                    ut.append(strr)
                                    # print(min(dd[2]), end="|")
                                    # print(first_date)
                            else:
                                #                                 ut.append(strr)
                                # print(min(dd[2]), end="|")
                                # print(first_date)
                                pass
            ut_to.append([tg[n][0], ut])
            fi_ut.append([tg[n][0], utit])

        cursor.close()
        conn.close()
        return ut_to, fi_ut,

    def judd_one(self, tg, ta):
        conn = self.sql_connect()
        cursor = conn.cursor()
        if ta == 'bayanzhuoershi':
            ta = 'bayannaoershi'
        val = ''
        mk = {}
        for t in tg:
            mk[t[0]] = self.pinyin(t[0])
        for k, v in mk.items():
            if v == ta:
                val = k
        city_name = []
        save_lo = []
        add_ci = []
        save_hi = []
        fan = []
        tg_n = []
        min_date = []
        ci = val
        # sql = """select * from liudiao where jing!=0 and city = '"""+ci+"""';"""
        sql = """select min(actdate) from new_liudiao where city = '""" + ci + """';"""  # z这三个的时间判断需要！！！
        # print(sql)
        cursor.execute(sql)
        a = cursor.fetchall()
        min_date.append(a[0][0])
        save_lo.append(a)
        sql = """select max(actdate) from new_liudiao where city = '""" + ci + """';"""
        cursor.execute(sql)
        a = cursor.fetchall()
        save_hi.append(a)
        sql = """select distinct n from new_liudiao where city = '""" + ci + """';"""
        cursor.execute(sql)
        a = cursor.fetchall()
        tg_n.append(a)
        cursor.close()
        conn.close()
        lo = min(save_lo)[0][0]
        to = max(save_hi)[0][0]
        sql = """select * from new_liudiao where actdate<='""" + str(to) + """' and actdate>='""" + str(
            lo) + """';"""  # 在这个期间内的活动的全部，或许可以不要max值
        conn = self.sql_connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        a = cursor.fetchall()
        aa = np.array(a)
        m = tuple(set(aa[:, 0]))
        sql = """select * from new_liudiao where n in{}""".format(m)
        cursor.execute(sql)
        a = cursor.fetchall()
        df = pd.DataFrame(list(a))
        df_list = df.index.tolist()
        df_arr = np.array(df_list)
        df['no'] = df_arr
        prob_city_jingwei = []
        xx = df[5]
        yy = df[6]
        su = df[1].value_counts()
        length = len(su.keys())  # 在所选择时间区间内有病例活动的城市数量，su.keys()即为城市名称list
        for h in su.keys():
            sql = """select * from city_jingwei where city='""" + str(h) + """'"""
            cursor.execute(sql)
            b = cursor.fetchall()
            prob_city_jingwei.append(b)
        tot = []
        for i in range(0, len(xx)):
            tot.append([xx[i], yy[i]])
        #     len(tot)               #在这个时间区间内的行为数，及经纬
        centers, labels, mm = self.judian(length, tot)
        for n, un in enumerate(tg_n):
            first_date = min_date[n]
            for nnn in un:
                first_flag = False
                dd = df[df[0] == nnn[0]]
                noo = dd['no'].unique()
                lab = []
                for i in noo:
                    lab.append(labels[i])
                labst = set(lab)
                if len(labst) > 1:
                    add_ci.append(nnn[0])
        m = tuple(add_ci)
        if len(m) == 0:
            return []
        if len(m) == 1:
            m = m[0]
            sql = 'select * from new_liudiao where n = ' + str(m) + ';'
        else:
            sql = 'select * from new_liudiao where n in {}'.format(m)
        cursor.execute(sql)
        a = cursor.fetchall()
        ms = []
        for i in a:
            drt = []
            drt.append(i[0])
            drt.append(str(i[2].year) + '-' + str(i[2].month) + '-' + str(i[2].day))
            drt.append(str(i[3].year) + '-' + str(i[3].month) + '-' + str(i[3].day))
            drt.append(i[4])
            ms.append(drt)
        save_n = [-1]
        xp = []
        xpp = []
        for i in ms:
            if save_n[-1] != i[0]:
                xp.append(xpp)
                xpp = []
                save_n.append(i[0])
            xpp.append(i)
        xp.append(xpp)
        xp.pop(0)
        cursor.close()
        conn.close()
        return xp

    def judian(self, length, tot):  # length为聚点数,tot为行为的经纬二维数组
        tot_arr = np.array(tot)
        clf = KMeans(n_clusters=length)
        clf.fit(tot_arr)
        centers = clf.cluster_centers_  # 两组数据点的中心点
        labels = clf.labels_  # 每个数据点所属分组
        #     print(centers)
        #     print(labels)
        ci = self.judian_city()
        mm = []
        ci = list(ci)  # 城市名称及经纬度
        for nn, c in enumerate(centers):
            p1 = np.array([c[0], c[1]])
            # print(c)
            ap = []
            for ty in ci:
                p2 = np.array([ty[1], ty[2]])
                p3 = p2 - p1
                p4 = math.hypot(p3[0], p3[1])
                if p4 < 10:
                    ap.append([p4, ty[0]])
            #             for pp in ap:
            #                 print(pp)
            lll = np.array(ap)
            mi = lll[np.lexsort(lll[:, ::-1].T)][0]
            mm.append(mi)  # 离最低限度聚点最近的点
        return centers, labels, mm

    def judian_city(self):
        conn = self.sql_connect()
        cursor = conn.cursor()
        sql = 'select * from city_jingwei'
        cursor.execute(sql)
        a = cursor.fetchall()
        cursor.close()
        conn.close()
        return a

    def displ(self, tg):
        conn = self.sql_connect()
        cursor = conn.cursor()
        city_name = []
        save_lo = []
        save_hi = []
        fan = []
        tg_n = []
        for t in tg:
            city_name.append(t[0])
        min_date = []
        for ci in city_name:
            # sql = """select * from liudiao where jing!=0 and city = '"""+ci+"""';"""
            sql = """select min(actdate) from new_liudiao where city = '""" + ci + """';"""  # z这三个的时间判断需要！！！
            # print(sql)
            cursor.execute(sql)
            a = cursor.fetchall()
            min_date.append(a[0][0])
            save_lo.append(a)
            sql = """select max(actdate) from new_liudiao where city = '""" + ci + """';"""
            cursor.execute(sql)
            a = cursor.fetchall()
            save_hi.append(a)
            sql = """select distinct n from new_liudiao where city = '""" + ci + """';"""
            cursor.execute(sql)
            a = cursor.fetchall()
            tg_n.append(a)
        cursor.close()
        conn.close()
        lo = min(save_lo)[0][0]
        to = max(save_hi)[0][0]
        sql = """select * from new_liudiao where actdate<'""" + str(to) + """' and actdate>'""" + str(
            lo) + """';"""  # 在这个期间内的活动的全部，或许可以不要max值
        conn = self.sql_connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        a = cursor.fetchall()
        aa = np.array(a)
        m = tuple(set(aa[:, 0]))
        sql = """select * from new_liudiao where n in{}""".format(m)
        cursor.execute(sql)
        a = cursor.fetchall()
        cursor.close()
        conn.close()
        df = pd.DataFrame(list(a))
        df_list = df.index.tolist()
        df_arr = np.array(df_list)
        df['no'] = df_arr
        prob_city_jingwei = []
        at = df[4]
        xx = df[5]
        yy = df[6]
        data = []
        geo = {}
        past = []
        for (index, pos) in enumerate(at):
            if pos not in past:
                p = {}
                p['name'] = pos
                p['value'] = 1
                past.append(pos)
                data.append(p)
                geo[pos] = [xx[index], yy[index]]
            else:
                for i in data:
                    if i['name'] == pos:
                        i['value'] = i['value'] + 1
                        break
                    else:
                        pass

        return data, geo

    def pinyin(self, word):
        s = ''
        for py in pypinyin.pinyin(word, style=pypinyin.NORMAL):
            s += ''.join(py)
        return s

    def city_one(self, tg, cina):
        if cina == 'bayanzhuoershi':
            cina = 'bayannaoershi'
        val = ''
        mk = {}
        for t in tg:
            mk[t[0]] = self.pinyin(t[0])
        for k, v in mk.items():
            if v == cina:
                val = k
        conn = self.sql_connect()
        cursor = conn.cursor()
        city_name = []
        save_lo = []
        save_hi = []
        fan = []
        tg_n = []
        for t in tg:
            city_name.append(t[0])
        min_date = []
        for ci in city_name:
            # sql = """select * from liudiao where jing!=0 and city = '"""+ci+"""';"""
            sql = """select min(actdate) from new_liudiao where city = '""" + ci + """';"""  # z这三个的时间判断需要！！！
            # print(sql)
            cursor.execute(sql)
            a = cursor.fetchall()
            min_date.append(a[0][0])
            save_lo.append(a)
            sql = """select max(actdate) from new_liudiao where city = '""" + ci + """';"""
            cursor.execute(sql)
            a = cursor.fetchall()
            save_hi.append(a)
            sql = """select distinct n from new_liudiao where city = '""" + ci + """';"""
            cursor.execute(sql)
            a = cursor.fetchall()
            tg_n.append(a)
        lo = min(save_lo)[0][0]
        to = max(save_hi)[0][0]
        sql = """select * from new_liudiao where actdate<'""" + str(to) + """' and actdate>'""" + str(
            lo) + """' and city='""" + val + """';"""  # 在这个期间内的活动的全部，或许可以不要max值
        cursor.execute(sql)
        a = cursor.fetchall()
        aa = np.array(a)
        m = tuple(set(aa[:, 0]))
        if len(m) == 1:
            m = str(m).replace(',', '')
        sql = """select * from new_liudiao where n in{}""".format(m)
        cursor.execute(sql)
        a = cursor.fetchall()
        cursor.close()
        conn.close()
        df = pd.DataFrame(list(a))
        df_list = df.index.tolist()
        df_arr = np.array(df_list)
        df['no'] = df_arr
        prob_city_jingwei = []
        at = df[4]
        xx = df[5]
        yy = df[6]
        data = []
        geo = {}
        past = []
        for (index, pos) in enumerate(at):
            if pos not in past:
                p = {}
                p['name'] = pos
                p['value'] = 1
                past.append(pos)
                data.append(p)
                geo[pos] = [xx[index], yy[index]]
            else:
                for i in data:
                    if i['name'] == pos:
                        i['value'] = i['value'] + 1
                        break
                    else:
                        pass

        return data, geo, val

    # 虚假的城市数字
    def cont(self, target):
        conn = self.sql_connect()
        cursor = conn.cursor()
        dic = {}
        for i in target:
            city = i[0]
            sql = """select distinct n from new_liudiao where city = '"""+str(city)+"""';"""
            cursor.execute(sql)
            a = cursor.fetchall()
            dic[city] = len(a)
        return dic


    # def specify_act(self,filename):         #需要判断格式问题
    #     """目前改成了解析模式"""
    #     df = pd.read_excel(filename)
    #     df = df.fillna(0)
    #     xxxx=[]
    #     special_word = ['在','到','至','返回','从','前往','返回','居住地','旁边']
    #     conn = self.sql_connect()
    #     cursor = conn.cursor()
    #     sql = 'select max(n) from zancun;'
    #     cursor.execute(sql)
    #     a = cursor.fetchone()
    #     start_nod = a[0]+1
    #
    #     # start_nod = 0
    #
    #     for t in range(0, len(df)):
    #         city = str(df.loc[t][0])
    #         nod = t+start_nod
    #         dat = df.loc[t][2]
    #         date = str(dat.year) + '-' + str(dat.month) + '-' + str(dat.day)
    #         s = df.loc[t][3]
    #         datee = date
    #         s = s.replace('(', '')
    #         s = s.replace(')', '')
    #         s = s.split('\n')
    #         for sk in s:
    #             pattern_riqi = '([0-9]{1,2})月([0-9]{1,2})日'
    #             sk = re.split('，|；|。|？|！', sk)
    #             for sksk in sk:
    #                 act_date = re.findall(pattern_riqi, sksk)
    #
    #                 if len(act_date) > 0:
    #                     date = act_date
    #                 else:
    #                     date = date
    #                 for i in special_word:
    #                     ff = False
    #                     if i in sksk:
    #                         ff = True
    #                         new_s = re.findall(str(i) + '(.*)', sksk)
    #                         new_s = ''.join(new_s)
    #                         #                 print(new_s)
    #                         term_list = analyzer.analyze(new_s)
    #                         tg = ''
    #                         for n, term in enumerate(term_list):
    #                             if n == 0:
    #                                 if '[' in term.toString():
    #                                     flag = False
    #                                 else:
    #                                     flag = True
    #                                 tg = ''.join(re.findall('[^\x00-\xff]', term.toString()))
    #                             #                         print(tg)
    #
    #                             elif re.search(r'/n|/ns|/nt|/nsf|/ntc|/ntcb|/ntcf|/ntch|/nto|/nts|/ntu|/nz|/nf',
    #                                            str(term)):
    #                                 ss = re.findall('[^\x00-\xff]', term.toString())
    #                                 #                         print(ss)
    #                                 flag = False
    #                                 ss = ''.join(ss)
    #                                 tg = tg + ss
    #                             else:
    #                                 break
    #                         if flag == False:
    #                             try:
    #                                 dat = str(2022) + '-' + date[0][0] + '-' + date[0][1]
    #                             except:
    #                                 dat = datee
    #                             jing, wei = self.cha_baidu(str(tg), str(city))
    #                             tup = (nod, city, datee, dat, str(tg), jing, wei)
    #                             xxxx.append(tup)
    #                             sql = """insert into zancun values{}""".format(tup)
    #                             cursor.execute(sql)
    #                             conn.commit()
    #                     if ff == True:
    #                         break
