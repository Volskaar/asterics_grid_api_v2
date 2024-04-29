from flask import Flask
from flask import request

####################################################################################

import data_processing

####################################################################################
 
# Flask constructor
app = Flask(__name__)

####################################################################################
 
# Routes with associated functions
@app.route('/test')
def test_print_wiktionary_data():
    if data_processing.clean_data_dump():
        return "Nice shit"
    else:
        return "Dipshit"

####################################################################################
 
# main driver function
if __name__ == '__main__':
    app.run()