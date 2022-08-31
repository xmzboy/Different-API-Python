import requests
import json

url = 'http://dog-api.kinduff.com/api/facts?number=5'

r = requests.get(url)

req_dct = json.loads(r.text)

print(*req_dct['facts'], sep='\n\n')
