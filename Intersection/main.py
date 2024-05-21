from flask import Flask, request, jsonify
import requests
from collections import OrderedDict

app = Flask(__name__)


#////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////

def fetch_conjugations(url, verb):
    # Parameters for the API request
    params = {"verb": verb}

    # Send a GET request to the API
    response = requests.get(url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Get the JSON data from the response
        json_data = response.json()
        return json_data
    else:
        return None


#////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////

def process_conjugations(data):
    output = []

    # Iterate over the tense-conjugations pairs in the JSON data
    for tense, conjugations in data["data"].items():
        # Check if the tense is one of the target tenses
        if tense in ["PRASENS", "PRATERITUM", "FUTUR1", "FUTUR2", "PERFEKT", "PLUSQUAMPERFEKT"]:
            tense_translation = {
                "PRASENS": "Präsens",
                "PRATERITUM": "Präteritum",
                "FUTUR1": "Futur 1",
                "FUTUR2": "Futur 2",
                "PERFEKT": "Perfekt",
                "PLUSQUAMPERFEKT": "Plusquamperfekt",
            }

            # Initialize an empty list to store conjugations for each person
            conjugation_list = []

            # Iterate over the person-conjugation pairs
            for person, words in conjugations.items():
           
                pronoun_translation = {
                    "S1": "1. Person Singular",
                    "S2": "2. Person Singular",
                    "S3": "3. Person Singular",
                    "P1": "1. Person Plural",
                    "P2": "2. Person Plural",
                    "P3": "3. Person Plural",
                }

                pronoun = {
                    "S1": "ich",
                    "S2": "du",
                    "S3": "er/sie/es",
                    "P1": "wir",
                    "P2": "ihr",
                    "P3": "sie",
                }

                # Construct the conjugation string
                   # Construct the conjugation string
                conjugation = {
                    "Person": pronoun_translation[person],
                    "Indikativ": f"{pronoun[person]} {' '.join(words)}"
                }
                # Add the conjugation to the conjugation list
                conjugation_list.append(conjugation)

            # Create a tense-output pair and add it to the output list
            tense_output = {
                tense_translation[tense]: conjugation_list
            }
            output.append(tense_output)

    return output


#////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////

@app.route("/conjugate", methods=["GET"])

def conjugate_verb():
    #provide verb in the header
    verb = request.args.get("verb")
    if not verb:
        return jsonify({"error": "Please provide a verb parameter"}), 400

    #provide url to fetch data
    url = "http://localhost:3000/german-verbs-api"
    data = fetch_conjugations(url, verb)
    
    #process the ouput in a nice format
    if data:
        output = process_conjugations(data)
        return jsonify(output)
    else:
        return jsonify({"error": "Failed to fetch conjugations"}), 500

if __name__ == "__main__":
    app.run(debug=True)
