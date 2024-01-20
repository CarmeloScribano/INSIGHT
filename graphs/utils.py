def get_trades_by_type(df, msg_type):
    return df[df['MessageType'] == msg_type]

def get_df_rows_by_symbol(df, symbol):
    return df[df['Symbol'] == symbol]