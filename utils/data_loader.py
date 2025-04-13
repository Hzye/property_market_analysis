import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_data(year_month):
    data_date_dir = os.path.join("data_inv", year_month)
    df_suburbs = pd.read_csv(os.path.join(data_date_dir, "df_data_suburbs.csv"))
    df_houses = pd.read_csv(os.path.join(data_date_dir, "df_tables_houses.csv"))
    df_town_houses = pd.read_csv(os.path.join(data_date_dir, "df_tables_town_houses.csv"))
    df_units = pd.read_csv(os.path.join(data_date_dir, "df_tables_units.csv"))
    return (
        df_suburbs, 
        df_houses,
        df_town_houses,
        df_units
    )