import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df_suburbs = pd.read_csv("df_data_suburbs.csv")
    df_houses = pd.read_csv("df_tables_houses.csv")
    df_town_houses = pd.read_csv("df_tables_town_houses.csv")
    df_units = pd.read_csv("df_tables_units.csv")
    return (
        df_suburbs, 
        df_houses,
        df_town_houses,
        df_units
    )