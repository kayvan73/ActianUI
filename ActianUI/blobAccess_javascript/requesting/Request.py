import json
import requests
import base64
import imageio

response = requests.get('http://127.0.0.1:5000/api/imgBytes')
json_data = json.loads(response.text)
print(json_data['results'][0])
#print(response.text)
#print(type(response.text))
#if (isinstance(json_data['results'][1], 

#uncomment the below lines if you want to verify python test of base64
#decoded = base64.b64decode(json_data['results'][1])
#im = imageio.imread(decoded)
#saved = imageio.imwrite('NOBYTES.jpg', im, format='jpg')
