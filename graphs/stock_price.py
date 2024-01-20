import json
from ingestor import get_data_frame
from utils import get_trades_by_type

df = get_data_frame("Exchange_1")

new_order_requests = get_trades_by_type(df=df, msg_type="CancelRequest").sort_values(by='TimeStamp')
order_acknowledges = df.groupby(['OrderID']).apply(lambda x: x[x["MessageType"] == "CancelAcknowledged"])
new_order_requests.reset_index(drop = True, inplace = True)
order_acknowledges.reset_index(drop = True, inplace = True)
merged_pd = new_order_requests.merge(order_acknowledges, on="OrderID")[["TimeStamp_x", "TimeStamp_y"]]
merged_pd["OrderAcknowledgedDuration"] = merged_pd["TimeStamp_y"] - merged_pd["TimeStamp_x"]
print(merged_pd)

