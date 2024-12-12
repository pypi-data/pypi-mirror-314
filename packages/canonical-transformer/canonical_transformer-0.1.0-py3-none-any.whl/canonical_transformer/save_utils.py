import os
import json
from .data_utils import map_df_to_data


def save_df_as_csv(df, file_folder, file_name):
    df.to_csv(os.path.join(file_folder, file_name), index=False)
    print(f"| Saved csv to {os.path.join(file_folder, file_name)}")
    return None

def save_data_as_json(data, file_folder, file_name):
    with open(os.path.join(file_folder, file_name), 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"| Saved json to {os.path.join(file_folder, file_name)}")
    return None

def save_df_as_json(df, file_folder, file_name):
    data = map_df_to_data(df)
    
    print("| Transformed df to json data")
    save_data_as_json(data, file_folder, file_name)
    print(f"| Saved json to {os.path.join(file_folder, file_name)}")
    return None

