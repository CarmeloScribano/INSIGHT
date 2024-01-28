def set_trade_graph(trade_class, acknowledged_class, fill_class, cancelled_class,
        trade_selected_class, acknowledged_selected_class, fill_selected_class, cancelled_selected_class):
    new_trade = trade_class.replace('hidden', '').strip()
    new_acknowledged = acknowledged_class + ' hidden'
    new_fill = fill_class + ' hidden'
    new_cancelled = cancelled_class + ' hidden'

    new_trade_select = trade_selected_class.replace('hidden', '').strip()
    new_acknowledged_select = acknowledged_selected_class + ' hidden'
    new_fill_select = fill_selected_class + ' hidden'
    new_cancelled_select = cancelled_selected_class + ' hidden'

    return new_trade, new_acknowledged, new_fill, new_cancelled, new_trade_select, new_acknowledged_select, new_fill_select, new_cancelled_select


def set_acknowledged_graph(trade_class, acknowledged_class, fill_class, cancelled_class,
        trade_selected_class, acknowledged_selected_class, fill_selected_class, cancelled_selected_class):
    new_trade = trade_class + ' hidden'
    new_acknowledged = acknowledged_class.replace('hidden', '').strip()
    new_fill = fill_class + ' hidden'
    new_cancelled = cancelled_class + ' hidden'

    new_trade_select = trade_selected_class + ' hidden'
    new_acknowledged_select = acknowledged_selected_class.replace('hidden', '').strip()
    new_fill_select = fill_selected_class + ' hidden'
    new_cancelled_select = cancelled_selected_class + ' hidden'

    return new_trade, new_acknowledged, new_fill, new_cancelled, new_trade_select, new_acknowledged_select, new_fill_select, new_cancelled_select


def set_fill_graph(trade_class, acknowledged_class, fill_class, cancelled_class,
        trade_selected_class, acknowledged_selected_class, fill_selected_class, cancelled_selected_class):
    new_trade = trade_class + ' hidden'
    new_acknowledged = acknowledged_class + ' hidden'
    new_fill = fill_class.replace('hidden', '').strip()
    new_cancelled = cancelled_class + ' hidden'

    new_trade_select = trade_selected_class + ' hidden'
    new_acknowledged_select = acknowledged_selected_class + ' hidden'
    new_fill_select = fill_selected_class.replace('hidden', '').strip()
    new_cancelled_select = cancelled_selected_class + ' hidden'

    return new_trade, new_acknowledged, new_fill, new_cancelled, new_trade_select, new_acknowledged_select, new_fill_select, new_cancelled_select


def set_cancelled_graph(trade_class, acknowledged_class, fill_class, cancelled_class,
        trade_selected_class, acknowledged_selected_class, fill_selected_class, cancelled_selected_class):
    new_trade = trade_class + ' hidden'
    new_acknowledged = acknowledged_class + ' hidden'
    new_fill = fill_class + ' hidden'
    new_cancelled = cancelled_class.replace('hidden', '').strip()

    new_trade_select = trade_selected_class + ' hidden'
    new_acknowledged_select = acknowledged_selected_class + ' hidden'
    new_fill_select = fill_selected_class + ' hidden'
    new_cancelled_select = cancelled_selected_class.replace('hidden', '').strip()

    return new_trade, new_acknowledged, new_fill, new_cancelled, new_trade_select, new_acknowledged_select, new_fill_select, new_cancelled_select
