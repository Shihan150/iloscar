import dash
from dash import  Input, Output, dcc, html, Dash, dash_table, html, callback, State, ctx
from dash.dash_table.Format import Format
import dash_bootstrap_components as dbc
from collections import OrderedDict
import pandas as pd
from dash.exceptions import PreventUpdate

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from style import *
from iLOSCAR_backend import init_start, model_run, wo_results

dash.register_page(__name__, order = 2)

df_mode = pd.DataFrame(OrderedDict([
    ('Value', [0,1,1,1,0]),
    ('Parameter', ['PALEO', 'Sediment', 'LOADFLAG', 'Ocean temperature change', 'Save ystart']),
    ('Options', [ '1/0', '1/0', '1/0', '1/0', '1/0']),
    ('Comment', [ '1: paleo setup; \n 0: modern setup', '1: sediment box on; \n 0: sediment box off',
     '1: load initial settings from an external file; \n 0: off','1: ocean temperature change (co2-sensitivity) ON \n 0: Off',
     '1: the experiment aim is to autospin to the steady state and the system variables at t=tfinal will be saved \n 0: off.'
         ]),

]))

df_param = pd.DataFrame(OrderedDict([
    ('Value', [0,2e5,280, 280,
            0.8,1.8, 6.1,1.0,
            5, 12, 1.5, -4.0 ,
            20,10.3e-3, 53.0e-3, 3,
            0.2, 0.4]),
    ('Parameter', ['t0', 'tfinal', 'pCO2_ref', 'pCO2_initial',
                    'fepl', 'eph', 'rrain', 'fsh',
                    'silicate weathering0', 'carbonate weathering0',  'd13c carbonate weathering', 'd13c volcanic',
                    'Conveyor Transport',  'Ca_concentration', 'Mg concentration', 'climate sensitvity', 'nsi', 'ncc']),
   ('Unit', ['yr', 'yr', 'uatm', 'uatm',
              '-', 'mol m-2 yr-1', '-', '-',
              '10^12 mol yr-1', '10^12 mol yr-1', 'per mil','per mil',
              'Sv',  'mol/kg', 'mol/kg', '-', '-', '-']),

    ('Comment', [ 'start time (yr) for the experiment', 'end time (yr) for the experiment', 'pCO2 reference', 'steady-state pCO2',
            'biopump-efficiency', 'high-latitude carbon export', 'rain ratio', 'raise shelf rain relative to deep rain',
        'CaSiO3 weathering flux (initial)', 'CaCO3 weathering flux (initial)', 'd13c carbonate weathering', 'd13c volcanic degassing',
        'thermalhaline transport', 'oceanic Ca concentration', 'oceanic Mg concentration', 'default OCN temperature change per double pCO2', 'silicate weathering exponent',
        'carbonate weathering exponent'

    ]),
]))

df_carbon_emission = pd.DataFrame(OrderedDict([
    ('Value', [0,1000,-55,0, 3000]),
    ('Parameter', ['emission pattern', 'emission amount', 'd13c emission',
                   'emission start', 'emission duration']),
    ('Unit', [ '3/2/1/0', 'Gt', 'per mil', 'yr', 'yr']),
    ('Comment', [ f'3: emission scenario with time-dependant d13c \n 2: emission scenario from the external files \n 1:carbon emission in uniform distribution \n 0: no carbon emission',
    'total amount of carbon input, \n only useful when "emission pattern" == 1', 'd13c of input carbon, \n only useful when "emission pattern" == 1', 'start year for the emission, \n only useful when "emission pattern" == 1', 'duration for the emission, \n only useful when "emission pattern" == 1',
]),

]))

df_file = pd.DataFrame(OrderedDict([
    ('File name', ['./preind_steady.dat', './pulse_emi.dat', './preind_steady.dat']),
    ('Parameter', ['Initial steady state file name',
                   'Time-resolved carbon input ',
                   'File to save the final modeling results']),
    ('Comment', [ 'initial steady state file, \n required only when LOADFLAG == 1 in Step 1',
                  'time-resolved carbon input file, \n required only when "emission pattern" == 2 or 3 in Step 3',
                  'file to save the y when t = tfinal, \n required only when Save ystart == 1'
]),

]))

