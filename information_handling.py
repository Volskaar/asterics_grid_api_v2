import json

####################################################################################

def get_word_information(word):
    input = 'data_german.json'

    # open data dump in read mode
    with open(input, 'r', encoding='utf-8-sig') as dump:
        data = json.load(dump)

    # iterate over data to see if match is found
    print("Word: " + word)
    for object in data:
        print(object.get('word' + '\n'))
        if object.get('word') == word:
            return object
        
    return "nix"

