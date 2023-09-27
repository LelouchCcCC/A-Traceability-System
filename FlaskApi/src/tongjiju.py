import pymysql
import pandas as pd


class Mysql_csv(object):
    # 定义一个init方法，用于读取数据库
    def __init__(self):
        # 读取数据库和建立游标对象
        self.connect = pymysql.connect(host='localhost', user='root', password='20010308', database='yiqing',
                                       charset='utf8')
        self.cursor = self.connect.cursor()

    # 定义一个del类，用于运行完所有程序的时候关闭数据库和游标对象
    def __del__(self):
        self.connect.close()
        self.cursor.close()

    def read_csv_values(self):
        # 读取csv文件数据
        csv_name = 'D:\python-workspace\\na.csv'
        data = pd.read_csv(csv_name, encoding="gbk")
        data_3 = list(data.values)
        return data_3

    def write_mysql(self):
        # 在数据表中写入数据，因为数据是列表类型，把他转化为元组更符合sql语句
        for i in self.read_csv_values():  # 因为数据是迭代列表，所以用循环把数据提取出来
            data_6 = tuple(i)
            sql = """insert into tovillage values{}""".format(data_6)
            self.cursor.execute(sql)
            self.commit()
        print("\n数据植入完成")

    def commit(self):
        # 定义一个确认事务运行
        self.connect.commit()

    def run(self):
        self.write_mysql()


# 最后用一个main()函数来封装
def main():
    sql = Mysql_csv()
    sql.run()


if __name__ == '__main__':
    main()
