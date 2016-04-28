from flask import Flask

# Define the WSGI application object
application = Flask(__name__)

# Read the config file
application.config.from_object('config')

# Retrieve updated API config
import requests, json
payload = {'api_key': application.config['API_KEY']}
try:
    r = requests.get('https://api.themoviedb.org/3/configuration', params=payload)
    application.config['API_CONFIG'] = r.json()
    with open('api_config.json', 'w') as outfile:
        json.dump(r.json(), outfile)

except Exception as e:
    print(str(e))
    # Try fallback to local copy of config if necessary
    try:
        with open('api_config.json', 'r') as infile:
            application.config['API_CONFIG'] = json.load(infile)
    except Exception as e:
        print(str(e))

# Retrieve updated genres
try:
    r = requests.get('https://api.themoviedb.org/3/genre/movie/list', params=payload)
    application.config['API_GENRE'] = r.json()
    with open('api_genre.json', 'w') as outfile:
        json.dump(r.json(), outfile)

except Exception as e:
    print(str(e))
    # Try fallback to local copy of genres
    try:
        with open('api_genre.json', 'r') as infile:
            application.config['API_GENRE'] = json.load(infile)
    except Exception as e:
        print(str(e))
    


from app import views