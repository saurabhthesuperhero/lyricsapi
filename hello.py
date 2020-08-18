from flask import Flask,jsonify
import bs4
import requests
app = Flask(__name__)

@app.route('/')
def ello():
	return 'hello'
@app.route('/<lstring>')

def hello_world(lstring):
    #lstring='Perfect ed sheeran'
    res=requests.get('https://search.azlyrics.com/search.php?q=%s'%lstring,timeout=8)
    soup=bs4.BeautifulSoup(res.text,'lxml')
    result=soup.find_all('td',{"class":"text-left"})
    y=[]
    global col_link 
    col_link=[]

    for link in result [0:5]:
        #print(link.text)
        col_link.append(link.text) 
        y.append(link.find('a').get('href'))
    
        # i=i+1
    string_list="<br>".join(str(i) for i in col_link)

    dictionary=dict(zip(col_link,y))
    return jsonify(col_link)

