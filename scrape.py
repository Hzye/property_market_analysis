import requests
import pandas as pd
import numpy as np
from tqdm import tqdm
from bs4 import BeautifulSoup
from src.utils.database import connect_to_db
from dotenv import load_dotenv
import os
from datetime import datetime
from src.utils.helper import get_ym_today

# load in global vars
load_dotenv()
scrape_url = os.getenv("SCRAPE_URL")
uri = os.getenv("DATABASE_URL")

def main():
    db = connect_to_db()

    # use this to index
    suburbs = db["locations"].distinct("name")
    valid_suburbs = [sub.lower().replace(" ", "+") for sub in suburbs]

    # scrape
    tables, data = scrape_tables_and_data(valid_suburbs)

    # clean data
    df_suburbs, df_regions, df_states = clean_data(data)

    # clean tables
    df_houses, df_town_houses, df_units = clean_tables(suburbs, tables)

    # add date
    dfs = [
        df_suburbs, df_regions, df_states,
        df_houses, df_town_houses, df_units
    ]
    dfs = [add_date_col(df) for df in dfs]

    # add files to collections
    collection_names = [
        "data_suburbs",
        "data_regions",
        "data_states",
        "tables_houses",
        "tables_town_houses",
        "tables_units"
    ]

    # for (collection_name, df) in zip(collection_names, dfs):
    #     add_to_collection(db, collection_name, df)

def add_date_col(df):
    """Add date col to df."""
    date_today = get_ym_today()

    df["Date"] = date_today
    return df[["Date"] + [x for x in df.columns if "Date" not in x]]

def clean_tables(suburbs, tables):
    """Clean tabular data from scraping."""
    cols = get_table_cols(tables)

    df_houses, df_town_houses, df_units  = separate_tables(cols, suburbs, tables)

    df_houses = df_to_numeric(df_houses)
    df_town_houses = df_to_numeric(df_town_houses)
    df_units = df_to_numeric(df_units)

    df_houses.index.name = "Suburb"
    df_town_houses.index.name = "Suburb"
    df_units.index.name = "Suburb"

    return df_houses, df_town_houses, df_units

def separate_tables(cols, suburbs, tables):
    """Separate tabular data into property type."""
    # init empty df
    df_houses = pd.DataFrame(index=suburbs, columns=cols)
    df_town_houses = pd.DataFrame(index=suburbs, columns=cols)
    df_units = pd.DataFrame(index=suburbs, columns=cols)

    for suburb in suburbs:
        suburb_ = suburb.lower().replace(" ", "+")
        df_sub_table = pd.concat([
            tables[suburb_]["median"], 
            tables[suburb_]["rental"], 
            tables[suburb_]["sales"]
        ])
        
        df_houses.loc[suburb, :] = df_sub_table["House"].values
        df_town_houses.loc[suburb, :] = df_sub_table["Townhouses"].values
        df_units.loc[suburb, :] = df_sub_table["Units"].values

    return df_houses, df_town_houses, df_units

def df_to_numeric(df):
    """Convert table columns to numeric type."""
    df = df.dropna(axis=1)
    df = df.map(lambda x: x.replace("$", "").replace(",", "").replace("%", ""))
    return df.map(pd.to_numeric, errors="coerce")

def get_table_cols(tables):
    """Get tabular data column headers."""
    cols = list(tables["abbotsbury"]["median"]["Metric"].values) \
        + list(tables["abbotsbury"]["rental"]["Metric"].values) \
        + list(tables["abbotsbury"]["sales"]["Metric"].values)
    
    cols[1] = "Median price change - last quarter (%)"
    cols[2] = "Median price change - 1 year (%)"
    cols[3] = "Median price change - 2 years (%)"
    cols[6] = "Median rent change - 1 year (%)"
    cols[-2] = "Stock variance vs. last year (%)"

    return cols

def clean_data(data):
    """Clean other data (not tabular) from scrape."""

    data_suburbs, data_regions, data_states = split_data(data)

    df_suburbs = combine_clean_data(data_suburbs)
    df_regions = combine_clean_data(data_regions)
    df_states = combine_clean_data(data_states)

    return df_suburbs, df_regions, df_states

def combine_clean_data(data):
    """Combine non-tabular data into appropriate SA level."""
    df_data = pd.concat(data, axis=1)
    df_data.columns = df_data.iloc[0]
    df_data = df_data.iloc[1:,:]
    df_data = df_data.T
    
    if data[0].name == "region":
        df_data.drop(columns=["region"], inplace=True)
    elif data[0].name == "state":
        df_data.drop(columns=["region", "state"], inplace=True)

    df_data["vacancy_rate"] = df_data["vacancy_rate"].apply(lambda x: x.replace("%", ""))
    df_data["rental_stock"] = df_data["rental_stock"].apply(lambda x: x.replace(",", ""))
    df_data["population"] = df_data["population"].apply(lambda x: x.replace(",", ""))
    df_data["rental_pop"] = df_data["rental_pop"].apply(lambda x: x.replace("%", ""))
    df_data.iloc[:, :4] = df_data.iloc[:, :4].replace("NA", np.nan).apply(pd.to_numeric)
    
    return df_data.drop_duplicates()

def split_data(data):
    """Split data into suburb, region and state level."""
    data_ = []
    for x in data.values():
        if len(x.columns) == 3:
            x.loc["state"] = [x.loc["name", "state"]]*3
            x.loc["region"] = [x.loc["name", "region"]]*3
            data_.append(x)

    data_suburbs = [x.iloc[:, 0] for x in data_]
    data_regions = [x.iloc[:, 1] for x in data_]
    data_states = [x.iloc[:, 2] for x in data_]

    return data_suburbs, data_regions, data_states

def scrape_tables_and_data(valid_suburbs):
    """Scrape tabular and non-tabular data."""
    suburb_tables = {}
    suburb_other_data = {}

    for suburb in tqdm(valid_suburbs, desc="Scraping"):
        # get html
        page = requests.get(os.path.join(scrape_url, suburb))
        
        # save soup
        soup = BeautifulSoup(page.text, 'html.parser')
        
        suburb_tables[suburb] = scrape_tables(soup)
        suburb_other_data[suburb] = pd.DataFrame(scrape_other_data(suburb, soup))
    
    return suburb_tables, suburb_other_data

def scrape_tables(soup):
    """Scrape tabular data."""
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
    """Scrape non-tabular data."""
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

if __name__ == '__main__':
    main()