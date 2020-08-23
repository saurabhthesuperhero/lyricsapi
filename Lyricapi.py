from flask import Flask,jsonify,render_template
import bs4
import requests,json
from fake_useragent import UserAgent

app = Flask(__name__)

@app.route('/')
def ello():
	return 'Lyrics API'

def givelyrics(input_url):

    #linkss=int(input("Enter song number ........"))
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
    data=lyricss[1:lindex]
    return data


@app.route('/search=<lstring>')
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

    res=requests.get('https://search.azlyrics.com/search.php?q=%s&w=songs'%lstring, headers=headers)
    # soup=bs4.BeautifulSoup(res.content,'html.parser')
    # result=soup.find_all('td',{"class":"text-left"})

    return res.content

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


# now creating demo app so we will call api 


def showlyricsnotapi(input_url):

    #linkss=int(input("Enter song number ........"))
    headers = {'User-Agent': UserAgent().random}

    lres=requests.get(input_url,headers)
    lsoup=bs4.BeautifulSoup(lres.text,'lxml')

    lresult=lsoup.find_all('div',{'class':'col-xs-12'})
    check='<!-- MxM banner -->'
    for lyric in lresult [1:2]:
        lyricss=lyric.text



    lindex=lyricss.find('Submit Corrections')
    data=[{"data":lyricss[10:lindex]}]
    return (data)

def callapi():
    import requests,json
    url='http://127.0.0.1:5000/search=blank%20space'
    headers = {'User-Agent': UserAgent().random}
    res=requests.get(url,headers)
    res=json.loads(res.content)
    return res['data']

@app.route('/demo')
def demo():
	listlyrics=callapi()
	print(listlyrics)
	return render_template('lyricui.html')


@app.route('/demo/view=<path:input_url>',methods=['GET', 'POST'])
def viewlyric(input_url):
    x=showlyricsnotapi(input_url)
    xx=x[0]['data']
    xx=(xx.replace("\n\n\n\n\n\n\n",""))
    # print(xx)
    xx=xx.replace("\n\n\n\n\n\n","\n")
    xx=xx.replace("\n","</br>")
    temp=xx.find("lyrics")
    nn=(xx[:temp])
    xx=xx[temp+6:]
    print( str(xx))
    return render_template('viewlyric.html',name=nn,lyric=str(xx))

@app.errorhandler(404)
def page_not_found(error):
    return "<div style='text-align:center;padding:30;'><h1>Url Doesnt exist, hahaha!</h1></div>", 404


