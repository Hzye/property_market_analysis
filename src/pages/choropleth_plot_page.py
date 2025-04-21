import streamlit as st
from config import Config

def page():
    st.markdown(f"# {Config.APP_TITLE}")
    st.markdown("## Choropleth Plot")
    st.sidebar.header("Choropleth Plot")

if __name__ == "__main__":
    page()