import io
import os

# Imports the Google Cloud client library
from google.cloud import vision_v1 as vision
from google.cloud.vision_v1 import types


# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = r"C:\Users\alija\Downloads\drugs.jpg"

with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

image = types.Image(content=content)

response = client.label_detection(image=image)
labels = response.label_annotations

response2 = client.safe_search_detection(image=image)
result = response2.safe_search_annotation
print(result)

print('Labels:')
for label in labels:
    print(label.description)
