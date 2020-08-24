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






<<<<<<< HEAD
=======
# def scrape_song_lyrics(url):
#     cookies = dict(privacypolicy='1xxxxxxxxxxxxxxxx')
#     header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',}
#     header=UserAgent()
#     # session=requests.Session()
#     try:
#         page =requests.get(url,headers=header)
#         html = BeautifulSoup(page.content, 'lxml')
#         lyrics = html.find('div', class_='lyrics').get_text()   
#     #remove identifiers like chorus, verse, etc
#     except:
#         try:
#             page =requests.get(url,headers=header)
#             html = BeautifulSoup(page.content, 'lxml')
#             lyrics = html.find('p', class_='').get_text()
#         except:
#             lyrics="try again after some time"
#     lyrics = re.sub(r'[\(\[].*?[\)\]]', '', lyrics)
#     lyrics = os.linesep.join([s for s in lyrics.splitlines() if s])         
#     return lyrics# DEMO

# def apifunction(lstring):

#     url="http://api.genius.com"
#     headers={'Authorization':''}
#     query=lstring
#     url=url+'/search?q='+query
#     res=requests.get(url,headers=headers)
#     dictionary=json.dumps(res.json(),sort_keys=True,indent=4)
#     res=res.json()
#     data=res['response']['hits']
#     title_songs=[]
#     link_songs=[]
#     lyric_songs=[]
#     for i in data:
#         title_songs.append(i['result']['full_title'])
#         link_songs.append(i['result']['url'])
#         lyric_songs.append(scrape_song_lyrics(i['result']['url']))

#     data=[]
#     for i in range(len(title_songs)):
#         data.append({"name":title_songs[i],"link":link_songs[i],"lyrics":lyric_songs[i]})
#     return jsonify(data=data,status=200)

# def givelyrics(input_url):

#     #linkss=int(input("Enter song number ........"))
#     headers = {'User-Agent': UserAgent().random}

#     lres=requests.get(input_url,headers)
#     lsoup=bs4.BeautifulSoup(lres.text,'lxml')

#     lresult=lsoup.find_all('div',{'class':'col-xs-12'})
#     check='<!-- MxM banner -->'
#     for lyric in lresult [1:2]:
#         lyricss=lyric.text

#     lyricss=lyricss.replace("\n\n\n\n\n","\n")
#     lyricss=lyricss.replace("\n\n\n","\n")

#     lyricss=lyricss[lyricss.find('lyrics')+6:]
#     lyricss=lyricss[lyricss.find('Lyrics')+6:]

#     lindex=lyricss.find('Submit Corrections')
#     data=lyricss[1:lindex]
#     return data


def hello_world(lstring):
    #lstring='Perfect ed sheeran'
    headers = {'User-Agent': UserAgent().random}

    res=requests.get('https://search.azlyrics.com/search.php?q=%s&w=songs'%lstring, headers=headers)
    soup=bs4.BeautifulSoup(res.content,'html.parser')
    result=soup.find_all('td',{"class":"text-left"})
    data=[]
    for link in result [0:6]:
        
        temp=(str(link.text[3:]).find('\n'))#ignoring first \n and will stop after second \n
        url=link.find('a').get('href')
        lyrics=givelyrics(url)
        name=link.text[3:temp+3]
        name=name[name.find(".")+2:]
        data.append({"name":name,"link":url,"lyrics":lyrics})
    return jsonify(data=data,status=200)


# tets for heroku
@app.route('/test')
def test():
    lstring='Perfect ed sheeran'

    headers = {'User-Agent': UserAgent().random}
    url='https://search.azlyrics.com/search.php?q=%s&w=songs'%lstring
    proxy=Random_Proxy()
    r=proxy.Proxy_Request(url=url,request_type='get')
    # soup=bs4.BeautifulSoup(res.content,'html.parser')
    # result=soup.find_all('td',{"class":"text-left"})

    return r.content

#api
@app.route('/link=<path:input_url>')
def showlyrics(input_url):

    #linkss=int(input("Enter song number ........"))
    print("hello")
    headers = {'User-Agent': UserAgent().random}

    lres=requests.get(input_url,headers)
    lsoup=bs4.BeautifulSoup(lres.text,'lxml')

    lresult=lsoup.find_all('div',{'class':'col-xs-12'})
    check='<!-- MxM banner -->'
    for lyric in lresult [1:2]:
        lyricss=lyric.text

    lyricss=lyricss.replace("\n\n\n\n\n","\n")
    lyricss=lyricss.replace("\n\n\n","\n")

    lyricss=lyricss[lyricss.find('lyrics')+6:]
    lyricss=lyricss[lyricss.find('Lyrics')+6:]

    lindex=lyricss.find('Submit Corrections')
    data=[{"data":lyricss[1:lindex]}]
    return jsonify(data=data,status=200)


>>>>>>> f534b0d8bf01c65af90a204dc72768366cfa0575
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


