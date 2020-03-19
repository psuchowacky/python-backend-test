import requests
import json

master_starship_dictionary = {
    'starships': [
    ],
    'starships_unknown_hyperdrive': [
    ]
}

def recursive_page_grabber(api_url, output_dict):
    api_url = api_url
    api_data = json.loads(requests.get(api_url).text)
    for result in api_data['results']:
        starship_data = {'name': result['name']}
        if result['hyperdrive_rating'] == 'unknown':
            output_dict['starships_unknown_hyperdrive'].append(starship_data)
        else:
            starship_data['hyperdrive'] = result['hyperdrive_rating']
            output_dict['starships'].append(starship_data)
    if api_data['next'] is not None:
        return recursive_page_grabber(api_data['next'], output_dict)

recursive_page_grabber('https://swapi.co/api/starships/', master_starship_dictionary)

master_starship_dictionary['starships'] = sorted(master_starship_dictionary['starships'], key=lambda k: k['hyperdrive'])

with open('starship_data.json', 'w', encoding='utf-8-sig') as WriteFile:
    json.dump(master_starship_dictionary, WriteFile, ensure_ascii=False, indent=4)
