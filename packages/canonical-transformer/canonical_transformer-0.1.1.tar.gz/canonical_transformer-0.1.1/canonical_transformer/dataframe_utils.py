import pandas as pd
from .format_utils import capitalize_column_names_in_df
import json
import os


def map_df_to_data(df, capitalize=False):
    df = df.reset_index() if df.index.name else df
    df = df.fillna('')    
    if capitalize:
        df = capitalize_column_names_in_df(df)
    data = df.to_dict(orient='records')
    return data

def map_data_to_df(data):
    df = pd.DataFrame(data)
    return df