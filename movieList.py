import mysqlUtil

def showTop6():
    sql = "select * from doubanTop250 where id<7"
    db = mysqlUtil.getDB()
    data = mysqlUtil.select(db, sql)
    db.close()
    return data

def showGuojiaNum():
    #电影num  国家num 类别num
    sql = "select guojia from doubanTop250"
    db = mysqlUtil.getDB()
    data = mysqlUtil.select(db,sql)
    guojialist = []
    guojiazd = {}
    for i in data:
        guojialist.append(list(i))
    for j in guojialist:
        str = j[0].replace(" ",",")
        str = str[:-1]
        print(str)
        if str != "":
            guojiaOne = str.split(",")
            for one in guojiaOne:
                guojiazd[one] = 1
    return len(guojiazd)

def showleibieNum():
    # 电影num  国家num 类别num
    sql = "select leibie from doubanTop250"
    db = mysqlUtil.getDB()
    data = mysqlUtil.select(db, sql)
    guojialist = []
    guojiazd = {}
    for i in data:
        guojialist.append(list(i))
    for j in guojialist:
        str = j[0].replace(" ", ",")
        str = str[:-1]
        print(str)
        if str != "":
            guojiaOne = str.split(",")
            for one in guojiaOne:
                guojiazd[one] = 1
    return len(guojiazd)

def showPage(num):
    star = (num-1)*18
    sum = num*18
    sql = "select * from doubanTop250 where id<="+str(sum)+" and id>"+str(star)
    print(sql)
    db = mysqlUtil.getDB()
    data = mysqlUtil.select(db, sql)
    return data
