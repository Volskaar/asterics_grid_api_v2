from bs4 import BeautifulSoup
import pandas as pd
import requests


def scrapWeb(verb):
 
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
    


verb= input('Please enter a Verb: ')
table_df = scrapWeb(verb)
print(table_df)

#store output to excel file
#table_df.to_excel('output.xlsx', index=False)