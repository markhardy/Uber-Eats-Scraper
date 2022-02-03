from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
import ssl
import urllib
import time

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

def run():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'} # set the headers
    ssl._create_default_https_context = ssl._create_unverified_context

    data = {}
    #city = input("Please enter the name of a city: ")
    #state = input("Enter the abbreviation of your state: ")
    city = 'washington'
    state = 'dc'
    url = "https://www.ubereats.com/city/" + city.lower() + "-" + state.lower()

    driver.get(url)
    time.sleep(5)
    
    label = driver.find_element(By.ID, 'location-typeahead-home-input')
    label.send_keys('washington d.c.')
    label.send_keys(u'\ue007')
    
    time.sleep(5)

    url = 'https://www.ubereats.com/feed?diningMode=DINE_IN&pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMldhc2hpbmd0b24lMjIlMkMlMjJyZWZlcmVuY2UlMjIlM0ElMjJDaElKVy1UMld0N0d0NGtSS2wySTFDSkZVc0klMjIlMkMlMjJyZWZlcmVuY2VUeXBlJTIyJTNBJTIyZ29vZ2xlX3BsYWNlcyUyMiUyQyUyMmxhdGl0dWRlJTIyJTNBMzguOTA2NzklMkMlMjJsb25naXR1ZGUlMjIlM0EtNzcuMDM3OTY2NyU3RA%3D%3D'
    driver.get(url)

    buttons = driver.find_elements(By.CLASS_NAME, 'gy')
    for button in buttons:
        print(button.text)


    req = Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
    page = urlopen(req).read()
    print(page)
    soup = BeautifulSoup(page, 'html.parser')
    print('page downloaded')
    
    for x in soup.findAll('h3'): # find the name of the restaurant
        x_url = x.find_parent(name='a', href=True)
        print('name of restaurant: ' + x.text)
        a = x.findNext('div', attrs = {'class' : 'ag bk'})
        click_restaurant_js(x_url['href'])
        if a is not None:
            hours = a.findNext('span').text
            hours = hours.replace("–"," to ")
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

def click_restaurant_js(url):

    restaurant_url = 'https://ubereats.com' + url
    driver.get(restaurant_url)
    time.sleep(8)

    #pictures = driver.find_elements(By.CSS_SELECTOR, 'picture source')
    pictures = driver.find_elements(By.TAG_NAME, 'picture')
    for picture in pictures:
        source = picture.find_element(By.TAG_NAME, 'source')
        srcset = source.get_attribute('srcset')
        print(srcset)
        img = picture.find_element(By.TAG_NAME, 'img')
        alt = img.get_attribute('alt')
        print(alt)


    '''
    pictures = driver.find_elements(By.TAG_NAME, 'ul')

    #pictures = driver.find_elements(By.TAG_NAME, 'picture')
    #pictures = driver.find_elements(By.CSS_SELECTOR, 'picture')
    print(pictures)
    for picture in pictures:
        print(picture)
        picture_child = picture.find_element(By.TAG_NAME, 'li')
        print(picture_child)
        #picture_child = picture.find_element(By.TAG_NAME, 'img')
        #print(picture_child.get_attribute('alt'))
        #print(picture_child.get_attribute('src'))
    '''
    

def click_restaurant(url):
    restaurant_url = 'https://ubereats.com' + url
    print('restaurant url: ' + restaurant_url)
    req = Request(restaurant_url, headers={'User-Agent' : 'Mozilla/5.0'})
    page = urlopen(req).read()
    time.sleep(5)
    soup = BeautifulSoup(page, 'html.parser')
    print(soup.picture)
    #print(soup.prettify())
    pictures = soup.find_all('picture')
    print(pictures)
    for picture in pictures:
        print(picture)
        children = picture.findChildren(recursive=False)
        picture_data = []
        for child in children:
            child_as_string = str(child)
            child_split = child_as_string.split('"')
            if len(child_split) > 3 and child_split[0] == '<source type=':
                src = child_split[3]
                picture_data.append(src)
            elif len(child_split) > 3 and child_split[0] == '<img alt=':
                alt = child_split[1]
                picture_data.append(alt)
            else:
                print('srcset has fewer than 3 elements')
        for data in picture_data:
            print(data)

    

        
    

    '''
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
            else:
                print('no aria')
                print(img)
    '''

run()
