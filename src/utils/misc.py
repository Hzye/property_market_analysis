import streamlit as st

def df_prop_select(prop_select):
    """Select prop dataframe based on user input"""
    if prop_select == "Houses":
        df_prop = st.session_state.df_houses
    elif prop_select == "Townhouses":
        df_prop = st.session_state.df_town_houses
    else:
        df_prop = st.session_state.df_units
    return df_prop