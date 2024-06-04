from flask import Flask, jsonify, make_response
from flask import request
import webscraper
 
# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
 
@app.route('/', methods=['POST'])
def webscraping():
    verb = str(request.data.decode('UTF-8'))
    output_type = request.args.get('type')

    # create response data
    response_data = webscraper.call_web_scraper(verb, output_type)
    response = make_response(response_data)

    # create response headers depending on datatype
    if output_type == 'json':
        response.headers['Content-Type'] = 'application/json'
    elif output_type == 'csv':
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename=data.csv'

    return response
 
# main driver functions
if __name__ == '__main__':
    app.run()