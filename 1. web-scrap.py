'''A script intended to iterate through all listings on the Morizon website (initially filtering by the Tricity area). 
The data should be collected in the form of a DataFrame. The script may encounter errors due to changing HTML classes 
on the site from which the data is obtained. However, the results of the original run are saved in a CSV file.'''


from bs4 import BeautifulSoup
import requests
from collections import defaultdict
import pandas as pd
import numpy as np

var = defaultdict(list) #a dictionary which values are predefined treated as lists
info = pd.DataFrame(var) #dataframe for an easier operations on recorcds
counter = 0 #counter will help in implementing unique indexes

main_url = 'https://www.morizon.pl/mieszkania/?ps%5Blocation%5D%5Bmap%5D=1&ps%5Blocation%5D%5Bmap_bounds%5D=54.556625057794,18.908441037799:54.303261388511,18.40058096221'
number_of_pages = 176 #number of pages on morizon at the time of running the script

for i in range(number_of_pages):
    main_page = requests.get(main_url) #opens url #url is being updated at the end of every loop
    main_soup = BeautifulSoup(main_page.text, 'html.parser') #launch of the scrapper


    for link in main_soup.find_all('div', class_='card--bottom-margin'): #loop through every real estate sale offer from the page
        url = 'https://www.morizon.pl/' + link.div.a['href'] #url to an sale offer


        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser') #for every sale offer on the page - we need to launch a scrapper
        
        price = soup.find('span', class_='Lh6ScZ') 
        price_per_meter = soup.find('span', class_='OgttQD')
        if price is not None: #filtering the offers that include the price (the main goal of the project is price prediction therefore the price variable is necessary)

            rooms = soup.find('span', class_='Fduk4D').text[3]
            number_of_floors = soup.find_all('span', class_='Fduk4D')[2].text
            location = soup.find_all('h2', class_='_9hyrtb')
            city_district = location[1].text.split(', ') #saving variables such as city, district and street in a list
            info_key = soup.find_all('div', class_='sACAYP YyH0Zt') #additional amenities - names
            info_value = soup.find_all('div', class_='sACAYP e6zNrk') #additional amenities - values

            info.loc[counter, 'id'] = counter #unique id
            info.loc[counter, 'Cena'] = price.text #price
            if price_per_meter is not None:
                info.loc[counter, 'Cena/metr'] = price_per_meter.text #column containng a price per squared meter
            else:
                info.loc[counter, 'Cena/metr'] = np.nan
            if rooms is not None:
                info.loc[counter, 'Pokoje'] = rooms #column containing a number of rooms
            else:
                info.loc[counter, 'Pokoje'] = np.nan
            info.loc[counter, 'Miasto'] = city_district[0]  #column containing a city name
            if len(city_district) > 1:
                info.loc[counter, 'Dzielnica'] = city_district[1] #column containing a district name
            else:
                info.loc[counter, 'Dzielnica'] = np.nan
            if len(city_district) > 2:
                info.loc[counter, 'Ulica'] = city_district[2] #column containing a street name
            else:
                info.loc[counter, 'Ulica'] = np.nan

            for i in range(len(info_key)):
                info.loc[counter, info_key[i].text] = info_value[i].text #additional amenities

            if number_of_floors[3:9] == 'parter': #number_of_floors has a following formula: ' * ground floor ' or ' * floor 1/5' or ' * floor 1'
                info.loc[counter, 'Piętro'] = 0 #if 'ground floor' in sale offer -> floor = 0
                info.loc[counter, 'Liczba pięter'] = np.nan #in case of a ground floor, Morizon doesn't show the max floors of the bulding therefore -> np.nan - later we will change np.nan for the mean of the whole dataset
            elif len(number_of_floors) < 12: #if len < 12 - there is no disclaimed number of floors in the building therefore I assume that the flat is located at the highest floor
                info.loc[counter, 'Piętro'] = number_of_floors[10]
                info.loc[counter, 'Liczba pięter'] = number_of_floors[10]
            elif len(number_of_floors) >= 12: #if len > 12 sale offer disclaims floor and the total number of floors in the building
                info.loc[counter, 'Piętro'] = number_of_floors[10]
                info.loc[counter, 'Liczba pięter'] = number_of_floors[12]

            counter += 1 #unique index has to increment at the end of the loop
        print(info) #result check


    #end of the loop for the sale offers atthe current page

    #time to find URL to the next page containing sale offers
    next_url = main_soup.find('div', class_='E0A3rM').a['href']
    main_url = 'https://www.morizon.pl/' + next_url #url update and looping through another sale offers page


#saving results into csv file
info.to_csv('C:/Users/Maciej/Documents/projekt_studia/real_estate/final_result.csv')