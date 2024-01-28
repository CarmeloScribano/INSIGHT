current_graph = 1


def set_graph(graph):
    global current_graph
    current_graph = graph


def get_current_graph():
    global current_graph
    return current_graph


def set_trade_graph(
        trade_class, acknowledged_class, fill_class, cancelled_class,
        trade_menu_class, acknowledged_menu_class, fill_menu_class, cancelled_menu_class,
        trade_selected_class, acknowledged_selected_class, fill_selected_class, cancelled_selected_class
    ):
    
    # Sets the charts and menus to default values to facilitate the remainder of the function
    trade_class, acknowledged_class, fill_class, cancelled_class = clear_transitions(trade_class, acknowledged_class, fill_class, cancelled_class)
    new_trade, new_acknowledged, new_fill, new_cancelled = trade_class, acknowledged_class, fill_class, cancelled_class

    if get_current_graph() == 2:
        new_trade = trade_class.replace('hidden', 'fade-left').strip()
        new_acknowledged = acknowledged_class + ' hidden'
    elif get_current_graph() == 3:
        new_trade = trade_class.replace('hidden', 'fade-left').strip()
        new_fill = fill_class + ' hidden'
    elif get_current_graph() == 4:
        new_trade = trade_class.replace('hidden', 'fade-right').strip()
        new_cancelled = cancelled_class + ' hidden'

    # Set the menu links to the appropriate style
    new_trade_menu = trade_menu_class + ' active-chart'
    new_acknowledged_menu = acknowledged_menu_class.replace('active-chart', '').strip()
    new_fill_menu = fill_menu_class.replace('active-chart', '').strip()
    new_cancelled_menu = cancelled_menu_class.replace('active-chart', '').strip()

    # Set the menu select circle to the appropriate style
    new_trade_select = trade_selected_class.replace('hidden', '').strip()
    new_acknowledged_select = acknowledged_selected_class + ' hidden'
    new_fill_select = fill_selected_class + ' hidden'
    new_cancelled_select = cancelled_selected_class + ' hidden'

    set_graph(1)

    return (
            new_trade, new_acknowledged, new_fill, new_cancelled, 
            new_trade_menu, new_acknowledged_menu, new_fill_menu, new_cancelled_menu, 
            new_trade_select, new_acknowledged_select, new_fill_select, new_cancelled_select
        )

def set_acknowledged_graph(
        trade_class, acknowledged_class, fill_class, cancelled_class,
        trade_menu_class, acknowledged_menu_class, fill_menu_class, cancelled_menu_class,
        trade_selected_class, acknowledged_selected_class, fill_selected_class, cancelled_selected_class
    ):

    # Sets the charts and menus to default values to facilitate the remainder of the function
    trade_class, acknowledged_class, fill_class, cancelled_class = clear_transitions(trade_class, acknowledged_class, fill_class, cancelled_class)
    new_trade, new_acknowledged, new_fill, new_cancelled = trade_class, acknowledged_class, fill_class, cancelled_class

    if get_current_graph() == 1:
        new_trade = trade_class + ' hidden'
        new_acknowledged = acknowledged_class.replace('hidden', 'fade-right').strip()
    elif get_current_graph() == 3:
        new_acknowledged = acknowledged_class.replace('hidden', 'fade-left').strip()
        new_fill = fill_class + ' hidden'
    elif get_current_graph() == 4:
        new_acknowledged = acknowledged_class.replace('hidden', 'fade-left').strip()
        new_cancelled = cancelled_class + ' hidden'

    # Set the menu links to the appropriate style
    new_trade_menu = trade_menu_class.replace('active-chart', '').strip()
    new_acknowledged_menu = acknowledged_menu_class + ' active-chart'
    new_fill_menu = fill_menu_class.replace('active-chart', '').strip()
    new_cancelled_menu = cancelled_menu_class.replace('active-chart', '').strip()
    
    # Set the menu select circle to the appropriate style
    new_trade_select = trade_selected_class + ' hidden'
    new_acknowledged_select = acknowledged_selected_class.replace('hidden', '').strip()
    new_fill_select = fill_selected_class + ' hidden'
    new_cancelled_select = cancelled_selected_class + ' hidden'

    set_graph(2)

    return (
            new_trade, new_acknowledged, new_fill, new_cancelled, 
            new_trade_menu, new_acknowledged_menu, new_fill_menu, new_cancelled_menu, 
            new_trade_select, new_acknowledged_select, new_fill_select, new_cancelled_select
        )

