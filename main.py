from flask import Flask
from flask import request

####################################################################################

import information_handling

####################################################################################
 
# Flask constructor
app = Flask(__name__)

####################################################################################
 
# Routes with associated functions
@app.route('/test')
def test_print_wiktionary_data():
    word = str(request.data)
    return information_handling.get_word_information(word)

####################################################################################
 
# main driver function
if __name__ == '__main__':
    app.run()