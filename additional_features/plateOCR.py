# import matplotlib.pyplot as plt
import cv2
import easyocr
import urllib.request
import ssl
import matplotlib.pyplot as plt
import random
from math import floor
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()
path = os.getenv('PATH_TEMP_IMG')



def blur(y_min, y_max, x_min_min, x_min, image):
    roi = image[y_min:y_max, x_min_min:x_min]
    if is_blue_dominant(roi):
        # Apply blur
        blurred_roi = cv2.GaussianBlur(roi, (99,99), 30)
        image[y_min:y_max, x_min_min:x_min] = blurred_roi
    return image

def coordinates(url):
    img = download_image(url)
    img = cv2.imread(img)

    reader = easyocr.Reader(['en'])
    output = reader.readtext(img)
    cord = output[-1][0]
    x_min, y_min = [int(min(idx)) for idx in zip(*cord)]
    x_max, y_max = [int(max(idx)) for idx in zip(*cord)]
    range_y = y_max - y_min
    y_min = floor(y_min + 0.05 * range_y)
    y_max = floor(y_max - 0.05 * range_y)
    x_min_min = floor(x_min - (x_max - x_min) * 0.1)

    return x_min, x_min_min, y_min, y_max, img

def is_blue_dominant(img):
    b, g, r = cv2.split(img)
    return np.mean(b) > np.mean(g)*1.25 and np.mean(b) > np.mean(r)*1.25

def download_image(url):
    context = ssl._create_unverified_context()
    filename = 'test' + str(random.randint(0,10000)) + '.jpg'

    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
        }
    )

    with urllib.request.urlopen(req, context=context) as u, open(path + filename, 'wb') as f:
        f.write(u.read())
    return path + filename

def write_image(image, filename):
    cv2.imwrite(path + 'blured_' + filename, image)

def main(url):
    x_min, x_min_min, y_min, y_max, image = coordinates(url)
    image = blur(y_min, y_max, x_min_min, x_min, image)
    write_image(image, 'test.jpg')