import requests
import re
from bs4 import BeautifulSoup

def find_section(html_doc, id_substring):
    sections = html_doc.find_all('section')
    p = re.compile(f'.*?{id_substring}.*')
    return [x for x in sections if p.match(x.get('id') or "")][0]

def parse_lift_data(lift_elm):
    lift_name = lift_elm.find('div', class_="text").text.strip()
    lift_status = lift_elm.find('img').get('alt')

    return {
        "name": lift_name,
        "status": lift_status,
    }

def parse_trail_data(trail_elm):
    trail_name = trail_elm.find('div', class_="text").text.strip()
    trail_status = trail_elm.find('img').get('alt')

    return {
        "name": trail_name,
        "status": trail_status,
    }

def parse_lifts_data(html_doc):
    lift_section = find_section(html_doc, "conditions_lift")
    lifts = lift_section.find_all('div', class_='breakInsideAvoid')

    lifts_data = []

    for lift in lifts:
        lifts_data.append(parse_lift_data(lift))

    return lifts_data

def parse_trails_data(html_doc):
    trail_section = find_section(html_doc, "conditions_trail")
    trails = trail_section.find_all('div', class_='breakInsideAvoid')

    trails_data = []

    for trail in trails:
        trails_data.append(parse_trail_data(trail))

    return trails_data

def scrape_sunday_river_data():
    vgm_url = 'https://www.sundayriver.com/mountain-report'
    html_text = requests.get(vgm_url).text
    html_doc = BeautifulSoup(html_text, 'html.parser')

    return {
        "lifts": parse_lifts_data(html_doc),
        "trails": parse_trails_data(html_doc),
    }
