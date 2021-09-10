import requests
import json
from PIL import Image

# url = "https://wordsapiv1.p.rapidapi.com/words/python/definitions"

# headers = {
#     'x-rapidapi-host': "wordsapiv1.p.rapidapi.com",
#     'x-rapidapi-key': "c83e7d750dmshcde9415b4bd29b2p1fdd2ajsnc5945f3ce5bb"
#     }

# response = requests.request("GET", url, headers=headers)

# # print(response.text)
# data = json.loads(response.text)
# print(data['definitions'])
# for el in data['definitions']:
# 	print(el['definition'])

def image_resize(img, h_new):
	w, h = img.size
	w_new = int(w * h_new / h)
	return img.resize((w_new, h_new))


image_back = Image.new('RGB', (500, 500), (255, 255, 255))
image_front = Image.open('image.png')
image_front = image_resize(image_front, 100)

image_back.paste(image_front)
image_back.save('image_back.png')

image_front.close()
image_back.close()


url = "https://weatherapi-com.p.rapidapi.com/forecast.json"

querystring = {"q":"almaty","days":"2"}

headers = {
    'x-rapidapi-host': "weatherapi-com.p.rapidapi.com",
    'x-rapidapi-key': "c83e7d750dmshcde9415b4bd29b2p1fdd2ajsnc5945f3ce5bb"
}

response = requests.request("GET", url, headers=headers, params=querystring)
data = json.loads(response.text)

print(data['forecast']['forecastday'][1]['day']['condition'])

response = requests.get("https:" + data['forecast']['forecastday'][1]['day']['condition']['icon'])
with open('image_icon.png', 'wb') as f:
	f.write(response.content)


image_back = Image.new('RGB', (500, 500), (255, 255, 255))
image_front = Image.open('image_icon.png')
image_front = image_resize(image_front, 100)

image_back.paste(image_front, image_front.split()[-1])
image_back.save('image_back.png')

image_front.close()
image_back.close()