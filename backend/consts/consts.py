import json

UA_CITIES = []
with open('consts/files/ua_cities.json', 'r') as file:
    UA_CITIES = json.loads(file.read())
