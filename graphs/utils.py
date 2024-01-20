def get_acked_trades(df, msg_type):
    return df[df['MessageType'] == msg_type]