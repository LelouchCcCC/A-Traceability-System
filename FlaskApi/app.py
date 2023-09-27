# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
from urllib import parse
import os
import pymysql
from src.wjw import Pachong
from src.msg import sj
import flask
from flask import Flask, render_template, request, jsonify
from src.baiduapi import Baid
from src.baiduapi import suyuan
from src.manager import manag
from src.managerquery.feedback_to_manager import ftm
from src.managerquery.email import SendEmail
from src.Spider.spider_to_sql import spider
from src.dataprocessing.mijieurl import MiPro
from src.chaxun import query
from src.userquery.userhome import user_query
from src.Policy.policy_web import Policy
from flask_cors import CORS, cross_origin
import configparser
from authlib.jose import jwt, JoseError
from flask_apscheduler import APScheduler
from src.aboutd.notice import Notice

config = configparser.ConfigParser()
config.read('config.ini')

scheduler = APScheduler()
Policy = Policy()

B = Baid()
S = suyuan()
Q = query()
M = manag()
STS = spider()
FTM = ftm()
UQ = user_query()
SE = SendEmail()
MJ = MiPro()
Notice = Notice()
app = Flask(__name__)
CORS(app, supports_credentials=True)


class Config(object):
    SCHEDULER_API_ENABLED = True


@scheduler.task('interval', id='do_job_1', minutes=30)
def job1():
    STS.exec()


app.config.from_object(Config())
scheduler.init_app(app)
scheduler.start()


def generate_token(user, **kwargs):
    """生成用于邮箱验证的JWT（json web token）"""
    SECRET_KEY = 'kkkkk'
    # 签名算法
    header = {'alg': 'HS256'}
    data = {'name': user}
    # 生成token
    encoded_jwt = jwt.encode(header, payload=data, key=SECRET_KEY)
    return str(encoded_jwt, encoding="utf-8")


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def sql_connect():
    conn = pymysql.connect(
        host=str(config.get('config', 'mysql_host').replace(',', '')),
        user=str(config.get('config', 'mysql_user').replace(',', '')),
        password=str(config.get('config', 'mysql_passwd').replace(',', '')),
        database='yiqing',
        charset='utf8',
        # autocommit=True,    # 如果插入数据，， 是否自动提交? 和conn.commit()功能一致。
    )
    return conn


# ,static_folder='../pycharm_vue/dist/static',template_folder='../pycharm_vue/dist'

# CORS(app, supports_credentials=True)
# 路由

@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin'] = '*'
    environ.headers['Access-Control-Allow-Method'] = '*'
    environ.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return environ


# @app.route('/')
# def index():
#     return render_template('COVID-19_China.html')

@app.route('/mag')
def manage():
    return render_template('manage.html')


@app.route('/tst')
def tst():
    target = S.sql_get_city()
    print(target)
    may, moremay, = S.judd(target)
    dic = S.cont(target)
    # print(city_name)
    commu = []
    for i in range(len(target)):
        mb_city = []
        ci = may[i][0]
        mi_li = moremay[i][1]
        fu_li = may[i][1]
        mb_city.append(ci)
        mb_city.append(fu_li)
        mb_city.append(mi_li)
        commu.append(mb_city)
    u = []

    last_tar = []
    for i in target:
        targ = []
        targ.append(i[0])
        targ.append(str(i[1].year) + '-' + str(i[1].month) + '-' + str(i[1].day))
        last_tar.append(targ)
    for n, i in enumerate(commu):
        if len(i[2]) == 0:
            if len(i[1]) == 0:
                temp = '信息不足,暂为本土出现的疫情'
            else:
                temp = '可能是与' + str(list(set(i[1]))).replace('[', '').replace(']', '').replace("'", "") + '有关'
        else:
            temp = '很可能与' + str(list(set(i[2]))).replace('[', '').replace(']', '') + '有关'
        u.append([last_tar[n], temp])
    print(u)
    uu = []
    for i in u:
        pp = {'date': i[0][1], 'city': i[0][0], 'message': i[1], 'num': dic[i[0][0]]}
        uu.append(pp)
    print(uu)
    non = []
    on = []
    ons = []
    for i in uu:
        if i['message'] == '信息不足,暂为本土出现的疫情':
            non.append(i)
        elif ',' not in i['message']:
            on.append(i)
        else:
            ons.append(i)
    sysy = {'non': non, 'on': on, 'ons': ons}
    return {'key': u, 'key2': uu, 'key3': sysy}


@app.route('/lks')
def lks():
    target = S.sql_get_city()
    data, geo = S.displ(target)
    return {'data': data, 'geo': geo}


@app.route('/onec', methods=['POST', 'GET'])
def onec():
    t_a = request.data
    data_json = json.loads(t_a)
    t_a = data_json['cityName']
    target = S.sql_get_city()
    data, geo, val = S.city_one(target, t_a)
    cityname = S.sql_get_city()
    mm = S.judd_one(target, t_a)
    left = []
    for i in cityname:
        left.append(i[0])
    return {'data': data, 'geo': geo, 'left': left, 'val': val, 'mm': mm}


