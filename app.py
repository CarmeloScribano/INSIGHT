from dash import Dash, html, dcc
from graphs.carmGraph import fig

app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children=html.P('ConUHacks VIII')),

    html.Div(
        className="grid-container",
        children=[
            html.Div(className="item1 bg-black"),
            html.Div(className="item2 bg-red"),
            html.Div(className="item3 bg-blue"),
            html.Div(className="item4 bg-orange"),
            html.Div(className="item5 bg-green")
        ]
    )
])

if __name__ == '__main__':
    app.run(debug=True)
