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
    # this url format is not working. must hard code to dc and dine in
    url = "https://www.ubereats.com/city/" + city.lower() + "-" + state.lower()
    #url = "https://www.ubereats.com/feed?diningMode=DINE_IN&pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMldhc2hpbmd0b24lMjIlMkMlMjJyZWZlcmVuY2UlMjIlM0ElMjJDaElKVy1UMld0N0d0NGtSS2wySTFDSkZVc0klMjIlMkMlMjJyZWZlcmVuY2VUeXBlJTIyJTNBJTIyZ29vZ2xlX3BsYWNlcyUyMiUyQyUyMmxhdGl0dWRlJTIyJTNBMzguOTA2NzklMkMlMjJsb25naXR1ZGUlMjIlM0EtNzcuMDM3OTY2NyU3RA%3D%3D"

    req = Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page, 'html.parser')

    for x in soup.findAll('h3'): # find the name of the restaurant
        x_url = x.find_parent(name='a', href=True)
        print('name of restaurant: ' + x.text)
        a = x.findNext('div', attrs = {'class' : 'ag bk'})
        #print('?: ' + a)
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
    #change variable names?
    req = Request(restaurant_url, headers={'User-Agent' : 'Mozilla/5.0'})
    page = urlopen(req).read()
    print(page)
    soup = BeautifulSoup(page, 'html.parser')
    print(soup.findAll('li', class_='gb gc'))

    for x in soup.findAll('li', class_='gb gc'):
        print('open li')
        print('x: ' + x.text)
        a = x.findNext('div', attrs = {'class' : 'gd ge fl ej ax'})
        if a is not None:
            print('a: ' + a.text)
            category = a.text
            image = a.findNext('img', src=True)
            image_url = image['src']
            dish = a.findNext('span').text
            price = a.findNext('span').text

            #upper case?
            print(category)
            print(image_url)
            print(dish)
            print(price)
    
run()
