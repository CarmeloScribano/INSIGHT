import pandas as pd

def get_data_frame(exchange_json):
    df = pd.read_json(f'data/{exchange_json}.json')
<<<<<<<< HEAD:graphs/ingestor.py
    return df
========
    return df   

    

>>>>>>>> d3cad0aea8426e1e7e51c010cc474f13bd1ebf04:utils/ingestor.py
