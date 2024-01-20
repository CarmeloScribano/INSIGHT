from ingestor import get_data_frame
from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd

df = get_data_frame("Exchange_1")

def get_cancel_request_trades(symbol, request,ack):
    myDict = {}
    dff = df[df['Symbol'] == symbol]
    for ind in dff.index:
        order_id = df['OrderID'][ind]
        if df['MessageType'][ind] == request or df['MessageType'][ind] == ack:
            time_stamp = pd.to_datetime(df['TimeStamp'][ind])
            message_type = df['MessageType'][ind]
            subDict = {'TimeStamp':time_stamp,"MessageType":message_type}
            if order_id not in myDict:  
                myDict[order_id] = [subDict]
            else:
                 myDict[order_id].append(subDict)
    return myDict  



def create_df_from_dict(trades_dict):

    df = pd.DataFrame(columns=['TimeStarted',"Duration"])
    for key, value in trades_dict.items():
       duration = (value[0]['TimeStamp'].timestamp())
       print(duration)
        
maDict = get_cancel_request_trades("PRQ83","CancelRequest","CancelAcknowledged")
create_df_from_dict(maDict)

