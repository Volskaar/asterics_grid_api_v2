import csv
import io
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

                # Combine all text elements inside td tags to get rid of the small attribute eg. -> smaller/sie/es lauft
                
                
                person = ' '.join(td_elements[0].stripped_strings)

                indikativ = ' '.join(td_elements[1].stripped_strings)
                konjunktiv1 = ' '.join(td_elements[2].stripped_strings)

                indikativ = indikativ.split()
                konjunktiv1 = konjunktiv1.split()

                if person and person != 'Person':
                    if person and indikativ and konjunktiv1:

                        # Necessary to remove unwanted words
                        if len(indikativ) > 1:
                            # Find position from "," if there is any
                            rest = ' '.join(indikativ[1:])
                            comma_position = rest.find(',')

                            # Extract everything before the comma
                            if comma_position != -1:
                                indikativOnlyVerb = rest[:comma_position]
                            else:
                                indikativOnlyVerb = rest

                        if len(konjunktiv1) > 1:
                            # Find position from "," if there is any
                            rest = ' '.join(konjunktiv1[1:])
                            comma_position = rest.find(',')

                            # Extract everything before the comma
                            if comma_position != -1:
                                konjunktiv1OnlyVerb = rest[:comma_position]
                            else:
                                konjunktiv1OnlyVerb = rest

                        person_list.append(person)
                        indikativ_list.append(indikativOnlyVerb)
                        konjunktiv1_list.append(konjunktiv1OnlyVerb)

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
    tenses = ["PRAESENS", "PRAETERITUM", "PERFEKT", "PLUSQAMPERFEKT", "FUTURI", "FUTURII"]
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

        words_per_tense += 1

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

def convert_to_csv(data):
    # create bytestream for csv output
    # create csv writer instance
    output = io.StringIO()
    writer = csv.writer(output)

    # for every entry in data -> build row in csv
    for item in data:
        value = item["value"]
        tags = ", ".join(item["tags"])
        writer.writerow([value, tags])

    # encode csv and close output bytestream
    csv_data = output.getvalue().encode('utf-8')
    output.close()

    return csv_data


#################################################################################################################

def call_web_scraper(verb, type):
    dataframe = scrape_web(verb)
    data = format_data(dataframe)

    if type == 'json':
        output = convert_to_json(data)
    if type == 'csv':
        output = convert_to_csv(data)

    return (output)
