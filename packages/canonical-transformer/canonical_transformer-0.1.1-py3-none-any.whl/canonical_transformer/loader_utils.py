import json

def load_json_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


