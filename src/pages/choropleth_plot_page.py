import streamlit as st
from config import Config

def page():
    st.markdown(f"# {Config.APP_TITLE}")
    st.markdown("## Choropleth Plot")
    st.sidebar.header("Choropleth Plot")

    st.write("""
        A choropleth map visually displays metrics in a geographical setting. The values of the metrics are coloured relative to each geographic division and therefore allows us to see
        geographic patterns in the data. They also look pretty.

        This page is under construction, but I aim to make it look something like this:
    """)
    st.image("C:/HENRY/GitHub/property_market_analysis/src/assets/images/choropleth_example.png")

if __name__ == "__main__":
    page()