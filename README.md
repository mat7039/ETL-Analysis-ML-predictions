The aim of the project is to create real estate price prediction model
In other words, the project aims to build a program in which user can add parameters from an advertisement they are interested in. As a result, they will receive feedback regarding the valuation of the offer (whether the offer is priced appropriately compared to similar ones, or if it is underpriced or overpriced). The application also aims to display the forecasted 'appropriate' price of the offer if it is not already so.

The motivation for undertaking the project is the desire to expand the range of tools that help in selecting the right offers on the real estate market, increasing awareness of the current state of the market, and the most important factors affecting the price of an apartment.

Project process overview:
![image](https://github.com/user-attachments/assets/9af54043-0fcf-44d1-8f92-e22fffa646f6)



1. Extraction
   In this step, I scraped data from the web using python script operating on html code and saved raw data as csv file on my local computer.
2. Transform
   The Data needed to be preprocessed in order to deliver it into strict relational table in the PostgreSQL Database.
   In this step I also applied some business logic: I dealt with missing values and deleted some unnecessary columns.
3. Database preparation
   In order to load data into DB I needed to create in advance a stage table containing columns and data types that match those in the preprocessed data file.
4. Load
   Loading csv file from local computer into Database using python script.
5. Data modeling
   For the sake of learning I decided to normalize data even though it is not recommended approach for OLAP environment.
6. Data analysis
   Short analysis of the data using SQL syntax.
7. Data visualization
   Most important visuals of the information that I learned while exploring the data using SQL.
8. Prediction Models
    Building a goal of the project: prediction model where anyone can put data about real estate that they are interested in and get estimated price in result.


Database schema after data modeling:
![image](https://github.com/user-attachments/assets/af209fd6-4d0a-4fe0-a697-526cc6acac44)



Final results:
![image](https://github.com/user-attachments/assets/bd2a50b4-c7ca-48a7-93a8-c56db4ee1e10)

