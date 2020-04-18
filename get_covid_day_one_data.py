import os
import sqlite3
import requests
import json

def setUpDatabase(database_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+database_name)
    cur = conn.cursor()
    return cur, conn

def get_day_one(cur,conn):
    url = 'https://api.covid19api.com/dayone/country/{}'
    cur.execute('SELECT country FROM Covid')
    list_of_tuples = cur.fetchall()
    cur.execute('SELECT COUNT (*) from Dayone ')
    count = cur.fetchone()[0]
    
    if count<248:
        end_count = count+20
        while count<end_count:
            try:
                country = list_of_tuples[count][0]
                url = 'https://api.covid19api.com/dayone/country/'+country
                r = requests.get(url)
                data = r.text
                dict_list = json.loads(data) # decoding JSON file
            
                if dict_list==[]:
                    cur.execute("INSERT OR IGNORE INTO Dayone (country, day_one) VALUES (?,?)",(country,'None'))
                elif dict_list=={'message':'Not Found'}:
                    cur.execute("INSERT OR IGNORE INTO Dayone (country, day_one) VALUES (?,?)",(country,'None'))
                else:
                    cur.execute("INSERT OR IGNORE INTO Dayone (country, day_one) VALUES (?,?)",(country,dict_list[0]['Date']))
            
                count+=1
            
            except:    #break when index has exceeded number of countries in data
                print('You have reached the end of data')
                break
        conn.commit()

def make_table_dayone(cur, conn):

    try:
        cur.execute("CREATE TABLE Dayone (country TEXT PRIMARY KEY, day_one TEXT)")
    
    except:
        print("table exists, proceed to gathering data")




def main():
    cur, conn = setUpDatabase('covid_currency.db')
    make_table_dayone(cur, conn)
    get_day_one(cur,conn)
    

    


if __name__ == "__main__":
    main()
