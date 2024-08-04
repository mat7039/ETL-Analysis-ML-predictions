'''The script aims to upload housing offer data stored in a CSV file into an existing, empty (record-free) table in PostgreSQL. 
The CSV file containing the data was initially saved in the file web-scrap.py, 
and then the data was preliminarily restructured into the appropriate format and saved again.
(pre_SQL_preprocessing.ipynb)'''

import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv('c:/Users/Maciej/Documents/projekt_studia/real_estate/final_result_updated.csv')
df.drop(columns=['Unnamed: 0'], inplace=True) #dataframe automatically creates column with an index that we do not need


user = 'postgres' 
password = 'xxxx' #password to connect with pgadmin4
host = 'localhost' # default
port = '5432'  # default
database = 'real_estate' #database name

# Establishing connection with PostgreSQL
connection_string = f'postgresql://{user}:{password}@{host}:{port}/{database}'
print('connected')

# Creating an engine
engine = create_engine(connection_string)
print('engine')

# Implementing data to the SQL table
table_name = 'real_estate_core'
df.to_sql(table_name, engine, if_exists='append', index=False)
print('Done')