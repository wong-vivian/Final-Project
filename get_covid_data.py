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
    length = len(dict_list['Countries'])
    if count< length+1:
        end_count = count+20
        while count<end_count:            
            try:
                countries_data = dict_list['Countries']
                total_confirmed = countries_data[count]['TotalConfirmed']
                total_death = countries_data[count]['TotalDeaths']              
                total_recovered = countries_data[count]['TotalRecovered']
                if total_confirmed != 0:
                    death_rate = total_death*100/total_confirmed            #count death rate for each country in percentage
                    recovered_rate = total_recovered*100/total_confirmed    #count recovered rate for each country in percentage
                else:
                    death_rate = 0              #set death rate to 0 if no confirmed case yet
                    recovered_rate = 0          #set recovered rate to 0 if no confirmed case yet
                cur.execute("INSERT OR IGNORE INTO Covid (country_code,country,total_confirmed, total_deaths, total_recovered, death_rate, recovered_rate) VALUES (?,?,?,?,?,?,?)",(countries_data[count]['CountryCode'],countries_data[count]['Country'], total_confirmed, total_death, total_recovered, death_rate, recovered_rate))
                count+=1
            except:    #break when index has exceeded number of countries in data
                print('You have reached the end of data')
                break
        conn.commit()
    
    


def make_table_covid(cur, conn):

    try:
        cur.execute("CREATE TABLE Covid (country_code TEXT PRIMARY KEY, country TEXT, total_confirmed INTEGER, total_deaths INTEGER, total_recovered INTEGER, death_rate FLOAT, recovered_rate FLOAT)")
    
    except:
        print("table exists, proceed to gathering data")
    



def main():
    cur, conn = setUpDatabase('covid_worldbank.db')
    make_table_covid(cur, conn)
    get_data_covid_coutries(cur,conn)
   

    


if __name__ == "__main__":
    main()
