from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import json
import ssl
import urllib
import time

def run():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'} # set the headers
    ssl._create_default_https_context = ssl._create_unverified_context

    data = {}
    #city = input("Please enter the name of a city: ")
    #state = input("Enter the abbreviation of your state: ")
    city = 'washington'
    state = 'dc'
    url = "https://www.ubereats.com/city/" + city.lower() + "-" + state.lower()

    req = Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page, 'html.parser')

    for x in soup.findAll('h3'): # find the name of the restaurant
        x_url = x.find_parent(name='a', href=True)
        print('name of restaurant: ' + x.text)
        a = x.findNext('div', attrs = {'class' : 'ag bk'})
        click_restaurant(x_url['href'])
        if a is not None:
            time = a.findNext('span').text
            time = time.replace("–"," to ")
            pre_rating = x.findNext('div', attrs = {'class' : 'spacer _16'})
            rating = pre_rating.findNext('div')
            key = x.text
           
            data[key] = []
            data[key].append({
                'Delivery Time' : time,
                'Delivery Cost' : a.text,
                'Rating' : rating.text
            })
            print('data key :' + data[key])

def write():
    with open('final_result.json', 'w+', encoding='utf-8') as out: # writing the ginal file
        json.dump(data, out, indent=4, ensure_ascii=False)

def click_restaurant(url):
    restaurant_url = 'https://ubereats.com' + url
    print('restaurant url: ' + restaurant_url)
    req = Request(restaurant_url, headers={'User-Agent' : 'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page, 'html.parser')
    images = soup.find_all('img')
    images_as_strings = []
    for image in images:
        images_as_strings.append(str(image))
        
    for x in images_as_strings:
        img = x.split('"')

        # Get img elements with 7+ attributes
        if len(img) > 7:
            aria_hidden = img[2].lstrip() + img[3]
            if aria_hidden == 'aria-hidden=true':
                alt = img[1]
                src = img[7]
                print('src: ' + src)
                print('alt: ' + alt)

run()
