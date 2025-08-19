import streamlit as st
from config import Config
from src.utils.data_loader import load_historical_data
import plotly.express as px

def page():
    st.session_state.df_suburbs_historical = load_historical_data()
    st.markdown(f"# {Config.APP_TITLE}")
    st.markdown("## Time Series Plots")
    st.write("""
        Time series plots allow us to identify patterns or trends in metrics over time. 

        This page currently only supports plotting a single metric of a suburb.    
    """)

    # side bar selections
    st.sidebar.header("Basic Plots")

    suburb_select = st.sidebar.selectbox(
        "Suburb:", 
        st.session_state.suburbs,
    )

    y_select = st.sidebar.selectbox(
        "Y axis:", 
        ["vacancy_rate", "rental_stock", "population", "rental_pop"],
    )

    df = st.session_state.df_suburbs_historical.query("name == @suburb_select")

    fig = px.line(df, x="Date", y=y_select, markers=True)  # markers=True adds dots
    fig.update_traces(line=dict(width=2), marker=dict(size=8))

    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    page()