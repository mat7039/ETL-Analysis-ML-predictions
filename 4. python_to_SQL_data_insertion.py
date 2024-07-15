'''Skrypt ma na celu wgranie danych ofert mieszkań na sprzedaż przechowywanych w pliku csv do istniejącej, pustej (jeszcze nie zawierającej rekordów) tabeli w postgreSQL.
Plik csv zawierający dane został pierwotnie zapisany w pliku web-scrap.py, a następnie dane zostały wstępnie przemodelowane do odpowiedniej postaci i ponownie zapisane
(pre_SQL_preprocessing.ipynb)'''

import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv('c:/Users/Maciej/Documents/projekt_studia/real_estate/final_result_updated.csv')
df.drop(columns=['Unnamed: 0'], inplace=True) #dataframe automatycznie tworzy kolumnę z indeksem, która po zapisie pliku do csv przechowywana jest pod nazwą Unnamed: 0, w tym przypadku taka kolumna jest niepotrzebna do dalszej analizy
print(df) #sprawdzenie poprawności wgrania dataframe


user = 'postgres' 
password = 'xxxx' #login i hasło do połączenia się z pgadmin4
host = 'localhost' # domyślne
port = '5432'  # domyślne
database = 'real_estate' #nazwa bazy danych (zgodnie z plikiem z kodem SQL

# Utworzenie połączenia z postgreSQL
connection_string = f'postgresql://{user}:{password}@{host}:{port}/{database}'
print('connected')

# Uruchomienie silnika
engine = create_engine(connection_string)
print('engine')

# Wgrywanie danych do tabeli w SQL
table_name = 'real_estate_core'
df.to_sql(table_name, engine, if_exists='append', index=False)
print('Done')