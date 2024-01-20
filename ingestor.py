import pandas as pd

def get_data_frame(exchange_json):
    df = pd.read_json(f'data/{exchange_json}.json')
    return df


    

