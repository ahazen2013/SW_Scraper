import requests
from bs4 import BeautifulSoup
import csv


# scrape names of a given species from Wookieepedia (defaults to humans)
def scrape_species_names(link='/wiki/Category:Humans', species='human'):
    url = 'https://starwars.fandom.com' + link
    f = open('Names/sw_' + species + '_names.txt', 'w', encoding='utf-8')
    while True:
        page = requests.get(url)
        # print(page.status_code)
        # print(page.text)
        soup = BeautifulSoup(page.text, 'html.parser')
        # print(soup.prettify())
        names = soup.find_all(class_='category-page__member-link')
        prev = ''
        for i in names:
            name = i.get('title')
            if '/' not in name and ':' not in name and '1' not in name and '2' not in name and '3' not in name\
                    and '4' not in name and '5' not in name and '6' not in name and '7' not in name and '8' not in name\
                    and '9' not in name and '0' not in name:
                if '(' in name:
                    name = name.split('(')[0][:-1]
                if "'s " in name or "s' " in name:
                    name = name.split("'")[0]
                if prev != name:
                    f.write(name + '\n')
                    prev = name
        next_url = soup.find_all(class_='category-page__pagination-next wds-button wds-is-secondary')
        if not next_url:
            break
        url = next_url[0].get('href')
    f.close()


# scrape basic planet data from Wookieepedia
def scrape_planets():
    url = 'https://starwars.fandom.com/wiki/List_of_planets'
    planets = [['Name', 'Region', 'Sector', 'System', 'Inhabitants', 'Capital City', 'Grid Coordinates']]
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    planet_table = soup.find_all("table", class_='wikitable sortable')
    for table in planet_table:
        for tr in table.tbody.find_all('tr'):
            row = []
            for td in tr.find_all('td'):
                try:
                    if '[' in td.text:
                        row.append(td.text.split('[')[0].strip())
                    else:
                        row.append(td.text.strip())
                except KeyError:
                    pass
            if row:
                planets.append(row)
    print(planets)
    with open(f'sw_planets.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        for i in planets:
            writer.writerow(i)


# scrape names of all members of all species from Wookieepedia
def scrape_all_names():
    url = 'https://starwars.fandom.com/wiki/Category:Individuals_by_species'
    while True:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        species = soup.find_all(class_='category-page__member-link')
        for i in species:
            name = i['title'][9:]
            print(name.lower())
            scrape_species_names(link=i['href'], species=name.lower())
        prev = ''
        next_url = soup.find_all(class_='category-page__pagination-next wds-button wds-is-secondary')
        if not next_url:
            break
        url = next_url[0].get('href')


def scrape_links(link='/wiki/Category:Humans', species='human'):
    url = 'https://starwars.fandom.com' + link
    links = []
    while True:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        names = soup.find_all(class_='category-page__member-link')
        prev = ''
        for i in names:
            name = 'https://starwars.fandom.com' + i.get('href')
            if 'Legends' not in name and 'Category:' not in name:
                links.append(name)
        next_url = soup.find_all(class_='category-page__pagination-next wds-button wds-is-secondary')
        if not next_url:
            break
        url = next_url[0].get('href')
    links = links[1:]
    print(len(links))
    return links


def scrape_characters(links=['https://starwars.fandom.com/wiki/Luke_Skywalker', 'https://starwars.fandom.com/wiki/Leia_Skywalker_Organa_Solo']):
    character_data = ['Name', 'Homeworld', 'Born', 'Died', 'Species', 'Gender', 'Height', 'Mass', 'Hair color',
                      'Eye color', 'Skin color', 'Cybernetics', 'Affiliation(s)', 'Masters', 'Apprentices']
    characters = []
    for i in links:
        print(i)
        character = dict()
        for j in character_data:
            character[j] = None
        url = i
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        species = soup.find_all(class_='pi-item pi-data pi-item-spacing pi-border-color')
        character['Name'] = soup.find("h1").text.strip()
        for k in species:
            try:
                character[k.find(class_='pi-data-label pi-secondary-font').text] = k.find(class_='pi-data-value pi-font').text
            except KeyError:
                pass
        print(character)
        characters.append(character)
    with open(f'sw_characters.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=character_data)
        writer.writeheader()
        for i in characters:
            try:
                writer.writerow(i)
            except ValueError:
                pass


scrape_characters(scrape_links())
