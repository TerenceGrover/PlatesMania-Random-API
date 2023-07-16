# import matplotlib.pyplot as plt
import cv2
import easyocr
from IPython.display import Image
import urllib.request
import ssl
import matplotlib.pyplot as plt


def coordinates(img):
    reader = easyocr.Reader(['en'])
    # Turn link into readable image
    output = reader.readtext(img)
    cord = output[-1][0]
    x_min, y_min = [int(min(idx)) for idx in zip(*cord)]
    x_max, y_max = [int(max(idx)) for idx in zip(*cord)]
    image = cv2.imread(img)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    return x_min, y_min, x_max, y_max

def download_image(url, filename):
    context = ssl._create_unverified_context()

    # Create a request object with the desired 'User-Agent' header
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
        }
    )

    with urllib.request.urlopen(req, context=context) as u, open('temp_img/'+filename, 'wb') as f:
        f.write(u.read())

# Now you can use this function to download the image:
download_image('https://img03.platesmania.com/230523/o/21622645.jpg','test.jpg')
# print(coordinates('temp_img/test.jpg'))