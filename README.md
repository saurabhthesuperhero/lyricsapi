
# Lyrics Api -Public APi


## What it can do ?

 - Give list of songs to your query
 - will give json of selected song lyrics

## Demo :
Click to have fun : https://apilyrics.herokuapp.com/demo

## How to use?
Call : https://apilyrics.herokuapp.com/search=query
where query can be: song name, artist name, album name.
## Sample Python Code:

    import requests,json
    def callapi(query):
    	url='http://apilyrics.herokuapp.com/search='+query
    	res=requests.get(url)
    	res=json.loads(res.content)
    	print(res)
    	
    callapi("blank space")
   
   It will Return response within milliseconds with status=200.

## How I made it:

 - Python
 - Flask
 - Html,CSS
 - AJAX,JS
 
