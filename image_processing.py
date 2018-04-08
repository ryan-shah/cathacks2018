from io import BytesIO
import os
import requests

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_url = "https://pixel.nymag.com/imgs/daily/science/2017/03/03/03-black-lives-matter.w710.h473.jpg"

response = requests.get(file_url)
content = BytesIO(response.content).read()

image = types.Image(content=content)

response = client.label_detection(image=image)
labels = response.label_annotations

response2 = client.safe_search_detection(image=image)
result = response2.safe_search_annotation

response3 = client.text_detection(image=image)
result2 = response3.text_annotations


print('Safe Search:')
print(result)

print('Text:')
for text in result2:
    print(text.description)

print('Labels:')
for label in labels:
    print(label.description)