def set_fill_graph(
        trade_class, acknowledged_class, fill_class, cancelled_class,
        trade_menu_class, acknowledged_menu_class, fill_menu_class, cancelled_menu_class,
        trade_selected_class, acknowledged_selected_class, fill_selected_class, cancelled_selected_class
    ):

    # Sets the charts and menus to default values to facilitate the remainder of the function
    trade_class, acknowledged_class, fill_class, cancelled_class = clear_transitions(trade_class, acknowledged_class, fill_class, cancelled_class)
    new_trade, new_acknowledged, new_fill, new_cancelled = trade_class, acknowledged_class, fill_class, cancelled_class

    if get_current_graph() == 1:
        new_trade = trade_class + ' hidden'
        new_fill = fill_class.replace('hidden', 'fade-right').strip()
    elif get_current_graph() == 2:
        new_acknowledged = acknowledged_class + ' hidden'
        new_fill = fill_class.replace('hidden', 'fade-right').strip()
    elif get_current_graph() == 4:
        new_fill = fill_class.replace('hidden', 'fade-left').strip()
        new_cancelled = cancelled_class + ' hidden'

    # Set the menu links to the appropriate style
    new_trade_menu = trade_menu_class.replace('active-chart', '').strip()
    new_acknowledged_menu = acknowledged_menu_class.replace('active-chart', '').strip()
    new_fill_menu = fill_menu_class + ' active-chart'
    new_cancelled_menu = cancelled_menu_class.replace('active-chart', '').strip()

    # Set the menu select circle to the appropriate style
    new_trade_select = trade_selected_class + ' hidden'
    new_acknowledged_select = acknowledged_selected_class + ' hidden'
    new_fill_select = fill_selected_class.replace('hidden', '').strip()
    new_cancelled_select = cancelled_selected_class + ' hidden'

    set_graph(3)

    return (
            new_trade, new_acknowledged, new_fill, new_cancelled, 
            new_trade_menu, new_acknowledged_menu, new_fill_menu, new_cancelled_menu, 
            new_trade_select, new_acknowledged_select, new_fill_select, new_cancelled_select
        )

def set_cancelled_graph(
        trade_class, acknowledged_class, fill_class, cancelled_class,
        trade_menu_class, acknowledged_menu_class, fill_menu_class, cancelled_menu_class,
        trade_selected_class, acknowledged_selected_class, fill_selected_class, cancelled_selected_class
    ):
    
    # Sets the charts and menus to default values to facilitate the remainder of the function
    trade_class, acknowledged_class, fill_class, cancelled_class = clear_transitions(trade_class, acknowledged_class, fill_class, cancelled_class)
    new_trade, new_acknowledged, new_fill, new_cancelled = trade_class, acknowledged_class, fill_class, cancelled_class
    
    if get_current_graph() == 1:
        new_trade = trade_class + ' hidden'
        new_cancelled = cancelled_class.replace('hidden', 'fade-left').strip()
    elif get_current_graph() == 2:
        new_acknowledged = acknowledged_class + ' hidden'
        new_cancelled = cancelled_class.replace('hidden', 'fade-right').strip()
    elif get_current_graph() == 3:
        new_fill = fill_class + ' hidden'
        new_cancelled = cancelled_class.replace('hidden', 'fade-right').strip()

    # Set the menu links to the appropriate style
    new_trade_menu = trade_menu_class.replace('active-chart', '').strip()
    new_acknowledged_menu = acknowledged_menu_class.replace('active-chart', '').strip()
    new_fill_menu = fill_menu_class.replace('active-chart', '').strip()
    new_cancelled_menu = cancelled_menu_class + ' active-chart'

    # Set the menu select circle to the appropriate style
    new_trade_select = trade_selected_class + ' hidden'
    new_acknowledged_select = acknowledged_selected_class + ' hidden'
    new_fill_select = fill_selected_class + ' hidden'
    new_cancelled_select = cancelled_selected_class.replace('hidden', '').strip()

    set_graph(4)

    return (
            new_trade, new_acknowledged, new_fill, new_cancelled, 
            new_trade_menu, new_acknowledged_menu, new_fill_menu, new_cancelled_menu, 
            new_trade_select, new_acknowledged_select, new_fill_select, new_cancelled_select
        )


def clear_transitions(trade_class, acknowledged_class, fill_class, cancelled_class):
    trade_class = trade_class.replace('fade-right', '').strip()
    acknowledged_class = acknowledged_class.replace('fade-right', '').strip()
    fill_class = fill_class.replace('fade-right', '').strip()
    cancelled_class = cancelled_class.replace('fade-right', '').strip()
    
    trade_class = trade_class.replace('fade-left', '').strip()
    acknowledged_class = acknowledged_class.replace('fade-left', '').strip()
    fill_class = fill_class.replace('fade-left', '').strip()
    cancelled_class = cancelled_class.replace('fade-left', '').strip()

    return trade_class, acknowledged_class, fill_class, cancelled_class
