import urllib.request
from bs4 import BeautifulSoup
import re
import xlwt
import MysqlCRUD
#正则表达式
findLink = re.compile(r'<a class="" href="(.*?)">')
title = re.compile(r'<span class="title">(.*?)</span>')
imgLink = re.compile(r'<img .* src="(.*?)".*/>')
daoyan = re.compile(r'<p class="">.*导演:(.*?)主.',re.S)
zhuyan = re.compile(r'<p class="">.*主.:(.*?)/.*</p>',re.S)
message = re.compile(r'<p class="">.*主..*<br/>(.*?)</p>',re.S)
pingfen = re.compile(r'<span class="rating_num".*property="v:average">(.*?)</span>',re.S)
pingjiaNum = re.compile(r'<span>(.*?)人评价</span>')
quote = re.compile(r'<span class="inq">(.*?)</span>')
data = []
def getData(baseurl):
    headers = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64;rv:82.0) Gecko / 20100101 Firefox / 82.0"
        # "User-Agent": "Mozilla / 5.0(Windows NT 10.0; WOW64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 65.0.3325.181 Safari / 537.36"
    }
    requset = urllib.request.Request(url=baseurl,headers=headers)
    response = urllib.request.urlopen(requset)
    return response.read().decode("utf-8")

def readPage(pageNum):
    f = open("doubantop250/%dpages.html"%pageNum,"r",encoding="utf-8")
    return f.read()
def bs4(htmlFile):
    #查找div下item类
    bs = BeautifulSoup(htmlFile,"html.parser")
    item = bs.find_all("div", class_="item") #class_表示为一个类
    for dy in item:
        movie = []
        dy = str(dy)
        link = re.findall(findLink,dy)[0]
        movie.append(link)
        imglink = re.findall(imgLink,dy)[0]
        movie.append(imglink)
        tit = re.findall(title,dy)
        if tit.__len__()==2:
            #中文名
            ctitle = tit[0]
            #英文名
            wtitle = str(tit[1]).replace("/","")
            wtitle = wtitle.replace("'","")
            elist = wtitle.split()
            wtitles = ""
            for el in elist:
                wtitles = wtitles+el+" "
            movie.append(ctitle)
            movie.append(wtitles)
        else:
            ctitle = tit[0]
            movie.append(ctitle)
            movie.append(" ")
        #导演
        daoy = re.findall(daoyan,dy)
        daoylist = str(daoy).replace(r"\xa0","")
        daoylist = daoylist.replace("[","")
        daoylist = daoylist.replace("]", "")
        daoylist = daoylist.replace("\'", "")
        movie.append(daoylist)
        #主演
        zhuy = re.findall(zhuyan,dy)
        zhuy = str(zhuy).replace("<br","")
        zhuy = zhuy.replace("[","")
        zhuy = zhuy.replace("]", "")
        zhuy = zhuy.replace("\'", "")
        movie.append(zhuy)

        #上映日期
        startYear = re.findall(message,dy)
        if startYear.__len__()==0:
            movie.append("")
        else:
            movie.append(str(startYear).split().pop(1)[0:4])

        #分类
        mess = re.findall(message,dy)
        if mess.__len__()==0:
            movie.append(" ")
            movie.append(" ")
        else:
            guojia = mess[0].strip().split("/")[1]
            leibie = mess[0].strip().split("/")[2]
            gj = ""
            for a in guojia.split():
                gj = gj+a+" "
            lb = ""
            for b in leibie.split():
                lb = lb + b + " "
            movie.append(gj)
            movie.append(lb)


        #评分
        rating_num = re.findall(pingfen,dy)[0]
        movie.append(rating_num)

        #评价人数
        pjnum = re.findall(pingjiaNum,dy)[0]
        movie.append(pjnum)

        #简介
        inq = re.findall(quote,dy)
        if inq.__len__()==0:
            movie.append(" ")
        else:
            movie.append(inq[0].replace("'","‘"))
        data.append(movie)

def name_is_exists(tag):
    return tag.has_attr("href")

def saves(data,path):
    book = xlwt.Workbook(encoding="UTF-8")
    sheet = book.add_sheet("豆瓣TOP250")
    col = ["详情链接","图片链接","电影名称","英文名称","导演","主演","上映时间","分类","豆瓣评分","评论人数","概括"]
    for i in range(0,10):
        sheet.write(0,i,col[i])
    for j in range(0,250):
        one = data[j]
        print(one)
        for k in range(0,10):
           sheet.write(j+1,k,one[k])
        print(j+1)
    book.save(path)

def savePage(htmlfile,pageNum):
    f = open("doubantop250/%dpages.html"%pageNum,"a+")
    f.close()
    with open("doubantop250/%dpages.html"%pageNum,"wb") as f:
        #   写文件用bytes而不是str，所以要转码
        f.write(bytes(htmlfile.encode('utf-8')))
def saveMysql(data):
    db = MysqlCRUD.getDB()
    # print(db)
    # print("建库")
    # MysqlCRUD.createTable(db,"CREATE TABLE doubanTop250 (id int(11) NOT NULL AUTO_INCREMENT,findLink varchar(255) DEFAULT NULL,imgLink varchar(255) DEFAULT NULL,ctitle varchar(255) DEFAULT NULL,wtitle varchar(255) DEFAULT NULL,daoyan varchar(255) DEFAULT NULL,zhuyan varchar(255) DEFAULT NULL,time varchar(255) DEFAULT NULL,guojia varchar(255) DEFAULT NULL,leibie varchar(255) DEFAULT NULL,pingfen varchar(255) DEFAULT NULL,pingjiaNum varchar(255) DEFAULT NULL,quote varchar(255) DEFAULT NULL,PRIMARY KEY (`id`));")
    # print("建库完成")

    #插入数据
    for j in range(0,250):
        one = data[j]
        sql = ""
        for k in range(0,12):
            if k !=11:
                sql = sql+"'"+one[k]+"',"
            else:
                sql = sql +"'"+ one[k]+"'"
        sql = "insert into doubanTop250 (findLink,imgLink,ctitle,wtitle,daoyan,zhuyan,time,guojia,leibie,pingfen,pingjiaNum,quote) values ("+sql+");"


        if(MysqlCRUD.insertRecords(db,sql)):
            print(j+1)
        else:
            print("失败",j+1)
            print("****" + sql)
    print("插入成功")
if __name__ == "__main__":
    baseurl = "https://movie.douban.com/top250?start="
    #爬取网页
    for i in range(0,10):
        url = baseurl+str(i*25)
        # htmlFile = getData(url)
        htmlFile = readPage(i)
        # savePage(htmlFile,i)
    # 解析数据
        bs4(htmlFile)
    print(data)

    #保存数据
    # saves(data,"D:/自编程序/studyPython/doubanTOP250.xls")
    saveMysql(data)