forward_mode = dash_table.DataTable(
    id='version',
    data=df_mode.to_dict('records'),
    columns=[{
        'id': 'Value',
        'name': 'Value',
        'type': 'numeric',
        'editable': True
    }, {
        'id': 'Parameter',
        'name': 'Parameter',
        'type': 'text',

    }, {
        'id': 'Options',
        'name': 'Options',
        'type': 'text'
    }, {
        'id': 'Comment',
        'name': 'Comment',
        'type': 'text',


    }],
    editable=False,
    style_table = df_style,
    style_cell={'fontSize':18,
    'font-family':'sans-serif',
     "whiteSpace": "pre-line",
     'textAlign': 'left',
     'border':'1px solid grey',
     'height': 40},
     style_header={
         # 'backgroundColor': 'rgb(210, 210, 210)',
         'color': 'black',
         'fontWeight': 'bold',
         'boarder' : '1px solid black'
     },
)

forward_params = dash_table.DataTable(
    id='model',
    data=df_param.to_dict('records'),
    columns=[{
        'id': 'Value',
        'name': 'Value',
        'type': 'numeric',
        'editable': True
    }, {
        'id': 'Parameter',
        'name': 'Parameter',
        'type': 'text',

    }, {
        'id': 'Unit',
        'name': 'Unit',
        'type': 'text'
    }, {
        'id': 'Comment',
        'name': 'Comment',
        'type': 'text',


    }],
    editable=False,
    style_table = df_style,
    style_cell={'fontSize':18,
    'font-family':'sans-serif',
     "whiteSpace": "pre-line",
     'textAlign': 'left',
     'border':'1px solid grey',
     'height': 40},
     style_header={
         # 'backgroundColor': 'rgb(210, 210, 210)',
         'color': 'black',
         'fontWeight': 'bold',
         'boarder' : '1px solid black'
     },
)

forward_carbon = dash_table.DataTable(
    id='carbon',
    data=df_carbon_emission.to_dict('records'),
    columns=[{
        'id': 'Value',
        'name': 'Value',
        'type': 'numeric',
        'editable': True
    }, {
        'id': 'Parameter',
        'name': 'Parameter',
        'type': 'text',

    }, {
        'id': 'Unit',
        'name': 'Unit',
        'type': 'text'
    }, {
        'id': 'Comment',
        'name': 'Comment',
        'type': 'text',


    }],
    editable = False,
    style_table = df_style,
    style_cell={'fontSize':18,
    'font-family':'sans-serif',
     "whiteSpace": "pre-line",
     'textAlign': 'left',
     'border':'1px solid grey',
     'height': 40},
     style_header={
         # 'backgroundColor': 'rgb(210, 210, 210)',
         'color': 'black',
         'fontWeight': 'bold',
         'boarder' : '1px solid black'
     },
)

forward_file = dash_table.DataTable(
    id='file',
    data=df_file.to_dict('records'),
    columns=[{
        'id': 'File name',
        'name': 'File name',
        'type': 'text',
        'editable': True
    },{
        'id': 'Comment',
        'name': 'Comment',
        'type': 'text',

    }],
    editable=False,
    style_table = df_style,
    style_cell={'fontSize':18,
    'font-family':'sans-serif',
     "whiteSpace": "pre-line",
     'textAlign': 'left',
     'border':'1px solid grey',
     'height': 40},
     style_header={
         # 'backgroundColor': 'rgb(210, 210, 210)',
         'color': 'black',
         'fontWeight': 'bold',
         'boarder' : '1px solid black'
     },

)

parameters_mode = {"FTYS": 0, 'FSED': 1, 'LOADFLAG': 0, 'tsnsflag': 0,'svstart': 1,}
param_mode = dcc.Store(id = 'param_mode_container', data = parameters_mode)

parameters_model = {'t0': 0, 'tfinal': 2e5, 'pref': 280, 'pcsi': 280,

                    'fepl': 0.8, 'eph':1.8, 'rrain':6.1, "fsh":1,
                    'fsi0': 5e12, 'finc0': 12, 'd13cin': 1.5, 'd13cvc': -4.0,
                    'thc': 20, 'cac': 10.3e-3, 'mgc': 53e-3, 'sclim': 3, 'nsi':0.2,
                    'ncc': 0.4}
param_model = dcc.Store(id = 'param_model_container', data = parameters_model)

parameters_carbon = {'cinpflag': 0, 'cinp': 1000, 'dccinp': -55, 'tcin0':0, 'tcspan': 6000}
param_carbon = dcc.Store(id = 'param_carbon_container', data = parameters_carbon)


parameters_file = {'initfile': './preind_steady.dat', 'cinpfile': './1000_0500.dat', 'svfile': './preind_steady.dat'}
param_file = dcc.Store(id = 'param_file_container', data = parameters_file)

