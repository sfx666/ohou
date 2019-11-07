from _sha1 import sha1
from datetime import datetime


import pymysql

from settings import dbParams
# 1.创建连接对象
conn=pymysql.Connect(**dbParams)

# 2.创建游标对象
cursor=conn.cursor()

# 创建库
try:
    sql="create database testt default charset = utf8"

    cursor.execute(sql)
    conn.commit()
except Exception as e:
    print(e)
finally:
    cursor.close()
    conn.close()


# 创建表
try:

    sql ="create table if not exists user(uid int primary key auto_increment,username varchar(50) unique," \
         "usertype enum('普通用户','管理员') default '普通用户',password  varchar(50) not null,regtime datetime," \
         "email varchar(50))"
    cursor.execute(sql)
    conn.commit()
except Exception as e:
    print(e)
finally:
    cursor.close()
    conn.close()

# 用户注册
try:
    index_username = "select username from user"
    username = input("请输入用户名:")
    while len(username) < 2:
        print("用户名长度小于2,请重新输入")
        username = input("请输入用户名:")
    while username in index_username:
        print("用户名存在,请重新输入")
        username = input("请输入用户名:")
    usertype = input("用户类型:")
    password = input("请填写密码:")
    email = input("请填写邮箱:")
    sql = "insert into user(username,usertype,password,regtime,email) values('{}','{}','{}','{}','{}')".format(username,usertype,sha1(password),datetime.now(),email)
    print(sql)
    result = cursor.execute(sql)
    conn.commit()
    print(result)
    if result > 0:
        print("执行成功")
    else:
        print("执行失败")
except Exception as e:
    print(e)
    conn.rollback()
finally:
    cursor.close()
    conn.close()

# 用户登录
username = input("请输入用户名：")
password = input("请输入密码：")
password = sha1(password.encode('utf8')).hexdigest()
print(username,password)

sql = "select uid from user where username= %s and password= %s"
print(sql)

result = cursor.execute(sql,[username,password])
print(result)
print(cursor._executed)

if result>0:
    print("登录成功")
else:
    print("登录失败,重新登录")

cursor.close()
conn.close()


