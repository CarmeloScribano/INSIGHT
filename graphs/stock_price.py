from ingestor import get_data_frame
from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd
from utils import get_trades_by_type
myDict = {}
df = get_data_frame("Exchange_1")

def get_cancel_request_trades(symbol):
    dff = df[df['Symbol'] == symbol]
    for ind in dff.index:
        order_id = df['OrderID'][ind]
        if df['MessageType'][ind] == "CancelRequest" or df['MessageType'][ind] == "CancelAcknowledged":
            time_stamp = df['TimeStamp'][ind]
            message_type = df['MessageType'][ind]
            subDict = {'TimeStamp':time_stamp,"MessageType":message_type}
            if order_id not in myDict:  
                myDict[order_id] = [subDict]
            else:
                 myDict[order_id].append(subDict)
    return dff  


get_cancel_request_trades("PRQ83")
count = 0
for key, index in myDict.items():
    if count == 0:
        print(key,index)
    count += 1

