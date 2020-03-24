from flask import Flask, jsonify
import json
import requests

# Creates an instance of the flask class. Acts as a placeholder for the current module, app.py.
app = Flask(__name__)


@app.route('/get_starships_by_hyperdrive_rating_local', methods=['GET'])
def get_starships_by_hyperdrive_rating_local():
    """
    :return: Loads a sorted local json with data already grabbed from the reference api and returns jsonified data.
    """
    file = open('starship_data.json', 'r', encoding='utf-8-sig')
    data = file.read()
    file.close()
    json_data = json.loads(data)
    return jsonify(json_data), 200


@app.route('/', methods=['GET'])
def get_starships_by_hyperdrive_rating_live():
    """
    :return: Grabs up-to-date data from the reference API, then sorts and returns a jsonified version of the data. This
    is slower than the local version, as it relies on the speed of the reply from the data external data source. End
    point is index so it loads when the test server loads, but normally I would have the app and route match as the
    above function.
    """

    master_starship_dictionary = {
        'starships': [
        ],
        'starships_unknown_hyperdrive': [
        ]
    }

    # A recursive function for grabbing all the page data.
    def recursive_page_grabber(api_url, output_dict):
        """
        :param api_url: A reference API for grabbing the most up-do-date data
        :param output_dict: A dictionary for the output to save data in our preferred format.
        :return: Returns itself until there is no "next" key in the API response.
        """
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

    # Grabbing up-to-date data
    recursive_page_grabber('https://swapi.co/api/starships/', master_starship_dictionary)

    # Sort the output
    master_starship_dictionary['starships'] = sorted(master_starship_dictionary['starships'],
                                                     key=lambda k: k['hyperdrive'])
    return jsonify(master_starship_dictionary), 200


if __name__ == '__main__':
    app.run(debug=True)