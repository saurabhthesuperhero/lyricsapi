from flask import Flask,jsonify
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
    y=[]
    global col_link 
    col_link=[]

    for link in result [0:5]:
        #print(link.text)
        
        temp=(str(link.text[3:]).find('\n'))#ignoring first \n and will stop after second \n
        # -creepy but good
       # print(link.text[3:temp+3])

        
        col_link.append(link.text[3:temp+3]) 
        y.append(link.find('a').get('href'))

  
    
        # i=i+1
    string_list="<br>".join(str(i) for i in col_link)

    dictionary=dict(zip(col_link,y))
    return str(dictionary)
    
app.run(debug=True)

