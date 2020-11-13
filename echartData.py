import mysqlUtil

def pingfen():
    sql = "select pingfen,COUNT(pingfen) from doubanTop250 GROUP BY pingfen"
    db = mysqlUtil.getDB()
    data = mysqlUtil.select(db,sql)
    pf = []
    sum = []
    for i in data:
        li = list(i)
        pf.append(float(li[0]))
        sum.append(li[1])
    da = {"pf":pf,"sum":sum}
    return da


def pjNum():
    sql="SELECT d2.pingfen,(SELECT SUM(pingjiaNum) from doubanTop250 as d1 where d1.pingfen=d2.pingfen) FROM `doubanTop250` as d2 GROUP BY d2.pingfen"
    db = mysqlUtil.getDB()
    data = mysqlUtil.select(db,sql)
    num = []
    for i in data:
        num.append(int(i[1]))
    return num
