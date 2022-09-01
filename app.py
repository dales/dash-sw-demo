import json
from dash import Dash, html, Input, Output, State, ALL, ctx, exceptions, dcc
import dash_bootstrap_components as dbc
from flask import send_file, Flask

DRAGULA_CSS = "https://cdnjs.cloudflare.com/ajax/libs/dragula/3.6.6/dragula.min.css"

app_flask = Flask(__name__)

app = Dash(__name__,
           server=app_flask,
           external_stylesheets=[
               dbc.themes.BOOTSTRAP,
               dbc.icons.FONT_AWESOME,
               DRAGULA_CSS
           ],
           external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/dragula/3.6.6/dragula.min.js"])


@app_flask.route("/service_worker")
def service_worker():
    file_name = "serviceworker.js"
    return send_file(file_name)


def in_card(func):
    def inner(*args, **kwargs):
        return dbc.Card(
            dbc.CardBody(children=[html.I(className="fa fa-times close-button"),html.I(className="fa fa-bars drag-handle")] + [func(*args, **kwargs)],
                         className="d-relative")
        )
    return inner


@in_card
def get_heatmap(index):
    return html.H1(f"Heatmap {index}")


@in_card
def get_table(index):
    return html.H1(f"Table {index}")


@in_card
def get_chart(index):
    return html.H1(f"Chart {index}")


def get_view_choice_list():

    actions = ["Heatmap", "Table", "Chart"]

    return dbc.Card(
        dbc.CardBody(
            [
                html.H1("View Choice"),
                html.Div([
                    html.Div(
                        children=[
                            dbc.Button(name, outline=True, color="secondary",
                                       className="me-1 view-button", id={"type": "view-action", "index": i}) for i, name
                            in
                            enumerate(actions)
                        ],
                        id="view-selectors",
                        className="d-grid gap-2")

                ])
            ],
            className="full-height")
    )


def get_view_list():
    return dbc.Card(
        dbc.CardBody(
            [
                html.H1("View List"),
                html.Div(children=[
                ], className="view-list d-flex flex-column gap-2 mx-3", id="view-list",)
            ],
            className="full-height")
    )


def get_layout():
    return dbc.Container(
        dbc.Row(
            [
                dbc.Col(get_view_choice_list(), width=3),
                dbc.Col(get_view_list(), width=9),
            ]
        ),
        className="p-3",
        fluid=True
    )

# ======================
# CALLBACKS
# ======================


@app.callback(Output("view-list", 'children'),
              Input({'type': 'view-action', 'index': ALL}, 'n_clicks'),
              [State('view-list', 'children'), State({'type': 'view-action', 'index': ALL}, 'children')],
              prevent_initial_call=True)
def add_plugin(view_clicked, views, view_buttons):
    if not any(view_clicked):
        raise exceptions.PreventUpdate
    clicked_id = json.loads(ctx.triggered[0]["prop_id"].split(".")[0])["index"]
    counter =  max(views or [0]) + 1
    triggered_index = clicked_id

    view_map = {
        "Heatmap":  get_heatmap,
        "Table": get_table,
        "Chart": get_chart
    }

    plugin_name = view_buttons[triggered_index]

    if plugin_name not in view_map:
        raise exceptions.PreventUpdate

    return [dbc.Row(view_map[plugin_name](counter), id={"type": "view-row", "index": counter})]









app.layout = get_layout

if __name__ == "__main__":
    app.run_server(debug=True, port=8040)
