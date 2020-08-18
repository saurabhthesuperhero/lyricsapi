from flask import Flask,jsonify,render_template
import bs4
import requests
app = Flask(__name__)

@app.route('/')
def ello():
	return 'Lyrics API'

@app.route('/search=<lstring>')
def hello_world(lstring):
    #lstring='Perfect ed sheeran'
    res=requests.get('https://search.azlyrics.com/search.php?q=%s'%lstring,timeout=5)
    soup=bs4.BeautifulSoup(res.text,'lxml')
    result=soup.find_all('td',{"class":"text-left"})
    data=[]
    for link in result [0:5]:
        
        temp=(str(link.text[3:]).find('\n'))#ignoring first \n and will stop after second \n
        data.append({"name":link.text[3:temp+3],"link":link.find('a').get('href')})
    return jsonify(data=data,status=200)
    


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
	return render_template('lyricui.html',listlyric=listlyrics)


