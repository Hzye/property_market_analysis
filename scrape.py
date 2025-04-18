import requests
import pandas as pd
from tqdm import tqdm
import re
import pickle
from bs4 import BeautifulSoup
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
from datetime import datetime

# load in global vars
load_dotenv()
uri = os.getenv('DATABASE_URL')

def main():
    db = connect_to_db(uri)

    # use this to index
    suburbs = db["locations"].distinct("name")
    valid_suburbs = [sub.lower().replace(" ", "+") for sub in suburbs]

    # scrape
    suburb_tables, suburb_other_data = scrape_tables_and_data(valid_suburbs)

def scrape_tables_and_data(valid_suburbs):
    suburb_tables = {}
    suburb_other_data = {}

    for suburb in tqdm(valid_suburbs, desc="Scraping"):
        # get html
        page = requests.get(f'https://www.realestateinvestar.com.au/property/{suburb}')
        
        # save soup
        soup = BeautifulSoup(page.text, 'html.parser')
        
        suburb_tables[suburb] = scrape_tables(soup)
        suburb_other_data[suburb] = pd.DataFrame(scrape_other_data(suburb, soup))
    
    return suburb_tables, suburb_other_data

def scrape_tables(soup):
    # get all tables from soup
    tables = soup.find_all('table')
    
    # set table names
    table_names = ["median", "rental", "sales"]
    
    # instantiate empty dict
    dfs = {}
    
    # iterate over the three tables and populate
    for i, table in enumerate(tables):
        # Extract headers (th elements)
        headers = [header.get_text(strip=True) for header in table.find_all('td', class_='datatitle')]

        # extract rows
        rows = []
        for row in table.find_all('tr')[1:]:  # skip the header row
            cells = row.find_all('td')
            row_data = [cell.get_text(strip=True) for cell in cells]
            rows.append(row_data)

        # create a DataFrame
        df = pd.DataFrame(rows, columns=['Metric'] + headers)
        dfs[table_names[i]] = df
    return dfs

def scrape_other_data(suburb, soup):
    other_data = {}

    paras = soup.find_all('p')

    vac_rates = []
    rental_stocks = []
    pops = []
    rental_pops = []

    for i, p in enumerate(paras):
        # get region
        if "  Suburb" in p.get_text():
            suburb_name = p.get_text().split("\n")[2]
            other_data["suburb"] = {"name": suburb_name}

        # get region
        if "  Region" in p.get_text():
            region_name = p.get_text().split("\n")[2]
            other_data["region"] = {"name": region_name}

        # get state
        if "  State" in p.get_text():
            #print(p.get_text())
            state_name = p.get_text().split("\n")[2]
            other_data["state"] = {"name": state_name}

        # get vac rate
        if "Current vacancy rate" in p.get_text():
            vac_rates.append(paras[i-1].get_text())

        # get rental stock
        if "Rental stock available" in p.get_text():
            rental_stocks.append(paras[i-1].get_text())

        # get pop
        if "Population" in p.get_text():
            pops.append(paras[i-1].get_text())

        # get rental pop
        if "Rental population" in p.get_text():
            rental_pops.append(paras[i-1].get_text())

    if suburb == "act":
        sas = ["state"]
    else:
        sas = ["suburb", "region", "state"]
    for (sa, vr, rs, p, rp) in zip(sas, vac_rates, rental_stocks, pops, rental_pops):
        other_data[sa]["vacancy_rate"] = vr
        other_data[sa]["rental_stock"] = rs
        other_data[sa]["population"] = p
        other_data[sa]["rental_pop"] = rp
        
    return other_data

def connect_to_db(uri):
    # establish db connection
    client = MongoClient(uri, server_api=ServerApi('1'))

    # ping
    try:
        client.admin.command('ping')
        print("Connected to db.")
    except Exception as e:
        print(e)

    # connect to db
    db = client["aus_prop"]
    return db

if __name__ == '__main__':
    main()