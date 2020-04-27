import os
import sqlite3
import requests
import json
import numpy as np
import matplotlib.pyplot as plt

def setUpDatabase(database_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+database_name)
    cur = conn.cursor()
    return cur, conn

def top_50_gdp_dr_rr(cur, conn):
    result = cur.execute("SELECT Covid.country, death_rate, recovered_rate FROM Covid JOIN Country_Indicator ON Covid.country = Country_Indicator.country ORDER BY Country_Indicator.GDP DESC LIMIT 50")
    recovered_rate = []
    death_rate = []
    country = []
    for row in result:
        recovered_rate.append(row[2])
        death_rate.append(row[1])
        country.append(row[0])
    
    fig, ax = plt.subplots()
    ax.scatter(death_rate, recovered_rate, marker = 'x', color = 'c')
    for x,y,i in zip(death_rate,recovered_rate, country):
        label = i
        plt.annotate(label, # this is the text
                (x,y), # this is the point to label
                textcoords="offset points", # how to position the text
                xytext=(0,3), # distance from text to points (x,y)
                ha='center', # horizontal alignment can be left, right or center
                size = 7.5) 
    ax.set(xlabel='Death Rate (%)', ylabel='Recovery Rate(%)',
        title='Top 50 GDP Countries: Death Rate vs Recovery Rate')
    ax.grid()
    fig.set_size_inches(10.5, 10.5)
    fig.savefig("test.png")
    plt.show()
def top_10_rec_gdp(cur, conn):
    result = cur.execute("SELECT Covid.country, recovered_rate, Country_Indicator.GDP FROM Covid JOIN Country_Indicator ON Covid.country = Country_Indicator.country ORDER BY Country_Indicator.GDP DESC LIMIT 10")
    recovered_rate = []
    gdp = []
    country = []
    for row in result:
        recovered_rate.append(row[1])
        gdp.append(row[2])
        country.append(row[0])
    
    fig, ax = plt.subplots()
    ax.scatter(gdp, recovered_rate, marker = 'x', color = 'black')
    for x,y,i in zip(gdp,recovered_rate, country):
        label = i
        plt.annotate(label, # this is the text
                (x,y), # this is the point to label
                textcoords="offset points", # how to position the text
                xytext=(0,10), # distance from text to points (x,y)
                ha='center') # horizontal alignment can be left, right or center
    ax.set(xlabel='GDP (in Trillions USD)', ylabel='Recovery Rate (%)',
        title='Top 10 GDP Countries: Covid Recovery Rate')
    ax.grid()
    fig.set_size_inches(10.5, 10.5)
    fig.savefig("test.png")
    plt.show()
def top_10_death_rec_rate(cur, conn):
    result = cur.execute("SELECT country, death_rate, recovered_rate FROM Covid ORDER BY death_rate DESC LIMIT 10")
    death_rate = []
    country = []
    recovered_rate = []
    for row in result:
        country.append(row[0])
        death_rate.append(row[1])
        recovered_rate.append(row[2])
    fig, ax = plt.subplots()
    ax.bar(country, death_rate, label='Death Rate')
    ax.bar(country, recovered_rate, bottom= death_rate,
        label='Recovery Rate')
    ax.set_ylabel('Death/Recovery Rate (%)')
    ax.set_title('Top 10 Covid Death Rate Countries and its Recovery Rate')
    plt.xticks(fontsize=8)
    ax.legend()
    fig.set_size_inches(10.5, 10.5)
    fig.savefig("test.png")
    plt.show()
def dr_rr_vs_population(cur, conn):
    result = cur.execute("SELECT Covid.country, death_rate, recovered_rate, Country_Indicator.population FROM Covid JOIN Country_Indicator ON Covid.country = Country_Indicator.country")
    recovered_rate = []
    death_rate = []
    population = []
    for row in result:
        recovered_rate.append(row[2])
        death_rate.append(row[1])
        population.append(row[3])
    fig, ax = plt.subplots()
    ax.scatter(population, recovered_rate, marker = 'x', color = 'c', label = 'Recovery Rate')
    ax.scatter(population, death_rate, marker='o', color = 'b', label = 'Death Rate')
    ax.set(xlabel='Population (in Billions)', ylabel='Death/Recovery Rate (%)',
        title='Covid Death/Recovery Rate vs Population per Country')
    ax.legend()
    ax.grid()
    fig.set_size_inches(10.5, 10.5)
    fig.savefig("test.png")
    plt.show()
def main():
    cur, conn = setUpDatabase('covid_worldbank.db')
    top_10_rec_gdp(cur, conn)
    dr_rr_vs_population(cur,conn)
    top_10_death_rec_rate(cur, conn)
    top_50_gdp_dr_rr(cur, conn)
if __name__ == "__main__":
    main()