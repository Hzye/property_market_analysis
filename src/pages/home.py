import streamlit as st
from config import Config
from src.utils.data_loader import load_filter_df, load_data, compute_monthly_delta
from src.utils.helper import get_ym_last_month

def page():
    st.markdown(f"# {Config.APP_TITLE}")

    st.markdown("## Home")
    st.write("""
        Welcome to my Australian property market analysis tool. The purpose of this project is for me to practice the Data Science pipeline in
        its entirety. 
    """)
    
    st.sidebar.header("Home")

    st.markdown("### Monthly Snapshot")
    st.write("Compare the change in metrics within:")

    delta_vac_rate, delta_rent_stock = compute_monthly_delta()

    # Quick stats cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Total Suburbs", value=f"{len(st.session_state.df_suburbs)}")
    
    with col2:
        st.metric(label="Avg. Vacancy Rate", value=f"{st.session_state.df_suburbs['vacancy_rate'].mean():.2f}%", delta=f"{delta_vac_rate:.2f}%")
    
    with col3:
        st.metric(label="Avg. Rental Stock", value=f"{st.session_state.df_suburbs['rental_stock'].mean().astype(int)}", delta=f"{delta_rent_stock:.2f}%")
    
    st.write("Compared to last month.")

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

if __name__ == "__main__":
    page()