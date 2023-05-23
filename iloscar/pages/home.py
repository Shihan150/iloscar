import dash
from dash import html, dcc
from style import *

dash.register_page(__name__, path='/', order = 1)

link = "https://doi.org/10.5194/gmd-5-149-2012"
layout = html.Div(children=[
    html.Div(style = Home_STYLE, children =[
    html.P("The LOSCAR model is designed to efficiently compute the partitioning of carbon between ocean, atmosphere, and sediments on time scales ranging from centuries to millions of years. "),
    html.Br(),
    html.P(["For a detailed model description, please refer to ",
            html.Label([ '',html.A('Zeebe (2012)', href=link)])]),
    html.Br(),
    html.P("This is the iLOSCAR-0.1 written in Python, which allows users to run the model from the website interface."),
    html.Br(),
    html.P("Author"),
    html.P(" Shihan Li | Department of Oceanography, Texas A&M University, College Station, Texas, 77843, USA"),
    html.Br(),
    html.P('Contributors'),
    html.P('Dr. Richard E. Zeebe | Department of Oceanography, University of Hawaii, Manoa Honolulu, HI 96822, USA'),
    html.P('Dr. Shuang Zhang | Department of Oceanography, Texas A&M University, College Station, Texas, 77843, USA'),
    ])

])
