import pandas as pd # for data manipulation
import numpy as np # for data manipulation
from statsmodels.nonparametric.smoothers_lowess import lowess
import os
from scipy import interpolate

import plotly.graph_objects as go # for data visualization
import plotly.express as px # for data visualization
from plotly.subplots import make_subplots


import dash
from dash import Dash, dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from style import *


dash.register_page(__name__, order = 4)


def make_fig(xdata, ydata , x_axis, y_axis):
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Scatter(x = xdata, y = ydata,
                                    mode = 'markers',
                                     name = 'raw data',
                                    marker=dict(size=8,
                                                color = '#EF553B',
                                  line=dict(width=1.5,
                                            color='DarkSlateGrey'),
                                    )), row = 1, col = 1
                        )

    fig.update_xaxes(title_text=x_axis, row=1, col=1, showline = True, showgrid = True, showticklabels = True,
                        linecolor = 'rgb(204,204,204)',
                        linewidth = 2, ticks = 'inside',
                        tickfont = dict( color = 'rgb(82,82,82)') )



    fig.update_yaxes(title_text = y_axis, row =1, col=1,
                     showgrid = True, zeroline = True, showline = True,
                        ticks = 'outside', linecolor = 'rgb(204,204,204)',
                        linewidth = 2
                    )

    fig.update_layout(

    #                 autosize=False,
    #                 width=600,
    #                 height=800,
                    plot_bgcolor = '#fcfaea',
                    font = dict(
                        size = 16,
                        family = 'Arial'
                        ),
        legend=dict(
        orientation="h",

        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1))

    return fig

f_lowess = html.Div(children = [
                dbc.Row(html.P('LOWESS smoothing'), style = {'margin-left':'-5rem', 'fontSize':26}),
                dbc.Row([html.Div('Select the raw data for LOWESS smoothing')],
                style = {'padding': '1rem 0rem', 'fontSize' : 18}),
                dbc.Row([dbc.Input(id = 'lowess_file', style = {'width': 700},
                        value = '', placeholder = 'choose .csv file...')])

                ])

layout = dbc.Container(fluid = False, style = Home_STYLE, children = [
                dcc.Store('lowess_results', data=[]),
                dbc.Row(
                dbc.Col(html.Div(style = {'width': 800, 'margin-left': '10rem'}, children=[

                    html.Div(f_lowess)],))),
                html.Br(),
                html.Div(dcc.Graph( id = 'lowess_fig', figure = make_fig([],[],'Age (kyr)', 'y')),
                        style = {'margin-left':'5rem', 'width': 900},),
                html.Br(),
                dbc.Row(
                        [dbc.Col([html.Div(html.Label('Choose the fraction for smoothing'),
                        style = {'textAlign':'left', 'fontSize':18, 'margin-left':'13rem'}),
                html.Div(dcc.Slider( min = 0, max = 1, step = 0.1,className="margin10",
                            id = 'fraction', value = 0.5),
                        style = {'margin-left':'5rem', 'width': 600})]),

                        dbc.Col([dbc.Button("Save results", id="download_button", outline = True,
                                        color = 'dark', className = 'me-1', n_clicks = 0,
                                        style = {'margin-left':'3rem', 'padding': '1rem 0rem', 'width':200}),
                         dcc.Download(id="download")]
                                )]

                        ),
                html.Br(),
                html.Hr(),

])




@callback(Output('lowess_fig', 'figure'),
            Output('lowess_results', 'data'),
            Input('lowess_file', 'value'),
            Input('fraction', 'value'),
            prevent_initial_call = True
            )

def update_fig(file, frac):



    if os.path.isfile(file):

        data = pd.read_csv(file)
        xdata = data.iloc[:,0]
        ydata = data.iloc[:,1]

        xlabel = 'Age'
        if max(ydata)>100:
            ylabel = 'pCO2 (uatm)'

        if max(ydata)<9 and min(ydata)>6:
            ylabel = 'pH'

        if min(ydata)<4:
            ylabel = 'd13C'

        if not ylabel:
            ylable = 'y'

        fig = make_fig(xdata, ydata, xlabel, ylabel)

        y_lowess = lowess(ydata, xdata, frac = frac)


        fig.add_trace(go.Scatter(x = y_lowess[:,0], y = y_lowess[:,1],
                            mode = 'lines',
                            name = 'Smoothing results',
                            line = dict(color = '#00b4d8', width = 2),
                            ), row = 1, col = 1
                )

        f = interpolate.interp1d(y_lowess[:,0], y_lowess[:,1])
        xnew = np.arange(min(xdata), max(xdata), 200)
        ynew = f(xnew)

        return fig, [xnew, ynew]

    else:
        raise PreventUpdate

@callback(
    Output("download", "data"),
    Input("download_button", "n_clicks"),
    State('lowess_results','data'),
    prevent_initial_call=True,
)
def save_results(n_clicks, data):
    if data != None:
        data = np.array(data).T
        df = pd.DataFrame(data[:,1], index = data[:,0])
        df.index.name = 'Age'

        df.columns = [ 'Proxy value']

        return dcc.send_data_frame(df.to_csv, "smoothing_results.csv")
    else:
        raise PreventUpdate