run_section = html.Div(style = {'textAlign':'left', "margin-left": "10rem"}, children =
        [
        dbc.Label(style = {'fontSize': 24}, children = "Experiment name"),
        dbc.Input(placeholder = 'Input experiment name...', id = 'exp_name', type = 'text'),
        dbc.FormText('The modeling results will be saved in a dictionary after experinent name', style = {'fontSize': 18})

        ]
)

run_info =   dbc.Container(style = run_info_style, id = 'run_info',children = [ dbc.Row([
        dbc.Col(html.Div(id = 'info_starting', key = ''))]),

    dbc.Row([
           dbc.Col(dbc.FormText(id = 'progress_bar_title', children = [],
        style = { "padding": "0rem 0rem"}), style = {'textAlign': 'left', 'margin-bottom': '2rem'},),


        ]),
    dbc.Row([
        dbc.Col(html.Progress(id="progress_bar", children = ['Progress'], value="0", hidden = True,
        style = {'width': '30rem', 'textAlign': 'left'})),


    ]),
    dbc.Row([
        dbc.Col(html.Div(id = 'info_integration'))]),

    dbc.Row([
        dbc.Col(html.Div(id = 'info_wo_results'))]),
        ])
link_forward = "https://github.com/Shihan150/iloscar/blob/main/README.md#1-forward-model-example"
link_inverse = "https://github.com/Shihan150/iloscar/blob/main/README.md#2-inverse-model-example"
#################

layout = dbc.Container(fluid = False,style = Home_STYLE, children = [
    dcc.Store(id = 'ysol', data = []),
    dcc.Store(id = 'tsol', data = []),

    dbc.Row([
        dbc.Col(html.Div("The first column in each table is editable and users can manually adjust the values.",
                        style={'fontSize':20, 'textAlign':'left', 'font-style': 'italic', "margin-left": "10rem",'padding': '1rem 1rem'} )),

    ]),
    # dbc.Row([
    #     dbc.Col(
    #     html.P(["Learn how to run the model from the ",  html.Label([ html.A('example', href=link_forward, target = '_blank'),  '.'])]),
    #     style={'fontSize':20, 'textAlign':'left', 'font-style': 'italic', "margin-left": "10rem",'padding': '1rem 1rem'}
    # )]),

    dbc.Row([
        dbc.Col(html.Div("Step 1: select the experiment version",
                        style={'fontSize':24, 'textAlign':'left', "margin-left": "10rem",'padding': '1rem 1rem'} )),

    ]),
    dbc.Row([
        dbc.Col(forward_mode)
    ]),
    html.Br(),
    dbc.Row([

        dbc.Col(dbc.Alert(id = 'warning', color = 'danger', children = [], is_open = False))
    ]),

    dbc.Row([
        dbc.Col(param_mode)
    ]),

    dbc.Row([
        dbc.Col(html.Br())
    ]),

    dbc.Row([
        dbc.Col(html.Div(id = 'test'))
    ]),
####################
    dbc.Row([
        dbc.Col(html.Div("Step 2: select the model parameters",
                        style={'fontSize':24,'textAlign':'left', "margin-left": "10rem",'padding': '1rem 1rem'} )),

    ]),

    dbc.Row([
        dbc.Col(forward_params)
    ]),

    dbc.Row([
        dbc.Col(param_model)
    ]),


###############################
    dbc.Row([
        dbc.Col(html.Br())
    ]),
    dbc.Row([
        dbc.Col(html.Div("Step 3: select the carbon emission scenario",
                        style={'fontSize':24, 'textAlign':'left', "margin-left": "10rem",'padding': '1rem 1rem'} )),

    ]),

    dbc.Row([
        dbc.Col(forward_carbon)]),

    dbc.Row([
        dbc.Col(param_carbon)
    ]),

    dbc.Row([
        dbc.Col(html.Br()),]),


    ####################
    dbc.Row([
        dbc.Col(html.Div("Step 4: select required external file, path information included ",
                        style={'fontSize':24,'textAlign':'left', "margin-left": "10rem",'padding': '1rem 1rem'} )),
    ]),

    dbc.Row([
        dbc.Col(forward_file)]),

    dbc.Row([
        dbc.Col(param_file)
    ]),



    dbc.Row([
        dbc.Col(html.Br()), dcc.Store(id = 'parameters', data = [])]),

    dbc.Row([
        dbc.Col(html.Div(id = 'test4')),

    dbc.Row([
        dbc.Col(run_section),
        dbc.Col(html.Div(
            [
            dbc.Button("Run",  id = 'run', outline = True, color = 'dark', className = "me-1", n_clicks = 0),
            # dbc.Button('Cancel', id = 'cancel_run', outline = True, color = 'dark', className = 'me-1', n_clicks = 0),
            dbc.Button('Clean the output', id = 'clean', outline = True, color = 'secondary', className = 'me-1', n_clicks = 0)
            ],
            className="d-grid gap-2 col-6 mx-auto",
            style = {
            "margin-left": "-5rem",
            "margin-right": "5rem",
            "padding": "1rem 0rem",
            }
            )
            )

]),

    ### running info
    run_info,
    html.Br(),
    dbc.Row(html.Div(id = 'pco2_display'),style = run_info_style),
    html.Br(),
    dbc.Row(html.Div(id = 'CCD_display'), style = run_info_style),
    html.Br(style = run_info_style)

    ])
])

