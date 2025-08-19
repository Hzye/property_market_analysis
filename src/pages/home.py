import streamlit as st
from config import Config
from src.utils.data_loader import (
    load_filter_df, load_data, 
    compute_monthly_delta,
    compute_monthly_delta_suburb
)
from src.utils.helper import get_ym_last_month

def page():
    st.markdown(f"# {Config.APP_TITLE}")

    st.markdown("## Home")
    st.write("""
        Welcome to my Australian property market analysis tool. The purpose of this project is for me to practice the Data Science pipeline in
        its entirety (and watch the property market!) 
    """)
    
    st.sidebar.header("Home")

    st.markdown(f"### Monthly Snapshot -- {st.session_state['month']} {st.session_state['year']}")

    col1, col2 = st.columns([1, 3])
    with col1:
        subdiv = st.selectbox(
            "Compare the change in metrics within:", 
            list(st.session_state["df_suburbs"]["name"]))
        delta_vacancy_rate, delta_rental_stock = compute_monthly_delta_suburb(subdiv)

    delta_vac_rate, delta_rent_stock = compute_monthly_delta()
    
    # Quick stats cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Total Suburbs Analysed", value=f"{len(st.session_state.df_suburbs)}")
    
    with col2:
        st.metric(label="Avg. Vacancy Rate", 
        value=f"{st.session_state.df_suburbs.query('name == @subdiv')['vacancy_rate'].iloc[0]:.2f}%", 
        delta=f"{delta_vac_rate:.2f}%")
    
    with col3:
        st.metric(label="Avg. Rental Stock", 
        value=f"{st.session_state.df_suburbs.query('name == @subdiv')['rental_stock'].iloc[0].astype(int)}", 
        delta=f"{delta_rent_stock:.2f}%")
    
    st.write("Compared to last month.")

    st.markdown("---")
    # st.subheader("Navigation")
    
    # # Navigation cards
    # nav_col1, nav_col2, nav_col3 = st.columns(3)
    
    # with nav_col1:
    #     st.info("📊 **Dashboard**  \nView key metrics and summary visualizations")
    
    # with nav_col2:
    #     st.info("🔍 **Data Explorer**  \nExplore and filter your MongoDB data")
    
    # with nav_col3:
    #     st.info("📈 **Analysis**  \nPerform advanced data analysis")

if __name__ == "__main__":
    page()