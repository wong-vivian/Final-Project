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
        url = "https://api.covid19api.com/summary" 
        r = requests.get(url)
        data = r.text
        dict_list = json.loads(data) # decoding JSON file

    except:
        print("covid_table: Error when reading from url")

    #only inserting data 20 at a time
    cur.execute('SELECT COUNT (*) from Covid ')
    count = cur.fetchone()[0]
    #print(count)
    if count+249:
        end_count = count+20
        while count<end_count:
            countries_data = dict_list['Countries']
            try:
                cur.execute("INSERT OR IGNORE INTO Covid (country_code,country,total_confirmed, total_deaths, total_recovered) VALUES (?,?,?,?,?)",(countries_data[count]['CountryCode'],countries_data[count]['Country'], countries_data[count]['TotalConfirmed'],countries_data[count]['TotalDeaths'], countries_data[count]['TotalRecovered']))
                count+=1
            except:    #break when index has exceeded number of countries in data
                print('You have reached the end of data')
                break
        conn.commit()


def make_table_covid(cur, conn):

    try:
        cur.execute("CREATE TABLE Covid (country_code TEXT PRIMARY KEY, country TEXT, total_confirmed INTEGER, total_deaths INTEGER, total_recovered INTEGER)")
    
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
    make_table_covid(cur, conn)
    get_data_covid_coutries(cur,conn)
    


if __name__ == "__main__":
    main()
