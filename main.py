from flask import Flask
from flask import request
import webscraper
 
# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
 
@app.route('/', methods=['POST'])
def webscraping():
    verb = str(request.data.decode('UTF-8'))
    print(verb)
    response_json = webscraper.call_web_scraper(verb)
    return response_json
 
# main driver function
if __name__ == '__main__':
    app.run()