import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.cheki.com.ng/vehicles/mercedes-benz?page=4'

source = requests.get(url).text
soup = BeautifulSoup(source, 'lxml')

mainPage = soup.find('ul', attrs={'class':'listing-unit__container'})

_mainPage = mainPage.find_all('div', attrs = {'class': 'right-card-part-container'})

with open('CarsMat.csv', mode='w', newline='') as outputFile:
    carPrices = csv.writer(outputFile, delimiter=',', quotechar= '"', quoting = csv.QUOTE_MINIMAL)
    carPrices.writerow(['Name', 'Model', 'Year', 'Location', 'Transmission', 'Condition', 'Color', 'Amount'])


    for card in _mainPage:
        car_nameR = card.find('span', attrs = {'class' : 'card-header'})
        car_name =  car_nameR.find('span', attrs = {'class' : 'ellipses'}).text.strip()
        car_items = car_name.split()
        year = car_items[0]
        make = car_items[1]
        model = car_items[2]

        car_price = card.find('h2', attrs = {'class' : 'listing-price'}).text.strip()
        currency = car_price[:1]
        price = car_price[1:]

        features = card.find('ul', attrs = {'class' : 'card-features'})
        lists = features.find_all('li', attrs = {'class' : 'ellipses'})
        color = lists[2].text.strip()
        location = lists[0].text.strip()
        transmission = lists[1].text.strip()
        cond = lists[3].text.strip()
        carPrices.writerow([make, model, year, location, transmission, cond, color, price])