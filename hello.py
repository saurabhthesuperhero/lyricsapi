from flask import Flask,jsonify
import bs4
import requests
app = Flask(__name__)

@app.route('/')
@app.route('/<lstring>')

def hello_world(lstring):
    #lstring='Perfect ed sheeran'
    res=requests.get('https://search.azlyrics.com/search.php?q=%s'%lstring)
    soup=bs4.BeautifulSoup(res.text,'lxml')
    result=soup.find_all('td',{"class":"text-left"})
    i=1
    global x
    x=['0']*10
    y=[]
    col_link=[]

    for link in result [0:5]:
        #print(link.text)
        col_link.append(link.text) 
        y.append(link.find('a').get('href'))
    
        # i=i+1
    string_list="<br>".join(str(i) for i in col_link)

    dictionary=dict(zip(col_link,y))
    return jsonify(dictionary)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)