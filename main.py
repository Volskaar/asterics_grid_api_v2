from flask import Flask
from flask import request
import webscraper
 
# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
 
@app.route('/', methods=['POST'])
def webscraping():
    # get request body as string
    # get request params
    verb = str(request.data.decode('UTF-8'))
    output_type = request.args.get('type')

    # create response data
    response = webscraper.call_web_scraper(verb, output_type)

    # set headers depending on data type
    if output_type == 'json':
        response.headers['Content-Type'] = 'application/json'
    elif output_type == 'csv':
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename=data.csv'

    return response
 
# main driver function
if __name__ == '__main__':
    app.run()