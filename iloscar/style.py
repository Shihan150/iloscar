# store the style information for iLOSCAR

# color platte
colors = {
    'background': '#fcfaea',
    'text': '#25252f',
    'title':'#FF8C00',
    'other':'#C5C5C5',
    'side_bar_back_color':"#f8f9fa",
    'warning': "#CC3300",
    'line': '#00b4d8'
}

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "13em",
    "padding": "2rem 1rem",
    "background-color": colors['side_bar_back_color'] ,
}



# add some padding.
CONTENT_STYLE = {
    "margin-left": "0rem",
    "margin-right": "2rem",
    "padding": "1rem 0rem",
    "color": colors['warning']
}

# Home page style
Home_STYLE = {
    'textAlign': 'left',
    'color': colors['text'],
    "fontSize": 24,
    "margin-left": "0rem",
    "margin-right": "0rem",
    "padding": "2rem 2rem",
    "whiteSpace": "pre-line",
    'backgroundColor': colors['background'],

}

# df style
df_style = {
    'width': 800,

    'overflowX': 'scroll',
    "margin-left": "10rem",
    "margin-right": "10rem",
    "whiteSpace": "pre-line",
    'backgroundColor':'#a9def9'

}

run_info_style = {
    'width': 800,

    'overflowX': 'scroll',
    "margin-left": "10rem",
    "margin-right": "10rem",
    "whiteSpace": "pre-line",
    'backgroundColor':'#fafafa',
    'fontSize': 18

}
