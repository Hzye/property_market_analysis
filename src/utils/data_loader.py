import pandas as pd
import streamlit as st
import os
from config import Config
from src.utils.helper import get_ym_today

@st.cache_data
def load_data():

    # Database connection status
    db = st.session_state.get("db")

    ym_today = get_ym_today()

    df_suburbs = load_filter_df(db, "data_suburbs", {"Date": ym_today})
    df_houses = load_filter_df(db, "tables_houses", {"Date": ym_today})
    df_town_houses = load_filter_df(db, "tables_town_houses", {"Date": ym_today})
    df_units = load_filter_df(db, "tables_units", {"Date": ym_today})
    return (
        df_suburbs, 
        df_houses,
        df_town_houses,
        df_units
    )

def load_df(db, name):
    coll = db[name]
    return pd.DataFrame(coll.find({})).drop(columns="_id")

def filter_df(df, condition):
    key = list(condition.keys())[0]
    value = condition[key]
    
    if key == "Date":
        df = df[df["Date"] == pd.to_datetime(value)].drop(columns="Date")
    elif key == "name" or key == "Suburb":
        df = df[df["name"] == value].drop(columns="name")
    return df

def load_filter_df(db, name, condition):
    df = load_df(db, name)
    return filter_df(df, condition)