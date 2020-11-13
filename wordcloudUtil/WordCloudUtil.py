import mysqlUtil
import jieba  #分词
# https://pypi.tuna.tsinghua.edu.cn/simple
from matplotlib import  pyplot as plt  #绘图
from wordcloud import WordCloud  #词语
from PIL import Image  #图片处理
import numpy as np  #矩阵运算
#查询词组
def wordcy(s):
    db = mysqlUtil.getDB()
    sql = "select "+s+" from doubanTop250"
    result = mysqlUtil.select(db,sql)
    print(result)
    strRes = ""
    for res in result:
        strRes = strRes+res[0]
    print(strRes)
    db.close()
    return strRes

#生成图片
def wordImg(text,ImgUrl,CyURl):
    #分词
    text = text.replace(" ","")
    text = text.replace("。","")
    text = text.replace(r"“", "")
    text = text.replace(r"， ", "")
    cut = jieba.cut(text)
    string = ' '.join(cut)
    print(string)

    #将图片转换为数组
    img = Image.open(ImgUrl)
    img_array = np.array(img)
    print(img_array)
    wordcol = WordCloud(background_color="white",mask=img_array,font_path="simsun")
    wordcol.generate_from_text(string)
    #绘制图片
    fig = plt.figure(1)
    plt.imshow(wordcol)
    plt.axis("off")
    # plt.show()
    plt.savefig(CyURl,dpi=500)
    return len(img_array)


