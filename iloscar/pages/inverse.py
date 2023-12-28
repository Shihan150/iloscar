import dash
from dash import Input, Output, dcc, html, Dash, dash_table, html, callback, State, ctx
from dash.dash_table.Format import Format
import dash_bootstrap_components as dbc
from collections import OrderedDict
import pandas as pd
import pprint
from dash.exceptions import PreventUpdate

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from style import *
from iLOSCAR_backend import init_start, model_run, wo_results

dash.register_page(__name__, order = 3)

# choose the target variables
inv_opt = html.Div(
        children = [
        dbc.Row([
        dbc.Col(html.Div("Select the target variable",)),

        dbc.Col(dcc.Dropdown(options = {
        'pCO2': 'pCO2' ,
        'd13c':'Mean surface ocean d13c',
        'GSpH':'Global surface pH',
        'pCO2_d13c':'pCO2 + mean surface ocean d13c',
        'pH_d13c': 'pH + mean surface ocean d13c'
        },
        value = 'pCO2_d13c',
        id = 'target',
        style = {'fontSize':16, "margin-left": "4rem","margin-right": "-5rem" , 'width':250})),]),

        dbc.Row(html.Br()),

        dbc.Row(html.Div(
            # dbc.InputGroup([
            [dbc.Input(id = 'target_file', style = {'width': 700},
                value = '',
                placeholder = "INPUT the .csv file containing pCO2 data for inversion...",
                ),
            html.Br(),
            dbc.Input(id = 'target_file2', style = {'width': 700}, type = 'text',
                value = '',
                placeholder = "INPUT the .csv file containing d13c data for inversion...",
                )],
            # dbc.InputGroupText('.csv'),
            # ]
            # )

                ))

        ],
        style={'fontSize':24, 'textAlign':'left', "margin-left": "10rem",'padding': '1rem 1rem'}
     )




df_mode_inv = pd.DataFrame(OrderedDict([
    ('Value', [0,1,1,1]),
    ('Parameter', ['PALEO', 'Sediment', 'LOADFLAG', 'Ocean temperature change']),
    ('Options', [ '1/0', '1/0', '1/0', '1/0']),
    ('Comment', [ '1: paleo setup; \n 0: modern setup', '1: sediment box on; \n 0: sediment box off',
     '1: load initial settings from an external file; \n 0: off','1: ocean temperature change (co2-sensitivity) ON \n 0: Off',
         ]),

]))

df_param_inv = pd.DataFrame(OrderedDict([
    ('Value', [0,2e5,280, 280,
            0.8,1.8, 6.1,1.0,
            5, 12, 1.5, -4.0 ,
            20,10.3e-3, 53.0e-3, 3,
            0.2, 0.4]),
    ('Parameter', ['t0', 'tfinal', 'pCO2_ref', 'pCO2_initial',
                    'fepl', 'eph', 'rrain', 'fsh',
                    'silicate weathering0', 'carbonate weathering0',  'd13c carbonate weathering', 'd13c volcanic',
                    'conveyor transport',  'Ca_concentration', 'Mg concentration', 'climate sensitivity', 'nsi', 'ncc']),
   ('Unit', ['yr', 'yr', 'uatm', 'uatm',
              '-', 'mol m-2 yr-1', '-', '-',
              '10^12 mol yr-1', '10^12 mol yr-1', 'per mil','per mil',
              'Sv',  'mol/kg', 'mol/kg', '-', '-', '-']),

    ('Comment', [ 'follow the time range of target records', 'follow the time range of target records', 'pCO2 reference', 'steady-state pCO2',
            'biopump-efficiency', 'high-latitude carbon export', 'rain ratio', 'raise shelf rain relative to deep rain',
        'CaSiO3 weathering flux (initial)', 'CaCO3 weathering flux (initial)', 'd13c carbonate weathering', 'd13c volcanic degassing',
        'thermohaline transport', 'oceanic Ca concentration', 'oceanic Mg concentration', 'default OCN temperature change per double pCO2', 'silicate weathering exponent',
        'carbonate weathering exponent'

    ]),
]))

df_carbon_emission_inv = pd.DataFrame(OrderedDict([
    ('Value', [-55, -0.1, 2]),
    ('Parameter', [ 'd13c emission', 'Lower boundary in bracket for toms748 method. Value equivalent to expected minimum carbon degassing rate. Negative values represent organic carbon burial',
                        'Higher boundary in bracket for toms748 method. Value equivalent to maximum degassing rate']),
    ('Unit', [ 'per mil', 'Gt/yr', 'Gt/yr']),
    ('Comment', ['d13c of input carbon, \n required for the single version', 'Default settings can work for most applications. Adjust the value for extreme case',
    'Increase the absolute value can reduce the failure probability of experiment, but at the expense of computation time'
]),

]))