# update param_mode according to input
@callback(Output("param_mode_container", "data"),

                [Input('version', "data")],
                State('param_mode_container', 'data'))
def update_param_mode(data, data_pre):
    new_data_keys = list(data_pre.keys())
    new_data_value = list(pd.DataFrame(data)['Value'])
    params = dict(zip(new_data_keys, new_data_value))


    return params

# check the Mode control
@callback(Output("warning", 'children'),
            Output('warning', 'is_open'),
          Input("param_mode_container", 'data')
    )

def mode_warning(data):
    if data['FTYS'] != 0 and data['FTYS'] != 1:
        return html.Div('Invalid PALEO value, must be 0 or 1'), True

    elif data['FSED'] != 0 and data['FSED'] != 1:
        return html.Div('Invalid Sediment value, must be 0 or 1'), True

    elif data['LOADFLAG'] != 0 and data['LOADFLAG'] != 1:
        return html.Div('Invalid LOADFLAG value, must be 0 or 1'), True

    else:
        return [], False



#update model parameters according to model
@callback(

          Output('model', 'data'),
          # Output('test3', 'children'),
                [Input('version', "data")],
                State('model', 'data'),
                State('param_mode_container', 'data'),
        )
def update_param_model_from_mode(data, data_pre, data_mode_pre):

    ftys = data[0]['Value']
    ftys_pre = data_mode_pre['FTYS']

    if ftys == ftys_pre:
        return data_pre

    else:
        if ftys == 1:
            data_pre[2]['Value'] = 500
            data_pre[3]['Value'] = 1000
            data_pre[6]['Value'] = 6.7
            data_pre[7]['Value'] = 4.5
            data_pre[12]['Value'] = 25
            data_pre[10]['Value'] = 2.0
            data_pre[13]['Value'] = 20e-3
            data_pre[14]['Value'] = 30e-3
            # file_data[0]['File name'] = './petm_steady.dat'


        else:
            data_pre[2]['Value'] = 280
            data_pre[3]['Value'] = 280
            data_pre[6]['Value'] = 6.1
            data_pre[7]['Value'] = 1
            data_pre[12]['Value'] = 20
            data_pre[10]['Value'] = 1.5
            data_pre[13]['Value'] = 10.3e-3
            data_pre[14]['Value'] = 53e-3
            # file_data[0]['File name'] = './preind_steady.dat'

        return data_pre
#

@callback(

          Output('file', 'data'),
          # Output('test3', 'children'),
                [Input('version', "data")],
                State('file', 'data'),
                State('param_mode_container', 'data'),
        )
def update_param_model_from_mode(data, data_pre, data_mode_pre):

    ftys = data[0]['Value']
    ftys_pre = data_mode_pre['FTYS']

    if ftys == ftys_pre:
        return data_pre

    else:
        if ftys == 1:

            data_pre[0]['File name'] = './petm_steady.dat'
            data_pre[2]['File name'] = './petm_steady.dat'


        else:
            data_pre[0]['File name'] = './preind_steady.dat'
            data_pre[2]['File name'] = './preind_steady.dat'

        return data_pre

# update param_model data according to input
@callback(Output("param_model_container", "data"),

                [Input('model', "data")],
                State('param_model_container', 'data')

                )
def update_param_model(data, data_pre):
    new_data_keys = list(data_pre.keys())
    new_data_value = list(pd.DataFrame(data)['Value'])
    params = dict(zip(new_data_keys, new_data_value))
    return params



# update carbon emission scenario according to input
@callback(Output("param_carbon_container", "data"),

                [Input('carbon', "data")],
                State('param_carbon_container', 'data')

                )
