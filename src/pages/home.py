import streamlit as st
from config import Config

def page():
    st.markdown(f"# {Config.APP_TITLE}")

    st.markdown("## Home")
    st.write("""
    This is a multi-page Streamlit application with MongoDB integration and Plotly visualizations.
    Use the sidebar to navigate between different pages or select options below.
    """)
    
    st.sidebar.header("Home")

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

if __name__ == "__main__":
    page()