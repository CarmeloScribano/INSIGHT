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
                html.P(
                    className="greeting",
                    children='Hello John Doe'
                ),

                html.Div(
                    className="grid-container",
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
        )
    ]
)

if __name__ == '__main__':
    app.run(debug=True)