def update_param_carbon(data, data_pre):
    new_data_keys = list(data_pre.keys())
    new_data_value = list(pd.DataFrame(data)['Value'])
    params = dict(zip(new_data_keys, new_data_value))
    return params

# update file information according to input
@callback(Output("param_file_container", "data"),

                [Input('file', "data")],
                State('param_file_container', 'data')

                )
def update_param_file(data, data_pre):
    new_data_keys = list(data_pre.keys())
    new_data_value = list(pd.DataFrame(data)['File name'])
    params = dict(zip(new_data_keys, new_data_value))
    return params


# merge all parameters
@callback(Output("parameters", "data"),
        Input('run', 'n_clicks'),
        Input('clean', 'n_clicks'),
            State('param_mode_container', 'data'),
            State('param_model_container', 'data'),
            State('param_carbon_container', 'data'),
            State('param_file_container', 'data'),
            State('exp_name', 'value'),

            prevent_initial_call = True
                )
def merge_params(n1, n2, dict1, dict2, dict3, dict4, exp_name):
    triggered_id = ctx.triggered_id
    if triggered_id == 'run':
        dict1.update(dict2)
        dict1.update(dict3)
        dict1.update(dict4)
        dict1['RUN_TYPE'] = 1
        dict1['exp_name'] = exp_name

        return dict1

    if triggered_id == 'clean':
        return {}


# initialize the model
@callback(Output('info_starting', 'children'),
        Output('info_starting', 'key'),
        Input('parameters', 'data'),
        prevent_initial_call = True
        )

def initialize(data):

    if data:
        info_starting = init_start(data)

        return info_starting

    else:
        return [], 'Fail'

# activate the progress bar
@callback(Output('progress_bar', 'hidden'),
            Output('progress_bar_title', 'children'),
            Input('info_starting', 'key'),
            Input('info_starting', 'children'),
            prevent_initial_call = True,
            )
def activate_progress_bar(key, info):

    if info:
        if key == 'Fail':
            raise PreventUpdate
        if key == 'Success':
            return True, 'Progressing...'

    else:
        return True, []

# run the model
@callback(output = [Output('info_integration', 'children'), Output('ysol', 'data'), Output('tsol', 'data')],
        inputs = [Input('progress_bar_title','children')],
        state = State('parameters', 'data'),
        background = False,
        progress = [Output('progress_bar', 'value'), Output('progress_bar', 'max')],
         running=[
        (Output("run", "disabled"), True, False),
        (Output('cancel_run', 'disabled'), False, True),
    ],
        cancel = [Input('cancel_run','n_clicks')],
        prevent_initial_call = True,

        )
def update_progress(key,data):


    if key:
        temp = init_start(data)
        return model_run(0)
    else:
        return [], [], []



# # save the results
# @callback(Output('info_wo_results','children'),
#
#             Input('run', 'n_clicks'), prevent_initial_call = True
#             )
#
# def clear_results(ysol, tsol):
#
#
#     return []


# save the results
@callback(Output('info_wo_results','children'),
            Input('ysol', 'data'),
            Input('tsol', 'data'),
            # Input('parameters', 'data'),
            prevent_initial_call = True
            )

def save_results(ysol, tsol):

    if ysol:
        return wo_results(ysol, tsol)

    else:
        return []


# plot the pco2 results
@callback(Output('pco2_display', 'children'),
            Output('CCD_display', 'children'),
            Input('info_wo_results', 'children'),
            State('exp_name', 'value'),
            State('param_mode_container', 'data'),
            prevent_initial_call = True
            )
