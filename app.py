from dash import Dash, html, dcc
from graphs.carmGraph import fig

app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.Div(
            className="sidemenu",
            children=[
                html.Div(className="graph1"),
                html.Div(className="graph2"),
                html.Div(className="graph3")
            ]
        ),
        
        html.Div(
            className="main",
            children=[
                html.Div(
                    className="header",
                    children=[
                        html.P('ConUHacks VIII')
                    ]
                ), 

                html.Div(
                    className="grid-container",
                    children=[
                        html.Div(
                            className="graph1", 
                            children=(
                                dcc.Graph(
                                id='example-graph',
                                figure=fig
                                )
                            )
                        ),
                        html.Div(
                            className="graph2", 
                            children=(
                                dcc.Graph(
                                id='example-graph',
                                figure=fig
                                )
                            )
                        ),
                        html.Div(
                            className="graph3", 
                            children=(
                                dcc.Graph(
                                id='example-graph',
                                figure=fig
                                )
                            )
                        )
                    ]
                )
            ]
        )
    ]
)

if __name__ == '__main__':
    app.run(debug=True)
