'''Skrypt mający przechodzić po wszystkich ogłoszeniach ze strony morizon (wstępnie filtrując po trójmieście). Dane mają być zebrane w postaci DataFrame,
skrypt może wywoływać błąd ze względu na zmieniające się klasy html na stronie z której pozyskiwano dane, jednak wyniki oryginalnego uruchomienia zapisane są w pliku csv'''


from bs4 import BeautifulSoup
import requests
from collections import defaultdict
import pandas as pd
import numpy as np

var = defaultdict(list) #stworzenie słownika, który domyślnie traktuje nowo tworzoną zmienną jako listę
info = pd.DataFrame(var) #dataframe dla łatwiejszej operacji na rekordach
counter = 0 #counter posłuży jako unikalne id rekordów

main_url = 'https://www.morizon.pl/mieszkania/?ps%5Blocation%5D%5Bmap%5D=1&ps%5Blocation%5D%5Bmap_bounds%5D=54.556625057794,18.908441037799:54.303261388511,18.40058096221'
number_of_pages = 176 #liczba stron z ogłoszeniami -1 (-1 dla pewności, że nic się nie stanie innego na ostatniej) - można zautomatyzować, aby skrypt sam wiedział ,która jest ostatnią stroną i działał while True
#ostatnia strona nie ma przycisku 'następna strona'

for i in range(number_of_pages):
    main_page = requests.get(main_url) #otwiera url #aktualizowany na koniec aktualnej pętli
    main_soup = BeautifulSoup(main_page.text, 'html.parser') #uruchomienie scrapera


    for link in main_soup.find_all('div', class_='card--bottom-margin'): #przejście po ogłoszeniach na pierwszej stronie z ofertami
        url = 'https://www.morizon.pl/' + link.div.a['href'] #link do konkretnego ogłoszenia


        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser') #dla każdego ogłoszenia uruchamiam scrappera
        
        price = soup.find('span', class_='Lh6ScZ') 
        price_per_meter = soup.find('span', class_='OgttQD')
        if price is not None: #filtruje tylko ogłoszenia mające cenę

            rooms = soup.find('span', class_='Fduk4D').text[3]
            number_of_floors = soup.find_all('span', class_='Fduk4D')[2].text
            location = soup.find_all('h2', class_='_9hyrtb')
            city_district = location[1].text.split(', ') #zapisanie wartości takich jak miasto, dzielnica, ulica w postaci listy
            info_key = soup.find_all('div', class_='sACAYP YyH0Zt') #dodatkowe udogodnienia - nazwy
            info_value = soup.find_all('div', class_='sACAYP e6zNrk') #dodatkowe udogodnienia - wartości

            info.loc[counter, 'id'] = counter #unikalne id
            info.loc[counter, 'Cena'] = price.text #cena
            if price_per_meter is not None:
                info.loc[counter, 'Cena/metr'] = price_per_meter.text #kolumna z ceną za metr
            else:
                info.loc[counter, 'Cena/metr'] = np.nan
            if rooms is not None:
                info.loc[counter, 'Pokoje'] = rooms #kolumna z liczbą pokoi
            else:
                info.loc[counter, 'Pokoje'] = np.nan
            info.loc[counter, 'Miasto'] = city_district[0]  #kolumna z nazwą miasta
            if len(city_district) > 1:
                info.loc[counter, 'Dzielnica'] = city_district[1] #kolumna z nazwą dzielnicy
            else:
                info.loc[counter, 'Dzielnica'] = np.nan
            if len(city_district) > 2:
                info.loc[counter, 'Ulica'] = city_district[2] #kolumna z nazwą ulicy (możliwe, że nie każda oferta bedzie miała podaną ulicę??)
            else:
                info.loc[counter, 'Ulica'] = np.nan

            for i in range(len(info_key)):
                info.loc[counter, info_key[i].text] = info_value[i].text #dodanie dodatkowych parametrów

            if number_of_floors[3:9] == 'parter': #number_of_floors wygląda następująco: ' * parter ' lub ' * piętro 1/5' lub ' * piętro 1'
                info.loc[counter, 'Piętro'] = 0 #jeśli parter w ogłoszeniu - piętro = 0
                info.loc[counter, 'Liczba pięter'] = np.nan #w przypadku parteru nie podają liczby pięter - np.nan - później np.nan zamieni się na średnią liczbę pięter dla zbioru
            elif len(number_of_floors) < 12: #jeśli len < 12 - nie ma podanej ogólnej ilości pięter - zakładam, że w tym wypadku ogłoszenie jest na ostatnim piętrze
                info.loc[counter, 'Piętro'] = number_of_floors[10]
                info.loc[counter, 'Liczba pięter'] = number_of_floors[10]
            elif len(number_of_floors) >= 12: #jesli len > 12 ogłoszenie podaje piętro i liczbę pięter
                info.loc[counter, 'Piętro'] = number_of_floors[10]
                info.loc[counter, 'Liczba pięter'] = number_of_floors[12]

            counter += 1 #id rośnie na koniec petli
        print(info) #sprawdzenie wyników


    #koniec pętli dla ogłoszeń na jednej stronie

    #odczytuje link do kolejnej strony z ogłoszeniami i go zapisuje
    next_url = main_soup.find('div', class_='E0A3rM').a['href']
    main_url = 'https://www.morizon.pl/' + next_url #aktualizacja url na następne przejście pętli (następna strona ogłoszeń)


info.to_csv('C:/Users/Maciej/Documents/projekt_studia/real_estate/final_result.csv')