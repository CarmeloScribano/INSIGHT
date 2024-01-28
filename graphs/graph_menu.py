def set_trade_graph(trade_class, acknowledged_class, fill_class, cancelled_class):
    new_trade = trade_class.replace('hidden', '').strip()
    new_acknowledged = acknowledged_class + ' hidden'
    new_fill = fill_class + ' hidden'
    new_cancelled = cancelled_class + ' hidden'
    return new_trade, new_acknowledged, new_fill, new_cancelled

def set_acknowledged_graph(trade_class, acknowledged_class, fill_class, cancelled_class):
    new_trade = trade_class + ' hidden'
    new_acknowledged = acknowledged_class.replace('hidden', '').strip()
    new_fill = fill_class + ' hidden'
    new_cancelled = cancelled_class + ' hidden'
    return new_trade, new_acknowledged, new_fill, new_cancelled

def set_fill_graph(trade_class, acknowledged_class, fill_class, cancelled_class):
    new_trade = trade_class + ' hidden'
    new_acknowledged = acknowledged_class + ' hidden'
    new_fill = fill_class.replace('hidden', '').strip()
    new_cancelled = cancelled_class + ' hidden'
    return new_trade, new_acknowledged, new_fill, new_cancelled

def set_cancelled_graph(trade_class, acknowledged_class, fill_class, cancelled_class):
    new_trade = trade_class + ' hidden'
    new_acknowledged = acknowledged_class + ' hidden'
    new_fill = fill_class + ' hidden'
    new_cancelled = cancelled_class.replace('hidden', '').strip()
    return new_trade, new_acknowledged, new_fill, new_cancelled