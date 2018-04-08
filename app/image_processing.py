from io import BytesIO
import os
import requests

# Imports the Google Cloud client library
from google.cloud import vision_v1 as vision
from google.cloud.vision_v1 import types

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\Users\alija\Downloads\google_auth.json"

def analyzeImage(url):
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # get image binary
    response = requests.get(url)
    content = BytesIO(response.content).read()
    image = types.Image(content=content)

    # check labels
    l_response = client.label_detection(image=image)
    labels = l_response.label_annotations

    # check safe search
    s_response = client.safe_search_detection(image=image)
    safe_search = s_response.safe_search_annotation

    # check OCR detection
    o_response = client.text_detection(image=image)
    OCR = o_response.text_annotations

    result = {"label":"", "safe_search":{}, "ocr":""}

    result["label"] = [label.description for label in labels]
    result["safe_search"]["adult"] = safe_search.adult
    result["safe_search"]["spoof"] = safe_search.spoof
    result["safe_search"]["medical"] = safe_search.spoof
    result["safe_search"]["violent"] = safe_search.violence
    result["ocr"] = [text.description for text in OCR]
    """
    print('Safe Search:')
    print(result['safe_search'])

    print('Text:')
    print(result['ocr'])

    print('Labels:')
    print(result["label"])
    """
    return result

def checkImageData(data):
    for key in data['safe_search']:
        if data['safe_search'][key] >= 3:
            return "Image flagged for " + key + " content"

    bad_image_tags = [line.rstrip('\n') for line in open(r"C:\Users\alija\Downloads\image_tags.txt")]
    bad_text_tags = [line.rstrip('\n') for line in open(r"C:\Users\alija\Downloads\text_tags.txt")]
    for label in data["label"]:
        if label in bad_image_tags:
            return "Image flagged for '" + label + "'"
    for text in data["ocr"]:
        if text in bad_text_tags:
            return "Image found to contain the inappropriate text '" + text + "'"
    return ''
