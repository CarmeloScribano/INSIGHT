import pandas as pd

def get_dataframe(exchange_json):
    df = pd.read_json(f'data/{exchange_json}.json')
    print(df)

print(get_dataframe("Exchange_2"))


    

