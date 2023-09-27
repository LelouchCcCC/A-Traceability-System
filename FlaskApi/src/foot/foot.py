import configparser
import pymysql
import re
import time
import os
import subprocess


class work(object):
    def __init__(self):
        self.logpath = os.path.abspath('.') + '\mysql.log'
        self.prefix = 'xh_'

    def sql_connect(self):
        config = configparser.ConfigParser()
        config.read('./config.ini')
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='yiqing',
            charset='utf8',
            # autocommit=True,    # 如果插入数据，， 是否自动提交? 和conn.commit()功能一致。
        )
        return conn

    def run(self):
        conn = self.sql_connect()
        cursor = conn.cursor()
        cursor.execute('set global general_log = on')
        conn.commit()
        current_path = 'set global log_output = \'file\''
        cursor.execute(current_path)
        conn.commit()
        cursor.execute('set global general_log_file=' + '\'' + self.logpath + '\'')
        conn.commit()
        conn.close()

        return 0

    def monitor(self):
        command = 'tail -f ' + self.logpath
        popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        try:
            while True:
                line = popen.stdout.readline().strip()
                print('line:', line)
                encodeStr = bytes.decode(line)
                pattern = re.findall('Query\s*(.*)', encodeStr, re.S)
                if len(pattern) != 0:
                    selectStr = pattern[0]
                    if selectStr != "COMMIT":
                        joinTime = time.strftime("%H:%M:%S", time.localtime()) + ' '
                        if self.prefix != "":
                            reg = re.findall(r'\b' + self.prefix + '\w*', encodeStr, re.S)
                            if len(reg) != 0:
                                table = '操作的表:' + reg[0]
                                joinTime += table
                                print(joinTime + ' ' + selectStr)
        except KeyboardInterrupt:
            os.remove(self.logpath)

if __name__ == '__main__':
    w = work()
    w.run()
    w.monitor()