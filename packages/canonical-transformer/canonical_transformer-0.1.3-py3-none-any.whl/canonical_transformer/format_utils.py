
def rename_columns(df, mapping):
    df = df.rename(columns=mapping)
    df.columns = [col.upper() for col in df.columns]
    return df

def capitalize_column_names_in_df(df):
    cols_ref = df.columns
    df.columns = [col.upper() for col in cols_ref]
    return df