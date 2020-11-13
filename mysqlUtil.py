import pymysql
import json
def connectDB():
    print("连接数据库")
    db = pymysql.connect("101.200.201.196",user="root",passwd="qycssg!0",db="db_doubandy",charset='utf8')
    print("连接成功")
    return db

# 创建表
def createTable(db,sql):
    cursor=db.cursor()
    # sql="CREATE TABLE "+"tableName"+" (id INT PRIMARY KEY NOT NULL,name TEXT NOT NULL,age INT NOT NULL,address CHAR(50),salary REAL);"
    try:
        print("开始执行sql")
        cursor.execute(sql)
        db.commit()
        print("建表提交")
        return True
    except:
        return False
# pip3 install --target=/home/wen/anaconda2/lib/python2.7/site-packages uwsgi

# 插入数据
def insertRecords(db,sql):
    cursor=db.cursor()
    try:
        # cursor.execute("INSERT INTO persons (id,name,age,address,salary) VALUES (2,'强月城',22,'zhongguo',2000.000)")
        cursor.execute(sql)
        db.commit()
        return True
    except:
        return False

# 删除
def delete(db):
    cursor = db.cursor()
    try:
        cursor.execute("delete from persons")
        db.commit()
        return True
    except:
        return False


# 查询
def select(db,sql):
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        # "select * from persons where age>=21 order by age desc"
        result = cursor.fetchall()
        return result
        # fields = ["id","name","age","address","salary"]
        # records = []
        # for row in result:
        #     records.append(dict(zip(fields,row)))
        # return json.dumps(records,ensure_ascii=False)
    except:
        print("出错了")
        return None

#创建DB
def getDB():
    return connectDB()