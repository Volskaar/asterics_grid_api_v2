from bs4 import BeautifulSoup
import pandas as pd
import requests
import json

def scrape_web(verb):
    pageToScrape = requests.get(f"https://de.wiktionary.org/wiki/Flexion:{verb}")
    soup = BeautifulSoup(pageToScrape.text, 'html.parser')

    # Find the initial section for Indikativ und Konjunktiv
    first_section = soup.find('span', {'id': 'Indikativ_und_Konjunktiv'})
    if not first_section:
        return pd.DataFrame()  # Return empty DataFrame if the section is not found

    tables = first_section.find_all_next('table')  

    person_list = []
    indikativ_list = []
    konjunktiv1_list = []

    futur2_found = False  # Flag to indicate if Futur II table has been found

    for table in tables:
        tr_elements = table.find_all('tr')

        for tr in tr_elements:
            td_elements = tr.find_all('td')
            if len(td_elements) >= 3:  # Ensure the row has at least 3 td elements

                # Watch out for  "er/sie/es" and add additional space btw person and verb 
                for td in td_elements:
                    if 'er/sie/es' in td.text:
                        td.string = td.text.replace('er/sie/es', 'er/sie/es ')

                person = td_elements[0].get_text(strip=True)
                indikativ = td_elements[1].get_text(strip=True)
                konjunktiv1 = td_elements[2].get_text(strip=True)
                if person and person != 'Person':  # Make sure person is not copied if it's the header
                    if person and indikativ and konjunktiv1:  # if everything is filled append it
                        person_list.append(person)
                        indikativ_list.append(indikativ)
                        konjunktiv1_list.append(konjunktiv1)
        
        # Check if the table contains "Futur II"
        if any("Futur II" in td.get_text() for td in table.find_all('td')):
            futur2_found = True
        
        if futur2_found:
            break

    # Create a DataFrame using pandas
    data = {'Person': person_list, 'Indikativ': indikativ_list, 'Konjunktiv': konjunktiv1_list}
    df = pd.DataFrame(data)
     
    return df

#################################################################################################################

def format_data(dataframe):
    result = []
    tenses = ["PRAESENS","PRAETERITUM","PERFEKT","PLUSQAMPERFEKT","FUTURI","FUTURII"]
    tense_cnt = 0
    words_per_tense = 0

    for index, row in dataframe.iterrows():
        # convert row to dictionary
        row_dict = row.to_dict()

        # extract person
        person = row_dict['Person']

        # create person tag
        tag_person = ""
        if "1." in person:
            tag_person = "1.PERS"
        elif "2." in person:
            tag_person = "2.PERS"
        elif "3." in person:
            tag_person = "3.PERS"

        # tenses tag
        tag_tense = ""
        tag_tense = tenses[tense_cnt]

        words_per_tense += 1;

        if words_per_tense == 6:
            words_per_tense = 0
            tense_cnt += 1

        
        # create plural tag
        tag_plural = ""
        if "Plural" in person:
            tag_plural = "PLURAL"

        tag_negation = ""
        if "nicht" in row_dict['Indikativ']:
            tag_negation = "NEGATION"
        
        # build output structure
        if not tag_plural and not tag_negation:
            entry = {
                "value": row_dict['Indikativ'],
                "tags": [tag_person, tag_tense]
            }
        elif not tag_plural:
            entry = {
                "value": row_dict['Indikativ'],
                "tags": [tag_person, tag_tense, tag_negation]
            }
        elif not tag_negation:
            entry = {
                "value": row_dict['Indikativ'],
                "tags": [tag_person, tag_tense, tag_plural]
            }
        else:
            entry = {
                "value": row_dict['Indikativ'],
                "tags": [tag_person, tag_tense, tag_plural, tag_negation]
            }

        result.append(entry)
    
    return result

#################################################################################################################

def convert_to_json(data):
    return json.dumps(data, ensure_ascii=False, indent=2)

#################################################################################################################

def call_web_scraper(verb):
    dataframe = scrape_web(verb)
    data = format_data(dataframe)
    json = convert_to_json(data)
    return(json)