df_file_inv = pd.DataFrame(OrderedDict([
    ('File name', ['./preind_steady.dat']),
    ('Parameter', ['Initial steady state file name']),
    ('Comment', [ 'initial steady state file, \n mandatory for the inverse model'
]),

]))

inverse_mode = dash_table.DataTable(
    id='version_inv',
    data=df_mode_inv.to_dict('records'),
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

inverse_params = dash_table.DataTable(
    id='model_inv',
    data=df_param_inv.to_dict('records'),
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

inverse_carbon = dash_table.DataTable(
    id='carbon_inv',
    data=df_carbon_emission_inv.to_dict('records'),
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

inverse_file = dash_table.DataTable(
    id='file_inv',
    data=df_file_inv.to_dict('records'),
    columns=[{
        'id': 'File name',
        'name': 'File name',
        'type': 'text',
        'editable': True
    },
    {
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

parameters_mode_inv = {"FTYS": 0, 'FSED': 1, 'LOADFLAG': 0, 'tsnsflag': 0,'svstart': 1,}
param_mode_inv = dcc.Store(id = 'param_mode_inv_container', data = parameters_mode_inv)

parameters_model_inv = {'t0': 0, 'tfinal': 2e5, 'pref': 280, 'pcsi': 280,

                    'fepl': 0.8, 'eph':1.8, 'rrain':6.1, "fsh":1,
                    'fsi0': 5e12, 'finc0': 12, 'd13cin': 1.5, 'd13cvc': -4.0,
                    'thc': 20, 'cac': 10.3e-3, 'mgc': 53e-3, 'sclim': 3, 'nsi':0.2,
                    'ncc': 0.4}
param_model_inv = dcc.Store(id = 'param_model_inv_container', data = parameters_model_inv)

parameters_carbon_inv = {'dccinp':-55, 'toms_low': -0.5, 'toms_high': 5}
param_carbon_inv = dcc.Store(id = 'param_carbon_inv_container', data = parameters_carbon_inv)


parameters_file_inv = {'initfile': './preind_steady.dat', 'cinpfile': './pulse_emi.dat'}
param_file_inv = dcc.Store(id = 'param_file_inv_container', data = parameters_file_inv)

run_section_inv = html.Div(style = {'textAlign':'left', "margin-left": "10rem"}, children =
        [
        dbc.Label(style = {'fontSize': 24}, children = "Experiment name"),
        dbc.Input(placeholder = 'Input experiment name...', id = 'exp_name_inv', type = 'text'),
        dbc.FormText('The modeling results will be saved in a dictionary after experinent name', style = {'fontSize': 18})
        ]
)

run_info_inv = dbc.Container(style = run_info_style, id = 'run_info', children = [
dbc.Row([
    dbc.Col(html.Div(id = 'info_starting_inv', key = ''))]),


dbc.Row([
       dbc.Col(dbc.FormText(id = 'progress_bar_title_inv', children = [],
    style = { "padding": "0rem 0rem"})),

    ]),
dbc.Row([
    dbc.Col(html.Progress(id="progress_bar_inv", children = ['Progress'], value="0", hidden = True,
    style = {'width': '30rem', 'textAlign': 'left'})),


]),
dbc.Row([
    dbc.Col(html.Div(id = 'info_integration_inv'))]),

dbc.Row([
    dbc.Col(html.Div(id = 'info_wo_results_inv'))]),
])


###
layout = dbc.Container(fluid = False, style = Home_STYLE, children = [

    dcc.Store(id = 'inv_target', data = []),
    dcc.Store(id = 'ysol_inv', data = []),
    dcc.Store(id = 'tsol_inv', data = []),


    dbc.Row(
    dbc.Col(html.Div(style = {'width': 800}, children=[

        html.Div(inv_opt),


    ]))
    ),
    html.Hr(style = {'margin-left':'7rem', 'width':900}),

    dbc.Row([
        dbc.Col(html.Div("The first column in each table is editable and users can manually adjust the values.",
                        style={'fontSize':20, 'textAlign':'left', 'font-style': 'italic', "margin-left": "10rem",'padding': '1rem 1rem'} )),

    ]),

    dbc.Row([
        dbc.Col(html.Div("Step 1: choose the experiment version",
                        style={'fontSize':24, 'textAlign':'left', "margin-left": "10rem",'padding': '1rem 1rem'} )),

    ]),
    dbc.Row([
        dbc.Col(inverse_mode)
    ]),

    dbc.Row([
        dbc.Col(html.Div(id = 'warning_inv', style = CONTENT_STYLE))
    ]),

    dbc.Row([
        dbc.Col(param_mode_inv)
    ]),

    dbc.Row([
        dbc.Col(html.Br())
    ]),


####################
    dbc.Row([
        dbc.Col(html.Div("Step 2: choose the model parameters",
                        style={'fontSize':24, 'textAlign':'left', "margin-left": "10rem",'padding': '1rem 1rem'})),

    ]),

    dbc.Row([
        dbc.Col(inverse_params)
    ]),

    dbc.Row([
        dbc.Col(param_model_inv)
    ]),


###############################
    dbc.Row([
        dbc.Col(html.Br())
    ]),
    dbc.Row([
        dbc.Col(html.Div("Step 3: choose the carbon emission scenario",
                        style={'fontSize':24, 'textAlign':'left', "margin-left": "10rem",'padding': '1rem 1rem'})),

    ]),

    dbc.Row([
        dbc.Col(inverse_carbon)]),

    dbc.Row([
        dbc.Col(param_carbon_inv)
    ]),

    dbc.Row([
        dbc.Col(html.Br()),]),


    ####################
    dbc.Row([
        dbc.Col(html.Div("Step 4: choose required external file, path information included ",
                        style={'fontSize':24, 'textAlign':'left', "margin-left": "10rem",'padding': '1rem 1rem'})),

    ]),

    dbc.Row([
        dbc.Col(inverse_file)]),

    dbc.Row([
        dbc.Col(param_file_inv)
    ]),



    dbc.Row([
        dbc.Col(html.Br()), dcc.Store(id = 'parameters_inv', data = [])]),



    dbc.Row([
        dbc.Col(run_section_inv),
        dbc.Col(html.Div(
            [
            dbc.Button("Run",  id = 'run_inv', outline = True, color = 'dark', className = "me-1", n_clicks = 0),
            dbc.Button('Cancel', id = 'cancel_run_inv', outline = True, color = 'secondary', className = 'me-1', n_clicks = 0),
            dbc.Button('Clean the output', id = 'clean_inv', outline = True, color = 'secondary', className = 'me-1', n_clicks = 0)
            ],
            className="d-grid gap-2 col-6 mx-auto",
            style = {
            "margin-left": "-5rem",
            "margin-right": "5rem",
            "padding": "1rem 0rem",
            }
            )),]),


    ### running info
    run_info_inv,
    html.Br(),
    dbc.Row(html.Div(id = 'inv_results_display', style = run_info_style))



])


# update the placeholder info from the variable selection
@callback(Output("target_file", 'placeholder'),
          Output('target_file', 'value'),
            Input('target', 'value'),
            prevent_initial_call = True
            )
def update_placeholder_target_file(value):
    if value == 'pCO2':
        return 'INPUT the .csv file containing pCO2 data for inversion...', []

    elif value == 'd13c':
        return 'INPUT the .csv file containing mean surface ocean d13C for inversion...', []

    elif value == 'pCO2_d13c':
        return 'INPUT the .csv file containing pCO2 for double inversion...', []

    elif value == 'GSpH':
        return 'INPUT the .csv file containing mean surface ocean pH for inversion...', []

    elif value == 'pH_d13c':
        return 'INPUT the .csv file containing mean surface ocean pH for inversion...', []

    elif value == None:

        return "select the target variable for inversion first...", []

# Input file 2 for double inversion
@callback(Output("target_file2", 'placeholder'),
          Output('target_file2', 'type'),
            Input('target', 'value'),
            prevent_initial_call = True
            )
def update_placeholder_target_file(value):
    if value == 'pCO2':
        return 'INPUT the .csv file containing pCO2 data for inversion...', 'hidden'

    elif value == 'd13c':
        return 'INPUT the .csv file containing mean surface ocean d13C for inversion...', 'hidden'

    elif value == 'pCO2_d13c':
        return 'INPUT the .csv file containing d13c data for inversion...', 'text'

    elif value == 'GSpH':
        return 'INPUT the .csv file containing d13c for inversion...', 'hidden'

    elif value == 'pH_d13c':
        return 'INPUT the .csv file containing d13c data for inversion...', 'text'

    elif value == None:

        return "INPUT the .csv file containing d13c data for inversion...", 'hidden'


# store the target information for inversion
@callback(
        Output('inv_target', 'data'),
        Input('target', 'value'),
        Input('target_file', 'value'),
        Input('target_file2', 'value')
        )
def update_inv_info(value1, value2, value3):
    dict = {'target': value1, 'target_file': value2, 'target_file2': value3}

    return dict

# update param_mode according to input
@callback(Output("param_mode_inv_container", "data"),

                [Input('version_inv', "data")],
                State('param_mode_inv_container', 'data'))
def update_param_mode_inv(data, data_pre):
    new_data_keys = list(data_pre.keys())
    new_data_value = list(pd.DataFrame(data)['Value'])
    params = dict(zip(new_data_keys, new_data_value))


    return params

# check the Mode control
@callback(Output("warning_inv", 'children'),
          Input("param_mode_inv_container", 'data')
    )

def mode_warning(data):
    if data['FTYS'] != 0 and data['FTYS'] != 1:
        return html.Div('Invalid PALEO value, must be 0 or 1')

    if data['FSED'] != 0 and data['FSED'] != 1:
        return html.Div('Invalid Sediment value, must be 0 or 1')

    if data['LOADFLAG'] != 0 and data['LOADFLAG'] != 1:
        return html.Div('Invalid LOADFLAG value, must be 0 or 1')



#update model parameters according to model
@callback(

          Output('model_inv', 'data'),

                [Input('version_inv', "data")],
                State('model_inv', 'data'),
                State('param_mode_inv_container', 'data'),
        )
def update_param_mode_inv_from_mode(data, data_pre, data_mode_pre):

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

          Output('file_inv', 'data'),

                [Input('version_inv', "data")],
                State('file_inv', 'data'),
                State('param_mode_inv_container', 'data'),
        )
def update_param_file_inv_from_mode(data, data_pre, data_mode_pre):

    ftys = data[0]['Value']
    ftys_pre = data_mode_pre['FTYS']

    if ftys == ftys_pre:
        return data_pre

    else:
        if ftys == 1:

            data_pre[0]['File name'] = './petm_steady.dat'


        else:
            data_pre[0]['File name'] = './preind_steady.dat'

        return data_pre

# update param_model_inv data according to input
@callback(Output("param_model_inv_container", "data"),

                [Input('model_inv', "data")],
                State('param_model_inv_container', 'data')

                )
def update_param_mode_inv(data, data_pre):
    new_data_keys = list(data_pre.keys())
    new_data_value = list(pd.DataFrame(data)['Value'])
    params = dict(zip(new_data_keys, new_data_value))
    return params



# update carbon emission scenario according to input
@callback(Output("param_carbon_inv_container", "data"),

                [Input('carbon_inv', "data")],
                State('param_carbon_inv_container', 'data')

                )
def update_param_carbon_inv(data, data_pre):
    new_data_keys = list(data_pre.keys())
    new_data_value = list(pd.DataFrame(data)['Value'])
    params = dict(zip(new_data_keys, new_data_value))
    params['cinpflag'] = 0

    return params

# update file information according to input
@callback(Output("param_file_inv_container", "data"),

                [Input('file_inv', "data")],
                State('param_file_inv_container', 'data')

                )
def update_param_file_inv(data, data_pre):
    new_data_keys = list(data_pre.keys())
    new_data_value = list(pd.DataFrame(data)['File name'])
    params = dict(zip(new_data_keys, new_data_value))
    return params


# merge all parameters
@callback(Output("parameters_inv", "data"),

            [Input('run_inv', "n_clicks"),
            Input('clean_inv', 'n_clicks')],

                State('param_mode_inv_container', 'data'),
                State('param_model_inv_container', 'data'),
                State('param_carbon_inv_container', 'data'),
                State('param_file_inv_container', 'data'),
                State('exp_name_inv', 'value'),
                State('inv_target', 'data'),
                prevent_initial_call = True
                )
def merge_params(n1, n2, dict1, dict2, dict3, dict4, exp_name, dict5):
    triggered_id = ctx.triggered_id
    if triggered_id =='run_inv':
        dict1.update(dict2)
        dict1.update(dict3)
        dict1.update(dict4)
        dict1.update(dict5)
        dict1['RUN_TYPE'] = 2
        dict1['exp_name'] = exp_name


        return dict1
    if triggered_id == 'clean_inv':
        return {}

# initialize the model
@callback(Output('info_starting_inv', 'children'),
        Output('info_starting_inv', 'key'),
        Input('parameters_inv', 'data'),
        prevent_initial_call = True
        )

def initialize(data):
    if data:
        info_starting_inv = init_start(data)

        return info_starting_inv

    else:
        return [], 'Fail'

# activate the progress bar
@callback(Output('progress_bar_inv', 'hidden'),
            Output('progress_bar_title_inv', 'children'),
            Input('info_starting_inv', 'key'),
            Input('info_starting_inv', 'children'),
            prevent_initial_call = True,
            )
def activate_progress_bar_inv(key, info):
    if info:
        if key == 'Fail':
            raise PreventUpdate
        if key == 'Success':
            return False, 'Progressing...'
    else:
        return True, []
# run the model
@callback(output = [ Output('info_integration_inv', 'children'), Output('ysol_inv', 'data'), Output('tsol_inv', 'data')],
        inputs = Input('progress_bar_inv','hidden'),
        state = State('parameters_inv', 'data'),
        background = True,
        running=[
       (Output("run_inv", "disabled"), True, False),
       (Output('cancel_run_inv', 'disabled'), False, True),
   ],
        progress = [Output('progress_bar_inv', 'value'), Output('progress_bar_inv', 'max')],
        cancel = [Input('cancel_run_inv','n_clicks')],
        prevent_initial_call = True,

        )
def update_progress(set_progress,key, data):
    if key:
        return [], [], []
    else:
        
        temp = init_start(data)
        return model_run(set_progress)


# save the results
@callback(Output('info_wo_results_inv','children'),
            Input('ysol_inv', 'data'),
            Input('tsol_inv', 'data'), prevent_initial_call = True
            )

def save_results(ysol, tsol):

    if ysol:
        return wo_results(ysol, tsol)
    else:
        return []


# plot the inversion results
@callback(Output('inv_results_display', 'children'),
            Input('info_wo_results_inv', 'children'),
            State('exp_name_inv', 'value'),
            State('inv_target', 'data'),
            prevent_initial_call = True
            )
def update_figure(data, exp_name, dict1):

    if data:
        fig = go.Figure()
        if dict1['target'] == 'pCO2' or dict1['target'] == 'GSpH' or dict1['target']=='d13c':
            if dict1['target'] == 'pCO2':
                data = pd.read_csv(f'{exp_name}/pCO2_d13c.csv')
                data2 = pd.read_csv(dict1['target_file'])
                data3 = pd.read_csv('inverse_emission_from_pco2.csv')

                fig = make_subplots(rows = 2, cols = 1, shared_xaxes = True,
                                    vertical_spacing = 0.02)


                fig.add_trace(go.Scatter(x = data.Age/1000, y = data.pCO2,
                                    mode = 'lines',
                                    name = 'Invere results',
                                    line = dict(color = '#00b4d8', width = 2),
                                    ), row = 1, col = 1
                        )

                fig.add_trace(go.Scatter(x = data2.iloc[:,0]/1000, y = data2.iloc[:,1],
                                    mode = 'markers',
                                    name = 'Target',
                                    marker=dict(size=8,
                                  line=dict(width=2,
                                            color='DarkSlateGrey')),), row = 1, col = 1)

                fig.add_trace(go.Scatter(x = data3.Age/1000, y = data3.total_carbon_emission_Gt,
                                    mode = 'lines',
                                    showlegend=False,
                                    line = dict(color = '#00b4d8', width = 2)),

                                    row = 2, col = 1)

                fig.update_xaxes(title_text="Age (kyr)", row=2, col=1, showline = True, showgrid = True, showticklabels = True,
                    linecolor = 'rgb(204,204,204)',
                    linewidth = 2, ticks = 'inside',
                    tickfont = dict( color = 'rgb(82,82,82)') )

                fig.update_xaxes(row = 1, col = 1,showline = True, showticklabels = False, showgrid = True,
                                linecolor = 'rgb(204,204,204)',
                                    linewidth = 2, ticks = 'inside',
                                    tickfont = dict( color = 'rgb(82,82,82)'))

                fig.update_yaxes(title_text = 'pCO2 (uatm)', row =1, col=1,
                                 showgrid = True, zeroline = True, showline = True,
                                    ticks = 'outside', linecolor = 'rgb(204,204,204)',
                                    linewidth = 2
                                )

                fig.update_yaxes(title_text = 'Cumulative emission (Gt)', row =2, col=1,
                                 showgrid = True, zeroline = True, showline = True,
                                    ticks = 'outside', linecolor = 'rgb(204,204,204)',
                                    linewidth = 2)
                fig.update_layout(

                                autosize=False,
                                width=800,
                                height=600,
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



            elif dict1['target'] == 'd13c':
                data = pd.read_csv((f'{exp_name}/Surface_dic_alk_d13c_ph.csv'))
                data2 = pd.read_csv(dict1['target_file'])
                data3 = pd.read_csv('inverse_emission_from_d13c.csv')

                fig = make_subplots(rows = 2, cols = 1, shared_xaxes = True,
                                    vertical_spacing = 0.02)


                fig.add_trace(go.Scatter(x = data.Age/1000, y = data.surface_d13c,
                                    mode = 'lines',
                                    name = 'Invere results',
                                    line = dict(color = '#00b4d8', width = 2),
                                    ), row = 1, col = 1
                        )

                fig.add_trace(go.Scatter(x = data2.iloc[:,0]/1000, y = data2.iloc[:,1],
                                    mode = 'markers',
                                    name = 'Target',
                                    marker=dict(size=8,
                                  line=dict(width=2,
                                            color='DarkSlateGrey')),), row = 1, col = 1)

                fig.add_trace(go.Scatter(x = data3.Age/1000, y = data3.total_carbon_emission_Gt,
                                    mode = 'lines',
                                    showlegend=False,
                                    line = dict(color = '#00b4d8', width = 2)),

                                    row = 2, col = 1)

                fig.update_xaxes(title_text="Age (kyr)", row=2, col=1, showline = True, showgrid = True, showticklabels = True,
                    linecolor = 'rgb(204,204,204)',
                    linewidth = 2, ticks = 'inside',
                    tickfont = dict( color = 'rgb(82,82,82)') )

                fig.update_xaxes(row = 1, col = 1,showline = True, showticklabels = False, showgrid = True,
                                linecolor = 'rgb(204,204,204)',
                                    linewidth = 2, ticks = 'inside',
                                    tickfont = dict( color = 'rgb(82,82,82)'))

                fig.update_yaxes(title_text = 'Surface d13c', row =1, col=1,
                                 showgrid = True, zeroline = True, showline = True,
                                    ticks = 'outside', linecolor = 'rgb(204,204,204)',
                                    linewidth = 2
                                )

                fig.update_yaxes(title_text = 'Cumulative emission (Gt)', row =2, col=1,
                                 showgrid = True, zeroline = True, showline = True,
                                    ticks = 'outside', linecolor = 'rgb(204,204,204)',
                                    linewidth = 2)
                fig.update_layout(

                                autosize=False,
                                width=800,
                                height=600,
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


            elif dict1['target'] == 'GSpH':
                data = pd.read_csv((f'{exp_name}/Surface_dic_alk_d13c_ph.csv'))
                data2 = pd.read_csv(dict1['target_file'])
                data3 = pd.read_csv('inverse_emission_from_ph.csv')

                fig = make_subplots(rows = 2, cols = 1, shared_xaxes = True,
                                    vertical_spacing = 0.02)


                fig.add_trace(go.Scatter(x = data.Age/1000, y = data.surface_pH,
                                    mode = 'lines',
                                    name = 'Invere results',
                                    line = dict(color = '#00b4d8', width = 2),
                                    ), row = 1, col = 1
                        )

                fig.add_trace(go.Scatter(x = data2.iloc[:,0]/1000, y = data2.iloc[:,1],
                                    mode = 'markers',
                                    name = 'Target',
                                    marker=dict(size=8,
                                  line=dict(width=2,
                                            color='DarkSlateGrey')),), row = 1, col = 1)

                fig.add_trace(go.Scatter(x = data3.Age/1000, y = data3.total_carbon_emission_Gt,
                                    mode = 'lines',
                                    showlegend=False,
                                    line = dict(color = '#00b4d8', width = 2)),

                                    row = 2, col = 1)

                fig.update_xaxes(title_text="Age (kyr)", row=2, col=1, showline = True, showgrid = True, showticklabels = True,
                    linecolor = 'rgb(204,204,204)',
                    linewidth = 2, ticks = 'inside',
                    tickfont = dict( color = 'rgb(82,82,82)') )

                fig.update_xaxes(row = 1, col = 1,showline = True, showticklabels = False, showgrid = True,
                                linecolor = 'rgb(204,204,204)',
                                    linewidth = 2, ticks = 'inside',
                                    tickfont = dict( color = 'rgb(82,82,82)'))

                fig.update_yaxes(title_text = 'pH', row =1, col=1,
                                 showgrid = True, zeroline = True, showline = True,
                                    ticks = 'outside', linecolor = 'rgb(204,204,204)',
                                    linewidth = 2
                                )

                fig.update_yaxes(title_text = 'Cumulative emission (Gt)', row =2, col=1,
                                 showgrid = True, zeroline = True, showline = True,
                                    ticks = 'outside', linecolor = 'rgb(204,204,204)',
                                    linewidth = 2)
                fig.update_layout(

                                autosize=False,
                                width=800,
                                height=600,
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


            return dcc.Graph(id ='single_inv', figure = fig)

        elif dict1['target'] == 'pCO2_d13c' or dict1['target']=='pH_d13c':
            if dict1['target'] == 'pCO2_d13c':
                data = pd.read_csv(f'{exp_name}/pCO2_d13c.csv')
                data2 = pd.read_csv(dict1['target_file'])
                data4 = pd.read_csv(f'{exp_name}/Surface_dic_alk_d13c_ph.csv')
                data3 = pd.read_csv(dict1['target_file2'])

                data5 = pd.read_csv('double_inversion_emission.csv')
                data6 = pd.read_csv('double_inversion_emission_d13c.csv')

                fig = make_subplots(rows=3, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.02,
                    specs = [[{"secondary_y": False}], [{"secondary_y": False}],
                            [{"secondary_y": True}]]
                   )

                fig.add_trace(go.Scatter(x = data.Age/1000, y = data.pCO2,
                                                mode = 'lines',
                                                 name = 'Inversion results',
                                                line = dict(color = '#00b4d8', width = 2),
                                                ), row = 1, col = 1
                                    )
                fig.add_trace(go.Scatter(x = data2.iloc[:,0]/1000, y = data2.iloc[:,1],
                                                mode = 'markers',
                                                 name = 'Target',
                                             showlegend=False,
                                                marker=dict(size=8,
                                                            color = '#EF553B',
                                              line=dict(width=1.5,
                                                        color='DarkSlateGrey')),),
                             row = 1, col = 1)

                fig.add_trace(go.Scatter(x = data4.Age/1000, y = data4.surface_d13c,
                                                mode = 'lines',
                                                 name = 'Inversion results',
                                         showlegend=False,
                                                line = dict(color = '#00b4d8', width = 2),
                                                ), row = 2, col = 1
                                    )

                fig.add_trace(go.Scatter(x = data3.iloc[:,0]/1000, y = data3.iloc[:,1],
                                                mode = 'markers',
                                                 name = 'Target',
                                                marker=dict(size=8,
                                                            color = '#EF553B',
                                              line=dict(width=1.5,
                                                        color='DarkSlateGrey')),),
                             row = 2, col = 1)

                fig.add_trace(go.Scatter(x = data5.Age/1000, y = data5.total_carbon_emission_Gt,
                        mode = 'lines',
                        name = 'Cumulative emission',
                        showlegend=False,
                          line = dict(color = '#9467BD', width = 2)),

              row = 3, col = 1)

                fig.add_trace(go.Scatter(x = data6.Age/1000, y = data6.d13C_of_carbon_emission,
                                                mode = 'lines',
                                                 name = 'Emission d13C',
                                                 showlegend=False,
                                                line = dict(color = '#FF7F0E', width = 2),
                                                ), row = 3, col = 1, secondary_y = True
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

                fig.update_yaxes(title_text = 'pCO2 (uatm)', row =1, col=1,
                                 showgrid = True, zeroline = True, showline = True,
                                    ticks = 'outside', linecolor = 'rgb(204,204,204)',
                                    linewidth = 2
                                )

                fig.update_yaxes(title_text = 'd13C (per mil)', row =2, col=1,
                                 showgrid = True, zeroline = True, showline = True,
                                    ticks = 'outside', linecolor = 'rgb(204,204,204)',
                                    linewidth = 2)

                fig.update_yaxes(title_text = 'Cumulative emission (Gt)', color = '#9467BD',
                 row =3, col=1,
                 showgrid = True, zeroline = True, showline = True,
                    ticks = 'outside', linecolor ='#9467BD',
                    linewidth = 2, secondary_y = False
                )
                fig.update_yaxes(title_text = 'd13C of emission', color = '#FF7F0E',
                                 row =3, col=1,
                                 showgrid = True, zeroline = True, showline = True,
                                    ticks = 'outside', linecolor ='#FF7F0E',
                                    linewidth = 2, secondary_y = True
                                )


                fig.update_layout(

                                autosize=False,
                                width=800,
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

            if dict1['target'] == 'pH_d13c':
                data = pd.read_csv(f'{exp_name}/Surface_dic_alk_d13c_ph.csv')
                data2 = pd.read_csv(dict1['target_file'])
                data4 = pd.read_csv(f'{exp_name}/Surface_dic_alk_d13c_ph.csv')
                data3 = pd.read_csv(dict1['target_file2'])
                data5 = pd.read_csv('double_inversion_emission_pH.csv')
                data6 = pd.read_csv('double_inversion_emission_d13c_pH.csv')

                fig = make_subplots(rows=3, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.02,
                    specs = [[{"secondary_y": False}], [{"secondary_y": False}],
                            [{"secondary_y": True}]]
                   )

                fig.add_trace(go.Scatter(x = data.Age/1000, y = data.surface_pH,
                                                mode = 'lines',
                                                 name = 'Inversion results',
                                                line = dict(color = '#00b4d8', width = 2),
                                                ), row = 1, col = 1
                                    )
                fig.add_trace(go.Scatter(x = data2.iloc[:,0]/1000, y = data2.iloc[:,1],
                                                mode = 'markers',
                                                 name = 'Target',
                                             showlegend=False,
                                                marker=dict(size=8,
                                                            color = '#EF553B',
                                              line=dict(width=1.5,
                                                        color='DarkSlateGrey')),),
                             row = 1, col = 1)

                fig.add_trace(go.Scatter(x = data4.Age/1000, y = data4.surface_d13c,
                                                mode = 'lines',
                                                 name = 'Inversion results',
                                         showlegend=False,
                                                line = dict(color = '#00b4d8', width = 2),
                                                ), row = 2, col = 1
                                    )

                fig.add_trace(go.Scatter(x = data3.iloc[:,0]/1000, y = data3.iloc[:,1],
                                                mode = 'markers',
                                                 name = 'Target',
                                                marker=dict(size=8,
                                                            color = '#EF553B',
                                              line=dict(width=1.5,
                                                        color='DarkSlateGrey')),),
                             row = 2, col = 1)

                fig.add_trace(go.Scatter(x = data5.Age/1000, y = data5.total_carbon_emission_Gt,
                        mode = 'lines',
                        name = 'Cumulative emission',
                        showlegend=False,
                          line = dict(color = '#9467BD', width = 2)),
              row = 3, col = 1)

                fig.add_trace(go.Scatter(x = data6.Age/1000, y = data6.d13C_of_carbon_emission,
                                                mode = 'lines',
                                                 name = 'Emission d13C',
                                                 showlegend=False,
                                                line = dict(color = '#FF7F0E', width = 2),
                                                ), row = 3, col = 1, secondary_y = True
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

                fig.update_yaxes(title_text = 'pH', row =1, col=1,
                                 showgrid = True, zeroline = True, showline = True,
                                    ticks = 'outside', linecolor = 'rgb(204,204,204)',
                                    linewidth = 2
                                )

                fig.update_yaxes(title_text = 'd13C (per mil)', row =2, col=1,
                                 showgrid = True, zeroline = True, showline = True,
                                    ticks = 'outside', linecolor = 'rgb(204,204,204)',
                                    linewidth = 2)

                fig.update_yaxes(title_text = 'Cumulative emission (Gt)', color = '#9467BD',
                 row =3, col=1,
                 showgrid = True, zeroline = True, showline = True,
                    ticks = 'outside', linecolor ='#9467BD',
                    linewidth = 2, secondary_y = False
                )
                fig.update_yaxes(title_text = 'd13C of emission', color = '#FF7F0E',
                                 row =3, col=1,
                                 showgrid = True, zeroline = True, showline = True,
                                    ticks = 'outside', linecolor ='#FF7F0E',
                                    linewidth = 2, secondary_y = True
                                )


                fig.update_layout(

                                autosize=False,
                                width=800,
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
            return dcc.Graph(id = 'double_inv', figure = fig)
    else:
        return {}
