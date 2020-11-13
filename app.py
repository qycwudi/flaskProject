from flask import Flask,render_template,request,jsonify
import movieList
import echartData
app = Flask(__name__)


@app.route('/test')
def index():
    return render_template("test.html")

@app.route("/")
def hello():
    RPicture = {
        "quoteWP": "static/assets/img/wordcloud/quoteWP.png",
        "guojiaWP": "static/assets/img/wordcloud/guojiaWP.png",
        "lbWP": "static/assets/img/wordcloud/lbWP.png",
        "guojiaa": "static/assets/img/ico/guojiaa.png",
        "leibiee": "static/assets/img/ico/leibiee.png",
        "WP":"static/assets/img/wordcloud/quoteWP.png"
    }
    movielist = []
    for mo in movieList.showTop6():
        movielist.append(list(mo))
    print(movielist)
    guojiaNum = movieList.showGuojiaNum()
    leibieNum = movieList.showleibieNum()
    movie = {
        "movieList": movielist,
        "movieNum":"250",
        "wordcloudNum":"370",
        "guojiaNum":str(guojiaNum),
        "leibieNum":str(leibieNum)
    }
    return render_template("index.html", RPicture=RPicture,movie=movie)

@app.route("/movie")
def movie():
    movielist = []
    for mo in movieList.showTop6():
        movielist.append(list(mo))
    movie = {
        "movielist":movielist,
        "movie1": movielist[0],
        "movie2": movielist[1],
        "movie3": movielist[2],
    }
    return render_template("douban/movie.html",movie=movie)

@app.route("/movieview")
def movieview():
    # num = request.form.get("")
    # print(movieList.showPage(int(num)))
    num = request.args.get("num")
    page = movieList.showPage(int(num))
    pagemovie = []
    for mo in page:
        pagemovie.append(list(mo))
    return jsonify({"pagemovie":pagemovie})
    # return render_template("douban/movie.html")


@app.route("/dataview")
def dataview():
    pfmap = echartData.pingfen()
    pjnum = echartData.pjNum()
    return render_template("douban/dataview.html",pfmap=pfmap,pjnum = pjnum)


@app.route("/wordcloud/<name>")
def wordcloud(name):
    WPURL = ""
    if name == "gjz":
        WPURL = "/static/assets/img/wordcloud/quoteWP.png"
    elif name == "guojia":
        WPURL = "/static/assets/img/wordcloud/guojiaWP.png"
    elif name == "leibie":
        WPURL = "/static/assets/img/wordcloud/lbWP.png"
    return render_template("douban/wordcloud.html",WPURL= WPURL)

@app.route("/qiangyuecheng")
def qiangyuecheng():
    return render_template("douban/qiangyuecheng.html")
if __name__ == '__main__':
    app.run(debug=True)
