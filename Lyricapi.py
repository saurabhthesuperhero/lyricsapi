from flask import Flask,jsonify,render_template
import bs4
import requests,json
app = Flask(__name__)

@app.route('/')
def ello():
	return 'Lyrics API'

@app.route('/search=<lstring>')
def hello_world(lstring):
    #lstring='Perfect ed sheeran'
    res=requests.get('https://search.azlyrics.com/search.php?q=%s&w=songs'%lstring,timeout=5)
    soup=bs4.BeautifulSoup(res.text,'lxml')
    result=soup.find_all('td',{"class":"text-left"})
    data=[]
    for link in result [0:6]:
        
        temp=(str(link.text[3:]).find('\n'))#ignoring first \n and will stop after second \n
        data.append({"name":link.text[3:temp+3],"link":link.find('a').get('href')})
    return jsonify(data=data,status=200)
    

#api
@app.route('/link=<path:input_url>')
def showlyrics(input_url):

    #linkss=int(input("Enter song number ........"))
    print("hello")
    lres=requests.get(input_url)
    lsoup=bs4.BeautifulSoup(lres.text,'lxml')

    lresult=lsoup.find_all('div',{'class':'col-xs-12'})
    check='<!-- MxM banner -->'
    for lyric in lresult [1:2]:
        lyricss=lyric.text


    lindex=lyricss.find('Submit Corrections')
    data=[{"data":lyricss[10:lindex]}]
    return jsonify(data=data,status=200)


# now creating demo app so we will call api 


def showlyricsnotapi(input_url):

    #linkss=int(input("Enter song number ........"))
    lres=requests.get(input_url)
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

	res=requests.get(url)
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


