from flask import Flask,jsonify,render_template
from flask import request as frequest
from bs4 import BeautifulSoup
import requests,json
from fake_useragent import UserAgent
from proxy import Random_Proxy
import re
import os
app = Flask(__name__)

@app.route('/')
def ello():
	return 'Lyrics API'



def scraplyrics(url):
    header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',}

    res=requests.get(url,headers=header)
    html=BeautifulSoup(res.content,'lxml')
    lyric=html.find("p",{"id":"songLyricsDiv"}).get_text()
    return lyric


@app.route('/search=<lstring>')
def songlistapi(lstring):
    url="http://www.songlyrics.com/index.php?section=search&searchW="+lstring+"&submit=Search&searchIn1=artist&searchIn2=album&searchIn3=song"
    res=requests.get(url)
    html=BeautifulSoup(res.content,'lxml')
    x=html.find_all("div",class_="serpresult")
    name=[]
    link=[]
    lyric=[]
    for i in x[:7]:
        link.append(i.find('a').get('href'))
        name.append(i.find('a').get('title'))
        lyric.append(scraplyrics(i.find('a').get('href')))
    data=[]
    for i in range(len(name)):
        data.append({"name":name[i],"link":link[i],"lyrics":lyric[i]})
    return jsonify(data=data,status=200)






# now creating demo app so we will call api 


@app.route('/demo')
def demo():
    return render_template('lyricui.html')


@app.route('/demo/view',methods=['GET', 'POST'])
def viewlyric():
    input_url=frequest.form.get('link')
    xx=scraplyrics(input_url)
    return render_template('viewlyric.html',lyric=str(xx))

@app.errorhandler(404)
def page_not_found(error):
    return "<div style='text-align:center;padding:30;'><h1>Url Doesnt exist, hahaha!</h1></div>", 404


