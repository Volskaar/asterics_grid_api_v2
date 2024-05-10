import requests 
# general request side: https://german-verbs-api.onrender.com/german-verbs-api

url = 'http://localhost:3000/german-verbs-api'
params = {
    'verb': 'kaufen',
    'tense': 'PERFEKT'
}

# main loop - always true
while(1):
    print('//////////////////////////////////////////////////////////////////')
    inputVerb = input("Please insert your verb here: ")
    inputTense = input("Please insert your desired tense of the verb: ")

    # fill params
    # alternative paramter: 'verbCase': 'DATIVE'
    params = {
        'verb': inputVerb,
        'tense': inputTense
    }
    
    # send request to localhost
    response = requests.get(url, params=params)

    if response.status_code == 200:
        print('Response body:', response.text)
    else:
        print('Error:', response.status_code)