def update_figure(data, exp_name, dict_mode):
    if data:

        data = pd.read_csv(f'{exp_name}/pCO2_d13c.csv')
        data_ocn = pd.read_csv(f'{exp_name}/Surface_dic_alk_d13c_ph.csv')
        data_ccd = pd.read_csv(f'{exp_name}/ccd.csv')
        fig = go.Figure()

        fig = make_subplots(rows = 3, cols = 1, shared_xaxes = True,
                            vertical_spacing = 0.02,
                            specs = [[{"secondary_y": False}], [{"secondary_y": True}],
                                    [{"secondary_y": False}]])


        fig.add_trace(go.Scatter(x = data_ocn.Age/1000, y = data_ocn.surface_dic,
                            mode = 'lines',
                            name = 'Mean surface DIC',
                            showlegend=True,
                            line = dict( width = 2)),

                            row = 1, col = 1)

        fig.add_trace(go.Scatter(x = data_ocn.Age/1000, y = data_ocn.surface_alk,
                            mode = 'lines',
                            name = 'Mean surface ALK',
                            showlegend=True,
                            line = dict( width = 2)),

                            row = 1, col = 1)


        fig.add_trace(go.Scatter(x = data.Age/1000, y = data.pCO2,
                            mode = 'lines',
                            name = 'pCO2',
                            line = dict(color = '#00b4d8', width = 2),
                            showlegend = False,
                            ),

                            row = 2, col = 1
                )

        fig.add_trace(go.Scatter(x=data_ocn.Age/1000, y = data_ocn.surface_pH,
                            mode = 'lines',
                            name = 'pH',
                            showlegend = False,
                            line = dict(color = '#9467BD', width = 2),
                            ),
                            row = 2, col = 1, secondary_y = True
                            )

        fig.add_trace(go.Scatter(x=data_ocn.Age/1000, y = data_ocn.surface_d13c,
                            mode = 'lines',
                            name = 'd13C',
                            showlegend = False,
                            line = dict(width = 2),
                            ),
                            row = 3, col = 1
                            )

        fig.update_xaxes(title_text="Age (kyr)", row=3, col=1, showline = True, showgrid = True, showticklabels = True,
                            linecolor = 'rgb(204,204,204)',
                            linewidth = 2, ticks = 'inside',
                            tickfont = dict( color = 'rgb(82,82,82)') )

        fig.update_xaxes(row = 1, col = 1,showline = True, showticklabels = False, showgrid = True,
                        linecolor = 'rgb(204,204,204)',
                            linewidth = 2, ticks = 'inside',
                            tickfont = dict( color = 'rgb(82,82,82)'))
        fig.update_xaxes(row = 2, col = 1,showline = True, showticklabels = False, showgrid = True,
                        linecolor = 'rgb(204,204,204)',
                            linewidth = 2, ticks = 'inside',
                            tickfont = dict( color = 'rgb(82,82,82)'))

        fig.update_yaxes(title_text = 'mmol/kg', row =1, col=1,
                         showgrid = True, zeroline = True, showline = True,
                            ticks = 'outside', linecolor = 'rgb(204,204,204)',
                            linewidth = 2
                        )

        fig.update_yaxes(title_text = 'd13C (per mil)', row =3, col=1,
                         showgrid = True, zeroline = True, showline = True,
                            ticks = 'outside', linecolor = 'rgb(204,204,204)',
                            linewidth = 2)

        fig.update_yaxes(title_text = 'mean surface pH', color = '#9467BD',
         row =2, col=1,
         showgrid = True, zeroline = True, showline = True,
            ticks = 'outside', linecolor ='#9467BD',
            linewidth = 2, secondary_y = True
        )
        fig.update_yaxes(title_text = 'atmospheric pCO2', color = '#00b4d8',
                         row =2, col=1,
                         showgrid = True, zeroline = True, showline = True,
                            ticks = 'outside', linecolor ='#00b4d8',
                            linewidth = 2, secondary_y = False
                        )


        fig.update_layout(

                        autosize=True,
                        # width=800,
                        height=900,
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

        fig1 = go.Figure()
        ocn_list = ['ATL', 'IND', 'PAC', 'TET']

        if dict_mode['FTYS'] == 1:

            n_ocn = 4
        else:
            n_ocn = 3

        for i in range(n_ocn):
            fig1.add_trace(go.Scatter(x=data_ccd.Age/1000, y = data_ccd.iloc[:,i+1],
                            mode = 'lines',
                            name = ocn_list[i],
                            showlegend = True,
                            line = dict(width = 2),
                            ),
                            )





        fig1.update_layout(xaxis_title = 'Age (kyr)', yaxis_title = 'CCD (m)')
        fig1.update_yaxes(autorange="reversed")
        fig1.update_layout(
                    autosize=True,
                    # width=800,
                    # height=300,
        xaxis = dict(
                    showline = True, showgrid = True, showticklabels = True,
                    linecolor = 'rgb(204,204,204)',
                    linewidth = 2, ticks = 'inside',
                    tickfont = dict( color = 'rgb(82,82,82)'),
                    ),
        yaxis = dict(
                    showgrid = True, zeroline = True, showline = True,
                    ticks = 'outside', linecolor = 'rgb(204,204,204)',
                    linewidth = 2
                    ),
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
        x=1)

        )


        return dcc.Graph(id ='pco2', figure = fig), dcc.Graph(id='CCD', figure = fig1)

    else:
        return {},{}
