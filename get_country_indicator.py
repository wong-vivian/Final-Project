import os
import sqlite3
import requests
import json
from datetime import datetime
def setUpDatabase(database_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+database_name)
    cur = conn.cursor()
    return cur, conn
def get_data_population():
    try:
        #getting data and returning a dictionary
        request_url    = "http://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?format=json&date=2018&per_page=500"
        r = requests.get(request_url)
        data = r.text    
        dict_list = json.loads(data) # decoding JSON file
        return(dict_list)
    except:
        print("Error when reading from url")
def get_data_gdp():
    try:
        #getting data and returning a dictionary
        request_url    = "http://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?format=json&date=2018&per_page=500"
        r = requests.get(request_url)
        data = r.text    
        dict_list = json.loads(data) # decoding JSON file
        return(dict_list)
    except:
        print("Error when reading from url")
def make_table(cur, conn):
    try:
        cur.execute("CREATE TABLE Country_Indicator (country TEXT PRIMARY KEY, population INTEGER, GDP INTEGER)")
    except:
        print("table exists, proceed to gathering data")
def insert_data(cur, conn):
    data_pop = get_data_population()
    data_gdp = get_data_gdp()
    length = len(data_pop[1]) + 1
    #only inserting data 20 at a time
    cur.execute('SELECT COUNT (*) from Country_Indicator ')
    count = cur.fetchone()[0]
    if count < length:
        end_count = count+20
        while count<end_count:
            try:
                cur.execute("INSERT OR IGNORE INTO Country_Indicator (country, population, gdp) VALUES (?,?,?)",(data_pop[1][count]['country']['value'],data_pop[1][count]['value'], data_gdp[1][count]['value']))
                count+=1
            except:    #break when index has exceeded number of countries in data
                print('You have reached the end of data')
                break
        conn.commit()
def main():
    cur, conn = setUpDatabase('covid_worldbank.db')
    make_table(cur, conn)
    insert_data(cur,conn)


if __name__ == "__main__":
    main()