@app.route('/onecc')
def onecc():
    t_a = request.args.get("ci")
    target = S.sql_get_city()
    data, geo, val = S.city_one(target, t_a)
    cityname = S.sql_get_city()
    mm = S.judd_one(target, t_a)
    # curt_city=
    left = []
    for i in cityname:
        left.append(i[0])
    return {'data': data, 'geo': geo, 'left': left, 'val': val, 'mm': mm}


@app.route('/fenci1')
def fenci1():
    txt = request.args.get("txt")
    city = request.args.get("city")
    lst = Q.cuti(txt, city)
    print(lst)
    return {'lst': lst}


@app.route('/fin_com')
def fin_com():
    data = request.args.getlist('msg[]')
    city = request.args.get('city')
    print(data, city)
    fir, sec, fir2, sec2 = Q.panduan(data, city)
    for i in sec2:
        if len(i['result']['nearby']) == 0:
            i['result']['isSafe'] = '1'
            i['result']['msg'] = '安全！未检测到附近存在中高风险地区'
        else:
            i['result']['isSafe'] = '0'
            st = '、'.join(i['result']['nearby'])
            i['result']['msg'] = '危险！检测到附近存在中高风险地区: ' + str(st)
    print(sec2)
    return {'fir': fir, 'sec': sec}


@app.route('/upload', methods=['POST'])
def upload():
    B = Baid()
    upload_path = config.get('config', 'root_path').replace(',', '')
    upload_path = upload_path.replace('"', '')
    file = flask.request.files['file']
    if not file:
        return {"status": "fail"}
    filename = file.filename
    extension = filename.split('.')[-1]
    if extension == 'xls':

        file.save(os.path.join(upload_path, filename))
        result = {"status": 200}
        B.specify_act(filename)
        return json.dumps(result)
    else:
        return {"status": "extension error"}


@app.route('/manager_url', methods=['POST'])
def managerurl():
    data = request.data
    data_json = json.loads(data)
    # 网址
    url = data_json['url']
    # {'status': 'success', 'content': t, 'main_city':main_city}
    need = MJ.gettext(url)
    content = need['content']
    main_city = need['main_city']
    filename, base = MJ.data_to_excel(content=content, city=main_city)
    B.specify_act2(filename=filename, base=base)
    # hd = B.jiexi()
    return {'need': need, 'base': base}


@app.route('/login', methods=['POST'])
def login():
    data = request.data
    if len(data) == 0:
        return 'ok'
    else:
        data_json = json.loads(data)
        username = data_json['username']
        password = data_json['password']
    conn = sql_connect()
    cursor = conn.cursor()
    sql = 'select level from user where username="' + str(username) + '" and password="' + str(password) + '";'
    cursor.execute(sql)
    a = cursor.fetchone()
    try:
        a = a[0]
        if a == 0:  # 终极管理员
            token = generate_token(username)
            res = {
                'code': '20000',
                'message': '成功取到用户信息',
                'token': token,
                'level': 'atAdmin'
            }
        elif a == 1:  # 普通管理员
            token = generate_token(username)
            res = {
                'code': '20003',
                'message': '成功取到用户信息',
                'token': token,
                'level': 'admin'
            }
        else:
            res = {'code': '20001', 'message': '未获取到用户信息'}
    except TypeError:
        res = {'code': '20002', 'message': '用户名或密码错误'}
    return json.dumps(res)


@app.route('/userhome', methods=['POST', 'GET'])
def userhome():
    data = UQ.cha()
    # return {data: data}
    return jsonify(data)


@app.route('/query', methods=['POST'])
def query():
    data = request.data
    data = data.decode('utf-8').replace('\\x', '%')
    data = parse.unquote(data)
    data = json.loads(data)
    print(data['date'])
    print(data['message'])
    a = Q.new_judge(data['date'], data['message'])
    if len(a) >= 1:
        return {"res": "1", "msg": "查询到您与确诊或疑似人员同乘同一交通工具，请您做好个人防护，通过“国家政务服务平台”自查是否为“同行密接人员”，以便进一步核查您的健康状况！"}
    else:
        return {"res": "0", "msg": "数据库中未查询到您与确诊或疑似人员同乘同一交通工具，请继续保持有效防护。"}


@app.route('/feedback', methods=['POST'])
def get_feed():
    data = request.data
    data = data.decode('utf-8').replace('\\x', '%')
    data = parse.unquote(data)
    data = json.loads(data)
    desc = data['desc']
    email = data['email']
    re = UQ.pos_feedback(desc, email)
    return {'ok': re}


# 管理员获取feedback
# 要改请求
@app.route('/managerfeed', methods=['GET', 'POST'])
def manager_feed():
    try:
        data = request.data
        data = data.decode('utf-8').replace('\\x', '%')
        data = parse.unquote(data)
        data = json.loads(data)
        date = data['date']
        email = data['email']
        FTM.pos01(date, )
    except:

        data = FTM.get_feedback()

    return {'data': data}


