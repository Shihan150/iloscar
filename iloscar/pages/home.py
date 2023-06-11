import dash
from dash import html, dcc
from style import *

dash.register_page(__name__, path='/', order = 1)

link_chen = 'https://www.pnas.org/doi/10.1073/pnas.2115231119'
link_loscar = "https://doi.org/10.5194/gmd-5-149-2012"
link_tutorial = 'https://github.com/Shihan150/iloscar/blob/main/README.md#example'
link_hull = 'https://www.science.org/doi/full/10.1126/science.aay5055'
link_papa = 'https://pubs.geoscienceworld.org/gsa/geology/article-abstract/50/4/511/611421/Quantifying-volcanism-and-organic-carbon-burial?redirectedFrom=fulltext'



layout = html.Div(children=[
    html.Div(style = Home_STYLE, children =[
    html.H1("iLOSCAR"),
    html.P("iLOSCAR is a software developed on the foundation of the Long-term Ocean-atmosphere-Sediment CArbon cycle Reservoir (LOSCAR) Model (Zeebe, 2012)."),
    html.Br(),
    html.H2("LOSCAR Model"),
    html.P(["The LOSCAR model, written in C, was designed for efficient computation of carbon partitioning among the ocean, atmosphere, and sediments over timescales ranging from centuries to millions of years. ",
        "For a detailed model description, please refer to ",
            html.Label([ '',html.A('Zeebe (2012)', href=link_loscar, target = '_blank'), '.'])]),
    html.P('The model has been extensively used in the estimation of carbon emissions during various hyperthermal events, as evidenced by numerous studies:'),
    html.Ul([
        html.Li(html.Label([ html.A('Chen et al., 2022', href=link_chen, target = '_blank'),  ''])),
        html.Li(html.Label([ html.A('Hull et al., 2020', href=link_hull, target = '_blank'),  ''])),
        html.Li(html.Label([ html.A('Papadomanolaki et al., 2022', href=link_papa, target = '_blank'),  ''])),
    ]),
    html.Br(),
    html.H2("iLOSCAR Development"),
    html.P("We have enhanced LOSCAR by developing iLOSCAR using Python, an open-source programming language. iLOSCAR offers a user-friendly web interface that enables users to interactively adjust model parameters and conduct experiments."),
    html.P([html.Label([ html.A('Examples', href=link_tutorial, target = '_blank'),  '']), ' ', ' are provided for a quick start.']),
    html.Li(html.Span(html.I("Foward Model", style = {'fontSize':24}))),
    html.P("iLOSCAR features a forward model that emulates the original LOSCAR model. Click the 'Forward' tab to start."),
    html.Li(html.Span(html.I("Inverse Model", style = {'fontSize':24}))),
    html.P("The software also includes an inverse model which extends beyond the capabilities of the original LOSCAR. This inverse model calculates the emission trajectory constrained by proxy records in a single run. Click the 'Inverse' tab to start."),
    html.Li(html.Span(html.I("Smoothing function", style = {'fontSize':24}))),
    html.P("The software also includes A LOWESS smoothing function. Users have the flexibility to upload data files and manually adjust the hyperparamter that controls the window fraction used in the LOWESS algorithm. Click the 'Smoothing' tab to start."),

    html.Br(),
    # html.P("Author"),
    # html.P(" Shihan Li | Department of Oceanography, Texas A&M University, College Station, Texas, 77843, USA"),
    # html.Br(),
    # html.P('Contributors'),
    # html.P('Dr. Richard E. Zeebe | Department of Oceanography, University of Hawaii, Manoa Honolulu, Hawaii, 96822, USA'),
    # html.P('Dr. Shuang Zhang | Department of Oceanography, Texas A&M University, College Station, Texas, 77843, USA'),
    ])

])
