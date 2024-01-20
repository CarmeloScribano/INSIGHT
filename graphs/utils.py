def get_trades_by_type(df, msg_type):
    return df[df['MessageType'] == msg_type]

def get_duration_of_x_and_y(df, msg_x, msg_y):
    msg_x_df = get_trades_by_type(df=df, msg_type=msg_x).sort_values(by='TimeStamp')
    msg_Y_df = df.groupby(['OrderID']).apply(lambda x: x[x["MessageType"] == msg_y])
    msg_x_df.reset_index(drop = True, inplace = True)
    msg_Y_df.reset_index(drop = True, inplace = True)
    merged_pd = msg_x_df.merge(msg_Y_df, on="OrderID")[["TimeStamp_x", "TimeStamp_y"]]
    merged_pd["XYDuration"] = merged_pd["TimeStamp_y"] - merged_pd["TimeStamp_x"]
    return merged_pd
