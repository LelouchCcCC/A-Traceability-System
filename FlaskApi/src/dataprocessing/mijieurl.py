import datetime
import os
import time
from pyhanlp import *
import requests
import xlwt
from bs4 import BeautifulSoup
import unicodedata
import urllib
import re
from lxml import etree

analyzer = PerceptronLexicalAnalyzer()


class MiPro(object):
    def gettext(self, url):
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.47',
            'cookie': 'unpl'
                      '=V2_ZzNtbRZSRkAmDERVfRpbUmJQEF9KBxYVcwEWBCsdVFFlARBZclRCFnUURlVnGVgUZwsZX0pcRhZFCEdkex5fDGQzEllCUUETcghEZEsaXDVmMxJaQFJAHXMAT1dyEFgAZgIVVUFWRBVFOEZcfyls0fKoytbVBQJXrLjjgtG3bAJiBBRUS1JHJXQ4R2Qwd11IZwQQWEFfRR18C09dfxxdBGALEVxFV3MURQs%3d; __jdv=76161171|c.mktdatatech.com|t_16282_151737613|tuiguang|e44db530726f4b339ad178aaa59e3335|1634297984488; __jdu=1634297982885400692061; areaId=16; ipLoc-djd=16-1315-46764-0; PCSYCityID=CN_350000_350200_350211; shshshfpa=bbd49cdc-6b5b-fc0d-0461-21eeaea49da2-1634297988; shshshfpb=xEdmUid06FhtbV9BShWa2qg%3D%3D; rkv=1.0; qrsc=3; __jda=122270672.1634297982885400692061.1634297982.1634297984.1634799674.2; __jdc=122270672; shshshfp=f6071145fbe9b4d3b17c550418edc813; 3AB9D23F7A4B3C9B=XQQEU4EIRLEXS6X7WCMGGUF3Z7OCIO7RVGCQT46ZC5CE3XHTUQDPMDWQ7QGQI7RGXQB3YKAKRUT4TBN6B224UCHM5Y '
        }
        try:
            response = requests.get(url=url, headers=header)
            try:
                html = response.text.encode("latin1").decode("utf-8")
                # print(html)
            except UnicodeEncodeError:
                html = response.text
                soup = BeautifulSoup(html, 'lxml')
                # print(soup.text)
            except UnicodeDecodeError:
                html = response.content.decode('gbk', 'ignore').encode('utf-8', 'ignore').decode('utf-8')
                soup = BeautifulSoup(html, 'lxml')
                # print(soup.text)
            else:
                soup = BeautifulSoup(html, 'lxml')
                # print(soup.text)
            response.close()
            txt = (soup.text.replace('\xa0', '\n').replace('\u2002', '\n').replace('\u3000', '\n').replace('\u200b',
                                                                                                        '\n').replace(
                '\t', '\n'))
            t = re.split('[\n]', txt)
            t = list(filter(None, t))
            tt = []
            for i in t:
                if len(i) >= 4: # tt为长度大于3的元素
                    tt.append(i)
            print(tt)
            tag = {'没有': 1}
            # t是数组，装着本url中全部的文本信息
            for i in t:
                term_list = analyzer.analyze(i)
                for n, term in enumerate(term_list):
                    if re.findall(r'/ns', str(term)):
                        need = re.findall('([\u4e00-\u9fa5]+)/ns', str(term))
                        for j in need:
                            if j in tag:
                                tag[j] = tag[j] + 1
                            else:
                                tag[j] = 1

            d_order = sorted(tag.items(), key=lambda x: x[1], reverse=True)
            # main_city为网站的地域
            main_city = d_order[0][0]
            return {'status': 'success', 'content': tt, 'main_city': main_city}
        except ConnectionError:
            return {'status': 'error', 'content': '网站无法连接'}
        except requests.exceptions.ConnectionError:
            return {'status': 'error', 'content': '网站无法连接'}
        except requests.exceptions.ReadTimeout:
            return {'status': 'error', 'content': '连接超时'}

    # 处理网页中的文本信息到excel
    def data_to_excel(self, content, city):
        date_save = time.strftime("%m月%d日", time.localtime(time.time()))
        quezhen_flag = False
        count = 0
        msg = []  # msg是保存着有时间的文字
        for i in content:
            pattern = '([1]?[0-9])月([0-9]*)日'
            j = re.findall(pattern, i)
            term_list = analyzer.analyze(i)
            need = ''
            count = 0
            for n, term in enumerate(term_list):
                if re.findall(r'/ns', str(term)):
                    count += 1
                    need = need + str(re.findall('([\u4e00-\u9fa5]+)/ns', str(term))[0])
            if count >= 2:
                print(need)
                msg.append(need)
            if len(j) != 0 and quezhen_flag is False:
                # date_save是确诊时间
                date_save2 = '2022' + '-' + str(int(j[0][0])) + '-' + str(int(j[0][1]))
                # t = datetime.datetime.strptime(date_save, "%Y/%m/%d")
                quezhen_flag = True
            # elif len(j) != 0:
            #     p = re.search(pattern, i)
            #     if p:
            #         msg.append(i)

        work_book = xlwt.Workbook(encoding='utf-8')
        sheet = work_book.add_sheet('message')
        sheet.write(0, 0, '在哪发现的')
        sheet.write(0, 1, '病例号数')
        sheet.write(0, 2, '发现日期')
        sheet.write(0, 3, '活动详情')
        if date_save2:
            date_save = date_save2
        base = []
        for n, i in enumerate(msg):
            sheet.write(n + 1, 0, city)
            sheet.write(n + 1, 1, n)
            sheet.write(n + 1, 2, date_save)
            sheet.write(n + 1, 3, i)
            dic = {'city': city, 'no': n, 'date': date_save, 'act': i}
            base.append(dic)
        file_name = time.strftime("%Y_%m_%d--%H_%M_%S", time.localtime(time.time())) + ".xls"
        file_name = os.path.join('Excel', file_name)
        work_book.save(file_name)
        return file_name, base
