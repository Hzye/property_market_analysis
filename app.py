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
        "df_houses": None,
        "df_town_houses": None,
        "df_units": None,
        "states": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

basic_plot_page = st.Page("src/pages/basic_plot_page.py", title="Basic Plot", icon=":material/add_circle:")
choropleth_plot_page = st.Page("src/pages/choropleth_plot_page.py", title="Choropleth Plot", icon=":material/delete:")

# pg = st.navigation([basic_plot_page, choropleth_plot_page])
# pg.run()

def main():
    db = connect_to_db()

    if "db" not in st.session_state:
        st.session_state.db = db
    
    st.title(Config.APP_TITLE)

    render_sidebar()

    # # load data
    # df_suburbs, df_houses, df_town_houses, df_units = load_data(year_month_select)

    # st.session_state.df_suburbs = df_suburbs
    # st.session_state.df_houses = df_houses
    # st.session_state.df_town_houses = df_town_houses
    # st.session_state.df_units = df_units

    st.header("Hello")

    st.write("""
    This is a multi-page Streamlit application with MongoDB integration and Plotly visualizations.
    Use the sidebar to navigate between different pages or select options below.
    """)
    
    # Quick stats cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Total Suburbs", value="1,234")
    
    with col2:
        st.metric(label="Active Users", value="567", delta="12%")
    
    with col3:
        st.metric(label="Data Points", value="89.5K", delta="-3%")
    
    st.markdown("---")
    st.subheader("Navigation")
    
    # Navigation cards
    nav_col1, nav_col2, nav_col3 = st.columns(3)
    
    with nav_col1:
        st.info("📊 **Dashboard**  \nView key metrics and summary visualizations")
    
    with nav_col2:
        st.info("🔍 **Data Explorer**  \nExplore and filter your MongoDB data")
    
    with nav_col3:
        st.info("📈 **Analysis**  \nPerform advanced data analysis")

    # year_months = os.listdir("data_inv")[:-1][::-1]
    # year_month_select = st.sidebar.selectbox(
    #     "Choose year and month:", 
    #     year_months,
    #     index=0
    # )

    # states = list(df_suburbs["state"].unique()[:-1])
    # st.session_state.states = states

    # stats = [
    #     "vacancy_rate", 
    #     "rental_stock", 
    #     "population", 
    #     "rental_pop"
    # ]

    # stat_select = st.sidebar.selectbox(
    #     "Select statistic:", 
    #     stats,
    # )

    # create_distplot_by_state(
    #     stat=stat_select,
    #     df=df_suburbs,
    #     states=states
    # )

if __name__ == "__main__":
    main()