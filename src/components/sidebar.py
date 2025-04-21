import streamlit as st
from config import Config
from src.utils.database import get_collection_names

def render_sidebar():
    """Render the sidebar with common controls and info"""
    with st.sidebar:
        # Logo/title section
        st.markdown(Config.APP_TITLE, 
                   unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Database connection status
        db = st.session_state.get("db")

        # Filter section
        st.subheader("Filters")
        
        # Date range filter (will be handled in specific pages)
        # Add common filters here
        
        with st.expander("Advanced Filters"):
            # Add advanced filters that are common across pages
            limit = st.slider("Record Limit", min_value=10, max_value=10000, value=1000, step=10)
            st.session_state.data_limit = limit
        
        st.markdown("---")
        
        # About section
        with st.expander("About"):
            st.write("""
            This is a multi-page Streamlit app with MongoDB integration and Plotly visualizations.
            Built with:
            - Streamlit
            - Plotly
            - MongoDB
            """)
            
            st.write("Version 1.0.0")