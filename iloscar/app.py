import dash
from dash import html, dcc, DiskcacheManager, CeleryManager
from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform
import dash_bootstrap_components as dbc
from style import *
import diskcache

cache = diskcache.Cache('./cache')

external_stylesheets = [dbc.themes.SPACELAB]
# [
#     {
#         "href": (
#             "https://fonts.googleapis.com/css2?"
#             "family=Lato:wght@400;700&display=swap"
#         ),
#         "rel": "stylesheet",
#     },]
# [dbc.themes.SPACELAB]
app = DashProxy(__name__, use_pages=True, external_stylesheets=external_stylesheets,
    background_callback_manager = DiskcacheManager(cache),
    transforms=[MultiplexerTransform()])
sidebar = dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.Div(page["name"], className="ms-2"),
                    ],
                    href=page["path"],
                    active="exact",
                )
                for page in dash.page_registry.values()
            ],
            vertical=True,
            pills=True,
            className="bg-light",
            style = {'fontSize': 20}
)


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div("Welcom to iLOSCAR",
                         style={'fontSize':50, 'textAlign':'center'}))
    ]),

    html.Hr(),

    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),

            dbc.Col(
                [
                    dash.page_container
                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10)
        ]
    )
], fluid=True)


if __name__ == "__main__":
    app.run(debug=True, port = '7777')
