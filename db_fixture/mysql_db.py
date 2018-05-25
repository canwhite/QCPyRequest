# coding=utf8
#游标
import pymysql.cursors
#os模块
import os
#用于操作配置文件
import configparser as cparser


#通过以上解释，第一步os.path.dirname(__file__)返回到／pyrequest-master／db_fixture
#第二步返回到／pyrequest-master，也就是说这种操作返回到了上一层目录
base_dir = str(os.path.dirname(os.path.dirname(__file__)))


#将地址"\"转化成反斜杠"/",windows到mac的转换
base_dir = base_dir.replace('\\', '/')

#拼接处完整路径
file_path = base_dir + "/db_config.ini"


#操作配置文件
cf = cparser.ConfigParser()
#读取文件内容
cf.read(file_path)
#从[mysqlconf]层中读取的host键对应的value，以下的内容类似
host = cf.get("mysqlconf", "host")
port = cf.get("mysqlconf", "port")
db   = cf.get("mysqlconf", "db_name")
user = cf.get("mysqlconf", "user")
password = cf.get("mysqlconf", "password")



# ======== MySql base operating ===================
class DB:


    #初始化链接
    def __init__(self):
        try:
            # Connect to the database
            #使用pymysql的connect方法
            self.connection = pymysql.connect(host=host,
                                              port=int(port),
                                              user=user,
                                              password=password,
                                              db=db,
                                              charset='utf8mb4',
                                              cursorclass=pymysql.cursors.DictCursor)
        except pymysql.err.OperationalError as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))



    # 清空表
    def clear(self, table_name):


        # real_sql = "truncate table " + table_name + ";"
        #创建一条sql语句，删除表中所有内容
        real_sql = "delete from " + table_name + ";"
        #as 后边的cursor 相当于一个别名
        with self.connection.cursor() as cursor:
            #Mysql中如果表和表之间建立的外键约束，则无法删除表及修改表结构。

            # 解决方法是在Mysql中取消外键约束:  SET FOREIGN_KEY_CHECKS=0;

            # 然后将原来表的数据导出到sql语句，重新创建此表后，再把数据使用sql导入，

            # 然后再设置外键约束: SET FOREIGN_KEY_CHECKS=1;
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            #执行上面那个不需要参数的sql语句，删除表数据
            cursor.execute(real_sql)
        #往服务器提交一下操作
        self.connection.commit()




    # 插入语句
    def insert(self, table_name, table_data):

        #我们先看两个插入方法举例
        #insert into test values('charies',18,'3.1’);#这个是按顺序插
        #insert into test(age,name) values(18,'guo’);#这个是给部分字段插入数据，前后是一一对应的

        #我们可以在这里建个表







        #将value值转化为字符串再重新存贮
        for key in table_data:
            table_data[key] = "'"+str(table_data[key])+"'"
        #join
        #语法：  'sep'.join(list)
        # sep：分隔符。可以为空
        # list：要连接的元素序列、字符串、元组、字典

        key   = ','.join(table_data.keys())
        value = ','.join(table_data.values())

        #再写sql字段
        real_sql = "INSERT INTO " + table_name + " (" + key + ") VALUES (" + value + ")"
        #print(real_sql)

        with self.connection.cursor() as cursor:
            #执行sql语句
            cursor.execute(real_sql)
        #操作提交一下
        self.connection.commit()





    # 关闭数据链接
    def close(self):
        self.connection.close();



    #初始化的时候数据是datas
    def init_data(self, datas):

        for table, data in datas.items():

            self.clear(table)
            for d in data:
                self.insert(table, d)
        self.close()






if __name__ == '__main__':

    db = DB()
    table_name = "sign_event"
    data = {'id':1,'name':'红米','`limit`':2000,'status':1,'address':'北京会展中心','start_time':'2016-08-20 00:25:42','create_time':'2017-08-20 12:23:35'}
    # table_name2 = "sign_guest"
    # data2 = {'realname':'alen','phone':12312341234,'email':'alen@mail.com','sign':0,'event_id':1}

    db.clear(table_name)
    db.insert(table_name, data)
    db.close()


