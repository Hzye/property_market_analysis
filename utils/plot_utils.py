import pandas as pd
import json
import geopandas as gpd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import re
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt

def remove_outliers(df):
    """Filter outliers."""
    q1 = df.quantile(0.25)
    q3 = df.quantile(0.75)
    iqr = q3 - q1
    upper_thresh = q3 + 1.5*iqr
    
    return df[df < upper_thresh]

def create_distplot_by_state(stat, df, states):
    stat_by_state = {state: remove_outliers(df[stat][df["state"] == state].dropna()) for state in states}
    
    # group data together
    hist_data = list(stat_by_state.values())
    group_labels = list(stat_by_state.keys())

    # create distplot with custom bin_size
    fig = ff.create_distplot(hist_data, group_labels, show_hist=False, bin_size=0.1)
    fig.update_layout(
        title=f"Suburb {stat.replace('_', ' ').title()} Distribution by State", 
        template="seaborn"
    )
    st.plotly_chart(fig)

def create_basic_plot(df_filtered, x, y):
    fig = px.scatter(
        df_filtered, 
        x=x, 
        y=y,
        hover_data={"Suburb": True},
        template="seaborn"
    )
    fig.update_layout(
        #title=f"Suburb {stat.replace('_', ' ').title()} Distribution by State", 
        template="seaborn"
    )
    st.plotly_chart(fig)