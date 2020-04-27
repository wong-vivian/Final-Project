import os
import sqlite3
import requests
import json

def setUpDatabase(database_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+database_name)
    cur = conn.cursor()
    return cur, conn

#function that counts the world's confirmed cases, deaths, and recovered
def calculations (cur, conn):
    total_dict = {}
    cur.execute("SELECT SUM(total_confirmed) from Covid")
    total_confirmed = cur.fetchone()[0]    
    cur.execute("SELECT SUM(total_deaths) from Covid")
    total_death = cur.fetchone()[0]
    cur.execute("SELECT SUM(total_recovered) from Covid")
    total_recovered = cur.fetchone()[0]
    cur.execute("SELECT SUM(death_rate) from Covid")
    total_death_rate = cur.fetchone()[0]
    cur.execute("SELECT COUNT(death_rate) from Covid")
    count_dr = cur.fetchone()[0]
    cur.execute("SELECT SUM(recovered_rate) from Covid")
    total_recovered_rate = cur.fetchone()[0]
    cur.execute("SELECT COUNT(recovered_rate) from Covid")
    count_rr = cur.fetchone()[0]
    
    #total death, recovered, confirmed
    total_dict['total_confirmed']=total_confirmed
    total_dict['total_death']=total_death
    total_dict['total_recovered']=total_recovered
    #world's death rate
    total_dict['wdr']=total_death*100/total_confirmed
    #world's recovered rate
    total_dict['wrr']=total_recovered*100/total_confirmed
    #average death rate of countries in the world
    total_dict['adr']=total_death_rate/count_dr
    #average recovered rate of countries in the world
    total_dict['arr']=total_recovered_rate/count_rr
    
    return total_dict

#count average infection rate of the whole world
def average_infection_rate_world (cur, conn):
    cur.execute("SELECT population, total_confirmed FROM Covid JOIN Country_Indicator ON Covid.country = Country_Indicator.country")
    list_of_tuple = cur.fetchall()
    #print(list_of_tuple)
    infection_rate_list = []
    for i in range(len(list_of_tuple)):
        if list_of_tuple[i][1]==0:
            infection_rate_list.append(0)
        elif list_of_tuple[i][0]==None or list_of_tuple[i][1]==None:
            continue
        else:
            infection_rate_list.append(100*float(list_of_tuple[i][1])/float(list_of_tuple[i][0]))

    average = sum(infection_rate_list)/len(infection_rate_list)
    return average
    

def main():
    cur, conn = setUpDatabase('covid_worldbank.db')
    #print (total_counts(cur,conn))
    #print(infection_rate_world(cur, conn))

    calc_dict = calculations(cur,conn)
    air = average_infection_rate_world(cur,conn)
    #write calculations to csv
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fname = dir_path + '/' + "covid_calculation.txt"
    fw = open(fname,'w')
    fw.write(('Total confirmed Covid cases: ')+str(calc_dict['total_confirmed']))
    fw.write('\n')
    fw.write(('Total Covid related deaths: ')+str(calc_dict['total_death']))
    fw.write('\n')
    fw.write(('Total recovery from Covid cases: ')+str(calc_dict['total_recovered']))
    fw.write('\n')
    fw.write(("World Covid related Death Rate: ")+str(calc_dict['wdr']))
    fw.write('\n')
    fw.write(("World Covid Recovery Rate: ")+str(calc_dict['wrr']))
    fw.write('\n')
    fw.write(("World Average Covid Death Rate: ")+str(calc_dict['adr']))
    fw.write('\n')
    fw.write(("World Average Covid Recovery Rate: ")+str(calc_dict['arr']))
    fw.write('\n')
    fw.write(("World Average Covid Infection Rate: ")+str(air))
    
    fw.close()


if __name__ == "__main__":
    main()




    






