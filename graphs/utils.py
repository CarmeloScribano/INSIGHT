def get_trades_by_type(df, msg_type):
    return df[df['MessageType'] == msg_type]