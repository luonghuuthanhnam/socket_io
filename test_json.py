import json

with open('userdata.json',encoding="utf8") as json_file:
    data = json.load(json_file)
    for p in data['UsersData']:
        print('Name: ' + p['name'])
        print('id: ' + p['id'])
        print('Age: ' + p['age'])
        print('')