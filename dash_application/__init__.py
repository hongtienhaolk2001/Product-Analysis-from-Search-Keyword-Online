import dash
from dash import dcc, html


def create_dash_application(flask_app):
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    """
    external_stylesheets = [
    {
    "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    """

    dash_app = dash.Dash(server=flask_app, name="Dashboard",
                         url_base_pathname="/dash/", external_stylesheets=external_stylesheets)
    #dash_app.config['suppress_callback_exceptions'] = True
    dash_app.layout = html.Div(children=[
        dcc.Location(id="url", refresh=False),
        html.Div(id="output-div"),
    ])

    return dash_app


def create_dash_application_pie(flask_app):
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    """
    external_stylesheets = [
    {
    "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    """

    dash_app = dash.Dash(server=flask_app, name="Dashboard",
                         url_base_pathname="/dash/piechart/", external_stylesheets=external_stylesheets)
    #dash_app.config['suppress_callback_exceptions'] = True
    dash_app.layout = html.Div(children=[
        dcc.Location(id="url", refresh=False),
        html.Div(id="output-div"),
    ])

    return dash_app


def create_dash_application_line(flask_app):
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    """
    external_stylesheets = [
    {
    "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    """

    dash_app = dash.Dash(server=flask_app, name="Dashboard",
                         url_base_pathname="/dash/linechart/", external_stylesheets=external_stylesheets)
    #dash_app.config['suppress_callback_exceptions'] = True
    dash_app.layout = html.Div(children=[
        dcc.Location(id="url", refresh=False),
        html.Div(id="output-div"),
    ])
    """
        @dash_app.callback(Output(component_id="output-div", component_property="children"),
                       Input(component_id="url", component_property="pathname"))
    def update(pathname):
        base = 'caphe_sen.xlsx'
        if pathname == "/dash/linechart":
            dash_app.layout =  linechart_layout(base)
        elif pathname == "/dash/piechart":
            dash_app.layout =  piechart_layout(base)
        else:
            dash_app.layout =  home_layout()
        #else:
        #    dash_app.layout =  piechart_layout(base)
    """

    return dash_app