@app.route('/sendemail', methods=['POST'])
def send_email():
    data = request.data
    data = data.decode('utf-8').replace('\\x', '%')
    data = parse.unquote(data)
    data = json.loads(data)
    print(data)
    receiver = data['receiver']
    content = data['content']
    print(receiver)
    status = SE.sending(receiver=receiver, content=content)
    return status


@app.route('/policy', methods=['POST'])
def get_policy():
    data = request.data
    data = data.decode('utf-8').replace('\\x', '%')
    data = parse.unquote(data)
    data = json.loads(data)
    data = data['cityname']
    print(data)
    pol = Policy.exec(data)
    return pol


@app.route('/getleft', methods=['GET'])
def get_left():
    target = S.sql_get_city()
    print(target)
    return {'target': target}


@app.route('/huidiao')
def huidiao():
    hd = B.jiexi()
    return {'kk': hd}


@app.route('/confirm')
def confirm():
    data = request.args.getlist('dd[]')
    ret = M.confm(data)
    if ret == 'ok':
        return {'status': 'okok'}
    else:
        return {'status': 'error'}


# 下面是新项目的接口
@app.route('/statistics.json', methods=['GET'])
def statics():
    data = UQ.cha()
    return jsonify(data)


@app.route('/feedback_success', methods=['POST'])
def feed_suc():
    try:
        data = request.data
        data = data.decode('utf-8').replace('\\x', '%')
        data = parse.unquote(data)
        data = json.loads(data)
        desc = data['content']
        email = data['email']
        re = UQ.pos_feedback(desc, email)
        return {"res": "1", "msg": "反馈提交成功！"}
    except:
        return {"res": "0", "msg": "反馈提交失败！"}


@app.route('/notice.json', methods=['GET'])
def get_notice():
    data = Notice.no()
    return jsonify(data)


@app.route('/contacts_check_safe.json', methods=['POST'])
def check_safe():
    data = request.data
    data = data.decode('utf-8').replace('\\x', '%')
    data = parse.unquote(data)
    print(data)
    data = json.loads(data)
    print('------')
    print(data)
    print(data['date'])
    print(data['number'])
    a = Q.new_judge(data['date'], data['number'])
    if len(a) >= 1:
        return {"res": "1", "msg": "查询到您与确诊或疑似人员同乘同一交通工具，请您做好个人防护，通过“国家政务服务平台”自查是否为“同行密接人员”，以便进一步核查您的健康状况！"}
    else:
        return {"res": "0", "msg": "数据库中未查询到您与确诊或疑似人员同乘同一交通工具，请继续保持有效防护。"}


# 数据接收形式有问题
@app.route('/regions_search.json', methods=['POST'])
def region_sech():
    data = request.data
    print(data)
    data = data.decode('utf-8').replace('\\x', '%')
    data = parse.unquote(data)
    data = json.loads(data)
    print(data)
    dataa = []
    # place = data['place']
    # date = data['date']
    # source = data['source']
    # location = source['location']
    # print(date)
    # print(place)
    # fir, sec, fir2, sec2 = Q.panduan(date, source)
    fir, sec, fir2, sec2 = Q.new_judge_panduan(data)
    for i in sec2:
        if len(i['result']['nearby']) == 0:
            i['result']['isSafe'] = '1'
            i['result']['msg'] = '安全！未检测到附近存在中高风险地区'
        else:
            i['result']['isSafe'] = '0'
            st = '、'.join(i['result']['nearby'])
            i['result']['msg'] = '危险！检测到附近存在中高风险地区: ' + str(st)
    for i in fir2:
        if len(i['result']['nearby']) == 0:
            i['result']['isSafe'] = '1'
            i['result']['msg'] = '安全！未检测到附近存在中高风险地区'
        else:
            i['result']['isSafe'] = '0'
            st = '、'.join(i['result']['nearby'])
            i['result']['msg'] = '危险！检测到附近存在中高风险地区: ' + str(st)
    print(fir2)
    print(sec2)
    return {'complex': fir2}


# 添加管理员
@app.route('/add-manager', methods=['POST'])
def addman():
    data = request.data
    print(data)
    data = data.decode('utf-8').replace('\\x', '%')
    data = parse.unquote(data)
    data = json.loads(data)
    name = data['username']
    password = data['password']
    res = FTM.addman(name, password)
    return res


# 查看管理员
@app.route('/watch-manager', methods=['GET'])
def watchman():
    wm = FTM.watchman()
    return {'np': wm}


@app.route('/bullt', methods=['POST'])
def bullt():
    data = request.data
    print(data)
    data = data.decode('utf-8').replace('\\x', '%')
    data = parse.unquote(data)
    data = json.loads(data)
    title = data['name']
    url = data['url']
    abstract = data['abstract']
    time = data['value3']
    timeout = data['value4']
    back = Notice.on(title, abstract, url, time, timeout)

    return back


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
    # print_hi('PyCharm')
    # s = sj()
    # B.datatosql()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
