import pandas as pd

def merge_suburb(df_suburbs, df_prop, state):
    suburbs = df_suburbs["name"][df_suburbs["state"] == state].unique()
    df_filtered = df_prop[df_prop["Suburb"].isin(suburbs)].merge(df_suburbs, left_on='Suburb', right_on='name')
    return df_filtered