import streamlit as st
from config import Config
from src.components.sidebar import render_sidebar
from src.utils.data_loader import load_data
from src.utils.plot_utils import create_distplot_by_state
from src.utils.database import connect_to_db
import os

st.set_page_config(
    page_title="AusProp", 
    page_icon="🏠",
    layout="wide"
)

# with open("src/assets/style.css") as f:
#     st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialization
def init_session_state():
    defaults = {
        "df_suburbs": None,
        "df_regions": None,
        "df_states": None,
        "df_houses": None,
        "df_town_houses": None,
        "df_units": None,
        "states": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

home_page = st.Page("src/pages/home.py", title="Home", icon=":material/add_circle:")
basic_plot_page = st.Page("src/pages/basic_plot_page.py", title="Basic Plot", icon=":material/add_circle:")
choropleth_plot_page = st.Page("src/pages/choropleth_plot_page.py", title="Choropleth Plot", icon=":material/delete:")

def main():
    db = connect_to_db()

    if "db" not in st.session_state:
        st.session_state.db = db

    #render_sidebar()

    # load data
    df_suburbs, df_regions, df_states, df_houses, df_town_houses, df_units = load_data()

    st.session_state.df_suburbs = df_suburbs
    st.session_state.df_regions = df_regions
    st.session_state.df_states = df_states
    st.session_state.df_houses = df_houses
    st.session_state.df_town_houses = df_town_houses
    st.session_state.df_units = df_units

    st.session_state.states = list(df_states["name"].values)

    pg = st.navigation([home_page, basic_plot_page, choropleth_plot_page])
    pg.run()

if __name__ == "__main__":
    main()