from dash import Dash, html, dcc
from graphs.carmGraph import fig

app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='ConUHacks VIII'),

    html.Div(
        className="app-header",
        children=[
            html.Div('Plotly Dash', className="app-header--title")
        ]
    ),

    html.Div(
        children=html.Div([
            html.H1('Overview'),
            html.Div('''
                This is an example of a simple Dash app with
                local, customized CSS.
            '''),
            dcc.Graph(
                id='example-graph',
                figure=fig
            )
        ])
    )
])

if __name__ == '__main__':
    app.run(debug=True)
