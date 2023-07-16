import threading
import requests
import json
import random
from lxml import html

def main():
    global last, obj, stop_event, sem, lock
    last = random.randint(21500000, 22063368)
    obj = {
        'id' : 0,
        'link' : '',
        'country' : ''
    }
    stop_event = threading.Event()
    sem = threading.Semaphore(50)
    lock = threading.Lock()

    with open('countries.json') as f:
        countries = json.load(f)['Country']

    while last > 0 and obj['id'] == 0:
        threads = []
        for country, country_code in countries.items():
            if stop_event.is_set():
                break
            sem.acquire()  # Wait for the semaphore to be released
            t = threading.Thread(target=looper, args=(country_code, country))
            threads.append(t)
            t.start()

        # Wait for threads to finish
        for t in threads:
            t.join()

        if obj['id'] == 0:
            last -= 1

    obj['link'] = get_image_src(obj['link'])
    if obj['link'] is None:
        return main()
    return obj

def looper(country_code, country):
    global last, obj, stop_event, sem

    if stop_event.is_set():
        sem.release()
        return

    link = f'https://platesmania.com/{country_code}/foto{last}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(link, headers=headers)

    if r.status_code == 200 and country_code != 'su':
        with lock:
            if obj['id'] == 0:
                obj['id'] = last
                obj['link'] = link
                obj['country'] = country
                stop_event.set()
                print('Link found!')

    sem.release()  # Release the semaphore when the thread is done

def get_image_src(url):
    print(url)
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    print(response.status_code)
    tree = html.fromstring(response.content)
    try:
        img_src = tree.xpath('//img[@class="img-responsive center-block"]/@src')[0]
        return img_src
    except:
        # Restart
        return None

if __name__ == '__main__':
    print(main())
