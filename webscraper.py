from bs4 import BeautifulSoup
import pandas as pd
import requests


def scrapWeb(verb):
 
    pageToScrape = requests.get(f"https://de.wiktionary.org/wiki/Flexion:{verb}")
    soup = BeautifulSoup(pageToScrape.text, 'html.parser')

    # Find the section for Präsens
    first_section = soup.find('span', {'id': 'Indikativ_und_Konjunktiv'})
    first_table = first_section.find_next('table')  
    
    # Extract all tr elements from the table within the Präsens section
    tr_elements = first_table.find_all('tr')

    person_list = []
    indikativ_list = []
    konjunktiv1_list = []

    # Extract data from tr elements
    for tr in tr_elements:
        td_elements = tr.find_all('td')
        if len(td_elements) >= 3:  # Ensure the row has at least 3 td elements
            person = td_elements[0].get_text(strip=True)
            indikativ = td_elements[1].get_text(strip=True)
            konjunktiv1 = td_elements[2].get_text(strip=True)
            if person != 'Person':  # Make sure person  is not copied
                if person and indikativ and konjunktiv1:  # if everything is filled append it
                    person_list.append(person)
                    indikativ_list.append(indikativ)
                    konjunktiv1_list.append(konjunktiv1)

          # Create a DataFrame using pandas
    data = {'Person': person_list, 'Indikativ': indikativ_list, 'Konjunktiv': konjunktiv1_list}
    df = pd.DataFrame(data)
           
    return df

            


verb= input('Please enter a Verb: ')
table_df = scrapWeb(verb)
print(table_df)

#store output to excel file
#table_df.to_excel('output.xlsx', index=False)