import json

input = 'data.json'
output = 'words.json'

def clean_data_dump():
    try:
        # get 
        # Open the input file and load data
            # data contained in original file as multiple objects in lines
        with open(input, 'r', encoding='utf-8-sig') as f:
            data = []
            for line in f:
                try:
                    obj = json.loads(line)
                    data.append(obj)
                except json.JSONDecodeError:
                    print(f"Ignoring invalid JSON data: {line.strip()}")

        # Filter data to keep only german verbs
            # lang_code = de
            # pos = verb
        filtered_data = [obj.get('word') for obj in data if obj.get('lang_code') == 'de' and obj.get('pos') == 'verb']

        # Write filtered data to output file
            # indent=2 for json readability
            # ensure_ascii=false to allow german umlaute
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(filtered_data, f,indent=2, ensure_ascii=False)

        return True
    except RuntimeError:
        print(RuntimeError)
        return False