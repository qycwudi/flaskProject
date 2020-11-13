import mysqlUtil
import wordcloudUtil.WordCloudUtil as wc

data = wc.wordcy("leibie")
wc.wordImg(data,r".\static\assets\img\wordcloud\lb.jpg",r".\static\assets\img\wordcloud\lbWP.png")

# data = wc.wordcy("quote")
# print(wc.wordImg(data, r".\static\assets\img\wordcloud\lb.jpg", r".\static\assets\img\wordcloud\quoteWP.png"))

# data = wc.wordcy("guojia")
# wc.wordImg(data,r".\static\assets\img\lb.jpg",r".\static\assets\img\guojiaWP.png")