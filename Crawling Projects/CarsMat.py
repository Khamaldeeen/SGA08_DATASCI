import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import time


def CarsMat(url):
    page = requests.get(url)
    container = BeautifulSoup(page.content, 'html.parser')
    cards = container.find_all('div', class_='card-main')
    pri = container.find_all('div', class_='right-side-desktop-card')
    #For the transmission, fuel type and condition
    transmission, condition, engine, lis1 = [], [], [], [] 
    for item1 in cards:
        lis = item1.find('ul', attrs = {'class' : 'card-features'}).text.strip()
        lis1.append(lis)
    for elem in lis1:
        t_cards = elem.split()
        trans = t_cards[1]
        cond = t_cards[-4] +' ' + 'Used'
        eng = t_cards[-1]
        transmission.append(trans)
        condition.append(cond)
        engine.append(eng)
    
    #The year, make and model of the car
    Year, Make, Model = [], [], []
    for item in cards: 
        car_name =  item.find('span', attrs = {'class' : 'ellipses'}).text.strip()
        car_items = car_name.split()
        year = car_items[0]
        make = car_items[1]
        model = car_items[2]
        Year.append(year)
        Make.append(make)
        Model.append(model)
    
    #The price of the cars in Naira 
    Price = []
    for items2 in pri:
        d_pri = items2.find('h2', attrs = {'class' : 'listing-price'}).text.strip()
        d_pri = d_pri[1:]
        fd_pri = int(d_pri.replace(',', ''))
        Price.append(fd_pri)
    return Year, Make, Model, transmission, condition, engine, Price

http = 'https://www.cheki.com.ng/vehicles'
https = [http]
for i in range(2,101):
    child = http + '?page=' + str(i)
    https.append(child)
M_Year, M_Make, M_Model, M_trans, M_cond, M_eng, M_Price = [], [], [], [], [], [], []
for point in https:
    Year1, Make1, Model1, trans1, cond1, eng1, Price1 = CarsMat(point)
    M_Year += Year1
    M_Make += Make1
    M_Model += Model1
    M_trans += trans1
    M_cond += cond1
    M_eng += eng1
    M_Price += Price1


CarData = pd.DataFrame({'Year': M_Year,
                        'Make' : M_Make,
                        'Model' : M_Model,
                        'Transmission' : M_trans,
                        'Condition' : M_cond,
                        'Engine Type' : M_eng,
                        'Price' : M_Price})

CarData.to_csv('Mat Cars.csv')