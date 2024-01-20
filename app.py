from dash import Dash, html, dcc
from dash_iconify import DashIconify
from graphs.carmGraph import fig

app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.Div(
            className="sidemenu",
            children=[
                html.Div(
                    children= [
                        DashIconify(
                        icon="ion:logo-github",
                        width=30,
                        ),

                        DashIconify(
                        icon="ion:logo-github",
                        width=30,
                        ),

                        DashIconify(
                        icon="ion:logo-github",
                        width=30,
                        ),

                        DashIconify(
                        icon="ion:logo-github",
                        width=30,
                        ),

                        DashIconify(
                        icon="ion:logo-github",
                        width=30,
                        )
                    ]
                )                
            ]
        ),
        
        html.Div(
            className="main",
            children=[
                html.Div(
                    children=[
                        html.P(
                            className="greeting",
                            children=[
                                'Hello, John Doe'
                            ]
                        ),

                        html.P(
                            className="greeting-subtitle",
                            children=[
                                'View your financial data here!'
                            ]
                        )
                    ]
                ),

                html.Div(
                    className="main-container",
                    children=[
                        html.Div(
                            className="graph1", 
                            children=(
                                dcc.Graph(
                                id='example-graph1',
                                figure=fig
                                )
                            )
                        ),

                        html.Div(
                            className="graph2", 
                            children=(
                                dcc.Graph(
                                id='example-graph2',
                                figure=fig
                                )
                            )
                        ),

                        html.Div(
                            className="graph3", 
                            children=(
                                dcc.Graph(
                                id='example-graph3',
                                figure=fig
                                )
                            )
                        )
                    ]
                )
            ]
        ),

        html.Div(
            className="static-data",
            children=[
                html.Div(
                    className="static-data-container",
                    children=[
                        html.Div(
                            children=(
                                dcc.Graph(
                                id='static-data-graph1',
                                figure=fig
                                )
                            )
                        )
                    ]
                )
            ]
        ),
    ]
)

if __name__ == '__main__':
    app.run(debug=True)
