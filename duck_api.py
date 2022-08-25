import requests
from PIL import Image
from io import BytesIO

url = 'https://random-d.uk/api/randomimg'

r = requests.get(url)
print(r.status_code)

image = Image.open(BytesIO(r.content))
image.show()