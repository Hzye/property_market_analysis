import pandas as pd
import streamlit as st
import os
from config import Config
from src.utils.helper import get_ym_today, get_ym_last_month
import streamlit as st

@st.cache_data
def load_data(date=None):

    # Database connection status
    db = st.session_state.get("db")

    if date is None:
        date = get_ym_today()

    df_suburbs = load_filter_df(db, "data_suburbs", {"Date": date})
    df_regions = load_filter_df(db, "data_regions", {"Date": date})
    df_states = load_filter_df(db, "data_states", {"Date": date})
    df_houses = load_filter_df(db, "tables_houses", {"Date": date})
    df_town_houses = load_filter_df(db, "tables_town_houses", {"Date": date})
    df_units = load_filter_df(db, "tables_units", {"Date": date})
    return (
        df_suburbs, 
        df_regions,
        df_states,
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

def compute_monthly_delta():

    cols = ["vacancy_rate", "rental_stock"]

    area_levels = ["suburbs", "regions", "states"]
    property_types = ["houses", "town_houses", "units"]

    current_dict = {
        "suburbs": st.session_state.df_suburbs.sort_values("name").set_index("name"),
        "regions": st.session_state.df_regions,
        "states": st.session_state.df_states,
        "houses": st.session_state.df_houses,
        "town_houses": st.session_state.df_town_houses,
        "units": st.session_state.df_units
    }
    
    df_suburbs, df_regions, df_states, df_houses, df_town_houses, df_units = load_data(get_ym_last_month())

    prev_dict = {
        "suburbs": df_suburbs.sort_values("name").set_index("name"),
        "regions": df_regions,
        "states": df_states,
        "houses": df_houses,
        "town_houses": df_town_houses,
        "units": df_units
    }

    return compute_pc(current_dict["suburbs"][cols].mean(), prev_dict["suburbs"][cols].mean())

def compute_pc(current, prev):
    return (current - prev)/prev * 100