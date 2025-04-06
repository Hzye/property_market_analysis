import streamlit as st
from utils.data_loader import load_data
from utils.data_utils import merge_suburb
from utils.plot_utils import create_basic_plot
from utils.misc import df_prop_select

st.set_page_config(
    page_title="Basic Plots", 
    page_icon="🏠",
    layout="wide"
)

st.markdown("# 📈Basic Plots")

# side bar selections
st.sidebar.header("Basic Plots")

state_select = st.sidebar.selectbox(
    "State:", 
    st.session_state.states,
)

prop_select = st.sidebar.selectbox(
    "Property type:", 
    ["Houses", "Townhouses", "Units"],
)

df_prop = df_prop_select(prop_select)

df_filtered = merge_suburb(
    st.session_state.df_suburbs, 
    df_prop, 
    state_select
)

df_filtered_cols = df_filtered.columns[1:]

x_select = st.sidebar.selectbox(
    "X axis:", 
    df_filtered_cols,
)

y_select = st.sidebar.selectbox(
    "Y axis:", 
    df_filtered_cols,
)

st.write(f"### {prop_select} in {state_select}")
create_basic_plot(
    df_filtered,
    x_select,
    y_select
)