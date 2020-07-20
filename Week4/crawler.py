import requests 
import numpy as np 
import pandas as pd 
import time 
from bs4 import BeautifulSoup


def LagProp(url):
    req = requests.get(url)
    page = BeautifulSoup(req.text, 'lxml')
    
    #Interested features storage
    Title = page.select('.wp-block-content > a > h4')
    Loc = page.select('.wp-block-content > address > strong')
    Price = page.select('.wp-block-content > span > .price')


    #Room numbers and Name of house
    Type, Rooms = [], []
    for i in Title:
        con = i.get_text().split()
        bd = con[0]
        house_type = con[2:4]
        f_house = ' '.join(house_type)
        Type.append(f_house)
        Rooms.append(bd)

    #LLocation of houses by district
    Location = []
    for i in Loc:
        item = i.get_text().split()
        item = item[-2]
        item = item.replace(',', '')
        Location.append(item)

    #Amount of houses in Naira 
    Amount = []
    for i, item in enumerate(Price):
        obj = item.get_text()
        if len(obj) > 2:
            obj = obj.replace(',', '')
            try:
                obj = int(obj)
            except ValueError:
                obj = str(obj)     
            Amount.append(obj)

    return Type, Rooms, Location, Amount


#creating an iterable lists that will be passed into the functions to change the current page containing 100 pages

base = 'https://nigeriapropertycentre.com/for-rent/houses/lagos/showtype'
urls = []

for i in range(2, 100):
    addr = base + '?page=' + str(i) 
    urls.append(addr)

#Creating a for loop to iterate the items stored in urls and run our function that will fetch the properties
a_type, a_rooms, a_Loc, a_price = [], [], [], []

for li_ in urls:
    Type_1, Rooms_1, Location_1, Price_1 = LagProp(li_)
    a_type += Type_1
    a_rooms += Rooms_1
    a_Loc += Location_1
    a_price += Price_1


#parsing the stored lists into a pandas dataframe

data = pd.DataFrame.from_dict({'Type': a_type,
                                'Rooms': a_rooms,
                                'Location' : a_Loc,
                                'Price' : a_price})

#Storing the Dataframe created to a csv file
data.to_csv('Lagos Rent Amount.csv')


