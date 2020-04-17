import os
import sqlite3
import requests
import json

def setUpDatabase(database_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+database_name)
    cur = conn.cursor()
    return cur, conn

def get_data_covid_coutries(cur, conn):
    try:
        # get the data from the url
        url = "https://api.covid19api.com/countries" 
        r = requests.get(url)
        data = r.text
        dict_list = json.loads(data) # decoding JSON file

    except:
        print("covid_countries_table: Error when reading from url")

    #only inserting data 20 at a time
    cur.execute('SELECT COUNT (*) from Countries')
    count = cur.fetchone()[0]
    print(count)
    end_count = count+20
    while count<end_count:
        cur.execute("INSERT OR IGNORE INTO Countries (country_code,country) VALUES (?,?)",(dict_list[count]['ISO2'],dict_list[count]['Country']))
        count+=1
    conn.commit()


def make_table_covid_countries(cur, conn):

    try:
        cur.execute("CREATE TABLE Countries (country_code TEXT PRIMARY KEY, country TEXT)")
    
    except:
        print("table exists, proceed to gathering data")
    

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
    make_table_covid_countries(cur, conn)
    get_data_covid_coutries(cur,conn)
    


if __name__ == "__main__":
    main()
