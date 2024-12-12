from .data_utils import map_df_to_data

def transfrom_df_to_data_fits_universal_dataframe(df, rnd=2):
    df = round(df, rnd)
    data = map_df_to_data(df, capitalize=True)
    return data
    