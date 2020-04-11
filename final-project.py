import os
import sqlite3
import requests
import json

def setUpDatabase(database_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+database_name)
    cur = conn.cursor()
    return cur, conn

def get_data_covid_coutries():
    try:
       # get the data from the url
       url = "https://api.covid19api.com/countries" 
       r = requests.get(url)
       data = r.text
       dict_list = json.loads(data) # decoding JSON file
       #print(dict_list)
       return dict_list

    except:
        print("covid_countries_table: Error when reading from url")


def make_table_covid_countries(dict_list, cur, conn):
    cur.execute("DROP TABLE IF EXISTS Countries")
    cur.execute("CREATE TABLE Countries (country_code TEXT PRIMARY KEY, country TEXT)")
    for i in range(len(dict_list)):
        cur.execute("INSERT INTO Countries (country_code,country) VALUES (?,?)",(dict_list[i]['ISO2'],dict_list[i]['Country']))
    conn.commit()

'''def covid_dayone_table ():
    try:
       # get the data from the url
       #params = str(lat) + "&lng=" + str(long) +"&date=today"
       url = "https://api.covid19api.com/dayone/country/south-africa/status/confirmed" 
       r = requests.get(url)
       dict_ = json.loads(r.text)
   except:
       print("covid_dayone_table: Error when reading from url")'''

#https://api.covid19api.com/dayone/country/south-africa/status/confirmed

def main():
    cur, conn = setUpDatabase('covid_currency.db')
    data_countries = get_data_covid_coutries()
    make_table_covid_countries(data_countries, cur, conn)


if __name__ == "__main__":
    main()
