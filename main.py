from flask import Flask, jsonify, make_response
from flask import request
from flask_cors import CORS
import webscraper
 
# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
 
@app.route('/<word>', methods=['GET'])
def webscraping(word):
    word = word.lower()
    output_type = request.args.get('type')

    # create response data
    response_data = webscraper.call_web_scraper(word, output_type)
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