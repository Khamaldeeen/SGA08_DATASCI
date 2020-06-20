#web scraping with BS4

import requests
from bs4 import BeautifulSoup
import pandas as pd

page = requests.get('https://cars.mitula.com.ng/searchC/fuel-Petrol/q-Lagos-Toyota')

soup = BeautifulSoup(page.content, 'html.parser')

page_list = soup.find('div', class_= 'adsList mc')

list_item = page_list.find_all('div', class_="lis_ting_Ad")

for car in list_item:
    car_list = car.find('h4').text
    names = [car_list]
    bucket = names[0].split()
    make = bucket[0]
    model = bucket[1]
    year = bucket[2]
    #trans = bucket[3]
    

    car_price = car.find('div', class_='adPrice').find('div').text
    
    print(make, model, year, car_price)
    #print(car_price)

