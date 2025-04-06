import streamlit as st
from components.sidebar import render_sidebar
from utils.data_loader import load_data
from utils.plot_utils import create_distplot_by_state

st.set_page_config(
    page_title="AusProp", 
    page_icon="🏠",
    layout="wide"
)

# Initialization
if 'df_suburbs' not in st.session_state:
    st.session_state['df_suburbs'] = None

def main():
    render_sidebar()

    st.title("🏠 Australian Property Market Analysis")

    df_suburbs, df_houses, df_town_houses, df_units = load_data()

    st.session_state.df_suburbs = df_suburbs
    st.session_state.df_houses = df_houses
    st.session_state.df_town_houses = df_town_houses
    st.session_state.df_units = df_units

    states = list(df_suburbs["state"].unique()[:-1])
    st.session_state.states = states

    stats = [
        "vacancy_rate", 
        "rental_stock", 
        "population", 
        "rental_pop"
    ]

    stat_select = st.sidebar.selectbox(
        "Select statistic:", 
        stats,
    )

    create_distplot_by_state(
        stat=stat_select,
        df=df_suburbs,
        states=states
    )

if __name__ == "__main__":
    main()