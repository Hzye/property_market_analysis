import streamlit as st
from datetime import datetime
from dateutil.relativedelta import relativedelta

def df_prop_select(prop_select):
    """Select prop dataframe based on user input"""
    if prop_select == "Houses":
        df_prop = st.session_state.df_houses
    elif prop_select == "Townhouses":
        df_prop = st.session_state.df_town_houses
    else:
        df_prop = st.session_state.df_units
    return df_prop

def get_ym_today():
    """Get YYYYMM today."""
    # create dir path
    now = datetime.today()

    current_year = str(now.year)
    current_month = str(now.month)

    if len(current_month) < 2:
        current_month = "0"+current_month

    return datetime.strptime(current_year+current_month, "%Y%m")

def get_ym_last_month():
    """Get YYYYMM last month."""
    today_ym = get_ym_today()

    return today_ym - relativedelta(months=1)